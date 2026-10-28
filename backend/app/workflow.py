import asyncio
from sqlalchemy.dialects.postgresql import insert
from .config import get_settings
from .database import (
    Session,
    ResearchRun,
    Citation,
    SourceSnapshot,
    EvidencePassage,
    ClaimRecord,
    ClaimEvidence,
    ConflictRecord,
    event,
)
from .fixtures import fixture_documents
from .llm import EvidenceModel, ModelUnavailable
from .policy import rank_documents, validate_claim, find_conflicts, digest, POLICY_VERSION
from .schemas import ResearchRequest, ProcessRequest, utcnow
from .sources import Sources
from .scope import resolve_scope


def structured_claims(citations: list[dict]) -> list[dict]:
    """Copy traceable trial fields; no model or medical inference."""
    claims = []
    for c in citations:
        if c["source"] != "clinicaltrials" or not c.get("eligible_sections"):
            continue
        subgroup = c["display_bucket"] == "specific_population"
        details = c.get("population", {})
        population = (
            ", ".join(x.replace("_", " ") for x in c.get("population_tags", [])) or "Condition population"
        )
        minimum, maximum = details.get("minimum_age"), details.get("maximum_age")
        age = (
            f"ages {minimum} to {maximum}"
            if minimum and maximum
            else f"minimum age {minimum}"
            if minimum
            else f"maximum age {maximum}"
            if maximum
            else "age range not reported"
        )
        population += f"; {age}"
        countries = ", ".join(details.get("countries", [])) or "location not reported"
        by_pointer = {e["locator"]: e for e in c["evidence"]}
        title = by_pointer.get("/protocolSection/identificationModule/briefTitle")
        status = by_pointer.get("/protocolSection/statusModule/overallStatus")
        if title:
            fields = [
                title,
                status,
                by_pointer.get("/protocolSection/statusModule/lastUpdatePostDateStruct/date"),
            ]
            fields.extend(
                by_pointer.get(f"/protocolSection/eligibilityModule/{f}")
                for f in ["minimumAge", "maximumAge"]
            )
            fields.extend(e for e in c["evidence"] if e["locator"].endswith("/country"))
            refs = [{"evidence_id": e["id"], "quote": e["text"]} for e in fields if e]
            claims.append(
                {
                    "section": "specific_populations" if subgroup else "emerging",
                    "claim_type": "development",
                    "text": f"Registered study: {title['text']}"
                    + (f". Registry status: {status['text']}." if status else ".")
                    + f" Population: {population}. Study location: {countries}."
                    + " This is registered research, not established treatment benefit.",
                    "intervention": ", ".join(x.get("name", "") for x in c.get("interventions", []))
                    or "unknown",
                    "population": population,
                    "outcome": "registry status",
                    "direction": "neutral",
                    "references": refs,
                    "origin": "structured_source_fields",
                }
            )
        for role in c["organization_roles"]:
            e = by_pointer.get(role["locator"])
            if e:
                claims.append(
                    {
                        "section": "specific_populations" if subgroup else "organizations",
                        "claim_type": "organization",
                        "text": f"{role['name']} ({'industry sponsor' if role.get('organization_class') == 'INDUSTRY' else 'institution / organization; company status not established'}) is listed as {role['role'].replace('_', ' ')} for {c['canonical_id']}."
                        + (f" Population: {population}." if subgroup else ""),
                        "intervention": "unknown",
                        "population": population,
                        "outcome": "documented organization role",
                        "direction": "neutral",
                        "references": [{"evidence_id": e["id"], "quote": e["text"]}],
                        "origin": "structured_source_fields",
                    }
                )
    return claims[:18]


def fixture_claims(citations: list[dict]) -> list[dict]:
    return [
        {
            "section": "care_landscape",
            "claim_type": "published_finding",
            "text": c["evidence"][0]["text"],
            "intervention": "Example intervention",
            "population": "adults",
            "outcome": "example endpoint",
            "direction": "positive" if i == 0 else "negative",
            "references": [{"evidence_id": c["evidence"][0]["id"], "quote": c["evidence"][0]["text"]}],
            "origin": "synthetic_policy_fixture",
        }
        for i, c in enumerate(citations)
    ]


def store_result(run_id: str, result: dict, citations: list[dict]):
    with Session.begin() as db:
        for c in citations:
            db.execute(
                insert(SourceSnapshot)
                .values(
                    id=c["snapshot_id"],
                    source=c["source"],
                    canonical_id=c["canonical_id"],
                    content_hash=c["snapshot_hash"],
                    data=c["snapshot"],
                )
                .on_conflict_do_nothing(index_elements=[SourceSnapshot.id])
            )
            db.add(
                Citation(
                    id=c["id"],
                    run_id=run_id,
                    snapshot_id=c["snapshot_id"],
                    data={k: v for k, v in c.items() if k != "snapshot"},
                )
            )
            db.flush()
            for e in c["evidence"]:
                db.add(
                    EvidencePassage(
                        id=e["id"],
                        citation_id=c["id"],
                        snapshot_id=c["snapshot_id"],
                        locator=e["locator"],
                        text=e["text"],
                    )
                )
        db.flush()
        for claim in result["claims"]:
            db.add(ClaimRecord(id=claim["id"], run_id=run_id, data=claim))
            db.flush()
            for ref in {r["evidence_id"]: r for r in claim["references"]}.values():
                db.add(
                    ClaimEvidence(
                        claim_id=claim["id"],
                        evidence_id=ref["evidence_id"],
                        quote=ref["quote"],
                        check={
                            "quote_in_snapshot": True,
                            "support_check": claim["support_check"],
                            "snapshot_hash": ref["snapshot_hash"],
                        },
                    )
                )
        for conflict in result["conflicts"]:
            db.add(ConflictRecord(id=conflict["id"], run_id=run_id, data=conflict))
        run = db.get(ResearchRun, run_id)
        run.result = result
        run.status = result["status"]
        run.finished_at = utcnow()


async def execute(run_id: str, request: ResearchRequest, sources: Sources):
    scope = resolve_scope(request.condition, request.population, allow_ambiguous=request.mode == "fixture")
    with Session.begin() as db:
        db.get(ResearchRun, run_id).status = "running"
    citations = []
    claims = []
    excluded_claims = []
    attempts = []
    warnings = []
    model = EvidenceModel()
    error = False
    try:
        async with asyncio.timeout(get_settings().run_timeout_seconds):
            event(
                run_id, "retrieving", "Retrieving fixed-source records; source text cannot change the policy."
            )
            if request.mode == "fixture":
                documents = fixture_documents(request.condition)
                attempts = [
                    {
                        "source": "synthetic_fixture",
                        "status": "success",
                        "reason": "Fabricated edge-case evidence; never a live result.",
                    }
                ]
            else:
                documents, attempts = await sources.collect(
                    request.condition,
                    min(request.max_records, get_settings().max_records),
                    getattr(request, "pmids", None) if isinstance(request, ProcessRequest) else None,
                    getattr(request, "nct_ids", None) if isinstance(request, ProcessRequest) else None,
                    population=request.population,
                )
            event(
                run_id,
                "authenticating",
                "Checking canonical source identity, snapshot locators and publication status.",
            )
            citations = rank_documents(documents, request.condition, run_id, request.population)
            event(
                run_id,
                "ranking",
                "Applying the fixed ordering policy and grouping explicit study identifiers.",
            )
            candidates = (
                fixture_claims(citations) if request.mode == "fixture" else structured_claims(citations)
            )
            model_candidates = []
            if request.use_llm and request.mode == "live":
                event(
                    run_id,
                    "extracting",
                    "OpenAI reads selected saved evidence through one allowlisted function tool.",
                )
                try:
                    extraction = await model.extract(request.condition, citations)
                    if extraction.limitations:
                        warnings.append(
                            f"{len(extraction.limitations)} uncited model limitation notes were withheld. Only claims with validated evidence references enter the briefing."
                        )
                    for candidate in extraction.claims:
                        raw = candidate.model_dump()
                        ok, reasons, refs = validate_claim(raw, citations)
                        if ok:
                            model_candidates.append(
                                {**raw, "references": refs, "origin": "openai_extraction"}
                            )
                        else:
                            excluded_claims.append({"text": raw["text"], "reason_codes": reasons})
                    event(
                        run_id,
                        "validating",
                        "Checking exact quotations and reviewing semantic support; automated review is not clinical validation.",
                    )
                    review = await model.review(model_candidates, citations)
                    for i, candidate in enumerate(model_candidates):
                        decision = review.get(i)
                        if decision and decision["supported"]:
                            candidate["support_explanation"] = decision["explanation"]
                            candidates.append(candidate)
                        else:
                            excluded_claims.append(
                                {
                                    "text": candidate["text"],
                                    "reason_codes": ["SEMANTIC_SUPPORT_NOT_CONFIRMED"],
                                    "explanation": decision["explanation"]
                                    if decision
                                    else "No valid reviewer decision.",
                                }
                            )
                except ModelUnavailable as exc:
                    warnings.append(
                        exc.code
                        + ": generated synthesis is unavailable; inspect source evidence and structured registry fields."
                    )
            elif request.mode == "live":
                warnings.append(
                    "Model synthesis was disabled. Literature is presented as source evidence, without generated medical conclusions."
                )
            for candidate in candidates:
                ok, reasons, refs = validate_claim(candidate, citations)
                if not ok:
                    excluded_claims.append({"text": candidate["text"], "reason_codes": reasons})
                    continue
                candidate["references"] = refs
                candidate["id"] = "cl_" + digest([run_id, candidate["text"], refs])[:26]
                candidate["support_check"] = (
                    "synthetic_fixture"
                    if request.mode == "fixture"
                    else "structured_field_copy"
                    if candidate["origin"] == "structured_source_fields"
                    else "automated_semantic_review"
                )
                candidate["review_needed"] = candidate["origin"] != "structured_source_fields"
                if not any(c["text"] == candidate["text"] for c in claims):
                    claims.append(candidate)
    except TimeoutError:
        warnings.append("RUN_DEADLINE_REACHED: only completed evidence stages are shown.")
    except asyncio.CancelledError:
        with Session.begin() as db:
            run = db.get(ResearchRun, run_id)
            run.status = "interrupted"
            run.finished_at = utcnow()
        raise
    except Exception:
        warnings.append("PROCESSING_ERROR: the run could not finish all evidence stages.")
        error = True
    conflicts = find_conflicts(claims, citations)
    warnings.insert(
        0,
        "Standard-of-care coverage is unavailable: this prototype has no registered guideline connector. This is a retrieval gap, not a statement that the condition has no established care.",
    )
    if request.mode == "fixture":
        warnings.insert(
            0,
            "SYNTHETIC FIXTURE: all publications and findings in this run are fabricated to demonstrate policy behavior.",
        )
    if any(c["access_level"] == "abstract_only" for c in citations):
        warnings.append("PubMed evidence is abstract-only where available; full papers were not read.")
    if any(a.get("truncated") for a in attempts):
        warnings.append(
            "Result caps were reached. This is a bounded search, not a comprehensive evidence review."
        )
    if any(a["status"] == "failed" for a in attempts):
        warnings.append(
            "One or more sources failed. No-match and retrieval failure are not evidence of absence."
        )
    result = {
        "run_id": run_id,
        "condition": request.condition,
        "scope": scope,
        "jurisdiction": "US",
        "mode": request.mode,
        "status": "failed" if error and not citations else "partial" if citations else "failed",
        "policy_version": POLICY_VERSION,
        "as_of": utcnow().isoformat(),
        "model": get_settings().model_name() if model.usage else None,
        "source_attempts": attempts,
        "citations": [{k: v for k, v in c.items() if k != "snapshot"} for c in citations],
        "claims": claims,
        "excluded_claims": excluded_claims,
        "conflicts": conflicts,
        "coverage": {
            "current_care": {
                "status": "unavailable",
                "reason": "No guideline connector is implemented. Applicable US guidance was not retrieved; published study findings cannot establish the standard of care.",
            },
            "care_landscape": {
                "status": "limited"
                if any(c["section"] == "care_landscape" for c in claims)
                else "unavailable",
                "reason": "Bounded literature search; abstract access and study applicability require review.",
            },
            "emerging": {
                "status": "limited" if any(c["section"] == "emerging" for c in claims) else "unavailable",
                "reason": "Active interventional treatment trials updated within 3 years, screened for condition and population. Registration is not approval or benefit; historical/unverified records remain in the register.",
            },
            "organizations": {
                "status": "limited"
                if any(c["section"] == "organizations" for c in claims)
                else "unavailable",
                "reason": "Documented sponsor/collaborator roles for eligible emerging studies only. Industry and institutional roles are labeled; no market-leader claim is made.",
            },
            "specific_populations": {
                "status": "limited"
                if any(c["section"] == "specific_populations" for c in claims)
                else "unavailable",
                "reason": "Population-specific evidence is kept separate from the requested overview. Eligibility and geographic applicability still need review.",
            },
        },
        "warnings": list(dict.fromkeys(warnings)),
        "usage": {
            "model_requests": len(model.usage),
            "requests": model.usage,
            "tool_calls": model.tool_calls,
            "cost_usd": None,
        },
        "ranking_explanation": "Screen condition/subtype and population before ordering. Emerging sections require active, recently updated interventional treatment trials. Specific populations are separate; historical/unverified sources remain inspectable. Word matches only order records within these gates.",
    }
    store_result(run_id, result, citations)
    event(
        run_id,
        result["status"],
        f"Saved {len(citations)} citations, {len(claims)} supported/structured claims and {len(conflicts)} potential conflicts.",
    )
    return result
