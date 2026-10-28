"""Deterministic evidence admission and ordering. Never a clinical certainty score."""

import hashlib, json, re
from datetime import date
from urllib.parse import urlparse
from .schemas import SourceDocument
from .scope import resolve_scope, condition_matches, population_tags, diabetes_types

POLICY_VERSION = "us-evidence-2026-10-27.v3"
ACTIVE_TRIAL_STATUSES = {
    "RECRUITING",
    "NOT_YET_RECRUITING",
    "ACTIVE_NOT_RECRUITING",
    "ENROLLING_BY_INVITATION",
}
TRIAL_CURRENCY_YEARS = 3  # Research-screening window, not a clinical evidence threshold.
RANKING_RULES = [
    {
        "criterion": "Source identity",
        "rule": "Canonical PMID/NCT and exact API origin; unverified identity is excluded.",
    },
    {
        "criterion": "Publication status",
        "rule": "Retracted records excluded; corrections and missing metadata flagged.",
    },
    {
        "criterion": "Question match",
        "rule": "Match the condition/subtype before ranking. Separate specific populations from the general overview; retain eligibility for inspection.",
    },
    {
        "criterion": "Evidence class",
        "rule": "Guideline, synthesis, randomized trial, other study; registries have a separate role.",
    },
    {
        "criterion": "Results and access",
        "rule": "Registry without results supports development only. Abstract-only limitations remain visible.",
    },
    {
        "criterion": "Dates",
        "rule": "Emerging activity requires an active interventional treatment trial updated within 3 years. Other records stay in the register; retrieval time never makes a study new.",
    },
    {
        "criterion": "Independent lineage",
        "rule": "Explicit NCT/DOI links identify shared families. Unknown overlap remains unknown.",
    },
]


def digest(data) -> str:
    return hashlib.sha256(json.dumps(data, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def resolve_pointer(data, pointer: str):
    node = data
    for token in pointer.lstrip("/").split("/"):
        token = token.replace("~1", "/").replace("~0", "~")
        node = node[int(token)] if isinstance(node, list) else node[token]
    return node


def class_info(doc: SourceDocument):
    types = {x.lower() for x in doc.publication_types}
    if doc.source == "clinicaltrials":
        return "Trial registry", 5
    if types & {"practice guideline", "guideline"}:
        return "Guideline publication", 0
    if types & {"meta-analysis", "systematic review"}:
        return "Evidence synthesis", 1
    if "randomized controlled trial" in types:
        return "Randomized trial", 2
    if any("clinical trial" in x for x in types):
        return "Clinical study", 3
    return "Published literature", 4


def identity_ok(doc: SourceDocument) -> bool:
    try:
        parsed = urlparse(doc.url)
        invalid_port = parsed.port is not None
    except ValueError:
        return False
    if not doc.verified or parsed.scheme != "https" or parsed.username or parsed.password or invalid_port:
        return False
    if doc.source == "pubmed":
        return bool(
            re.fullmatch(r"\d{1,10}", doc.canonical_id)
            and parsed.hostname == "pubmed.ncbi.nlm.nih.gov"
            and parsed.path == f"/{doc.canonical_id}/"
        )
    return bool(
        re.fullmatch(r"NCT\d{8}", doc.canonical_id)
        and parsed.hostname == "clinicaltrials.gov"
        and parsed.path == f"/study/{doc.canonical_id}"
    )


def rank_documents(
    documents: list[SourceDocument],
    condition: str,
    run_id: str,
    population: str = "general",
    as_of: date | None = None,
) -> list[dict]:
    scope = resolve_scope(condition, population, allow_ambiguous=True)
    as_of = as_of or date.today()
    unique = {}
    for doc in documents:
        unique.setdefault((doc.source, doc.canonical_id), doc)
    ranked = []
    terms = set(re.findall(r"\w+", condition.lower())) - {"of", "the", "and", "in"}
    for doc in unique.values():
        reasons = []
        excluded = not identity_ok(doc) or doc.retracted
        if not identity_ok(doc):
            reasons.append("SOURCE_IDENTITY_UNVERIFIED")
        if doc.retracted:
            reasons.append("RETRACTED_PUBLICATION")
        if doc.corrected:
            reasons.append("CORRECTION_REQUIRES_REVIEW")
        if doc.access_level == "abstract_only":
            reasons.append("ABSTRACT_ONLY")
        if not doc.published_date:
            reasons.append("PUBLICATION_DATE_UNKNOWN")
        if doc.source == "clinicaltrials" and not doc.has_results:
            reasons.append("REGISTRY_WITHOUT_RESULTS")
        if doc.jurisdiction != "US":
            reasons.append("US_APPLICABILITY_NOT_VERIFIED")
        evidence_class, priority = class_info(doc)
        snapshot_hash = digest(doc.snapshot)
        cid = "cit_" + digest([run_id, doc.source, doc.canonical_id])[:24]
        passages = []
        for passage in doc.passages:
            try:
                value = resolve_pointer(doc.snapshot, passage["locator"])
                if not isinstance(value, str) or value != passage["text"] or not value.strip():
                    continue
                passages.append(
                    {
                        "id": "ev_" + digest([cid, passage["locator"], snapshot_hash])[:30],
                        "citation_id": cid,
                        "locator": passage["locator"],
                        "text": value,
                        "content_hash": digest(value),
                    }
                )
            except (KeyError, ValueError, IndexError, TypeError):
                continue
        if not passages:
            reasons.append("NO_INSPECTABLE_PASSAGE")
        corpus = (doc.title + " " + " ".join(x["text"] for x in passages)).lower()
        relevance = sum(term in corpus for term in terms)
        if not condition_matches(
            scope,
            doc.title,
            doc.population.get("conditions", []),
            doc.population.get("inclusion_criteria", "")
            if doc.source == "clinicaltrials"
            else " ".join(x["text"] for x in passages),
        ):
            excluded = True
            reasons.append("CONDITION_MISMATCH")
        tags = (
            doc.population.get("tags", []) if doc.source == "clinicaltrials" else population_tags(doc.title)
        )
        if len(diabetes_types(" ".join(doc.population.get("conditions", [])) or doc.title)) > 1:
            tags = [*tags, "mixed_diabetes_types"]
        requested = set(scope["population"]) - {"general"}
        specific = bool(set(tags) - requested)
        if specific:
            reasons.append("SPECIFIC_POPULATION_SEPARATE")
        if requested and not requested <= set(tags):
            excluded = True
            reasons.append("REQUESTED_POPULATION_NOT_ESTABLISHED")
        bucket = "specific_population" if specific else "general"
        eligible_sections = ["care_landscape", "specific_populations"]
        if doc.source == "clinicaltrials":
            eligible_sections = ["emerging", "organizations", "specific_populations"]
            if doc.status not in ACTIVE_TRIAL_STATUSES:
                reasons.append("TRIAL_NOT_CURRENT_ACTIVE")
                bucket = "historical_or_unverified"
            if not doc.updated_date or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", doc.updated_date):
                reasons.append("TRIAL_CURRENCY_UNVERIFIED")
                bucket = "historical_or_unverified"
            else:
                try:
                    updated = date.fromisoformat(doc.updated_date)
                    if not 0 <= (as_of - updated).days <= 365 * TRIAL_CURRENCY_YEARS:
                        reasons.append("TRIAL_UPDATE_OUTSIDE_CURRENCY_WINDOW")
                        bucket = "historical_or_unverified"
                except ValueError:
                    reasons.append("TRIAL_CURRENCY_UNVERIFIED")
                    bucket = "historical_or_unverified"
            if doc.study_type != "INTERVENTIONAL" or doc.primary_purpose != "TREATMENT":
                reasons.append("NOT_VERIFIED_TREATMENT_TRIAL")
                bucket = "historical_or_unverified"
            if not doc.population.get("conditions") or not doc.population.get("eligibility_criteria"):
                reasons.append("TRIAL_POPULATION_UNVERIFIED")
                bucket = "historical_or_unverified"
            if bucket == "historical_or_unverified":
                eligible_sections = []
        if specific and eligible_sections:
            eligible_sections = ["specific_populations"]
        if excluded:
            bucket = "excluded"
            eligible_sections = []
        family = (
            ("nct:" + doc.nct_ids[0])
            if len(doc.nct_ids) == 1
            else ("doi:" + doc.doi.lower() if doc.doi else f"{doc.source}:{doc.canonical_id}")
        )
        basis = (
            "explicit_trial_identifier"
            if len(doc.nct_ids) == 1
            else "same_publication_only; underlying study overlap unknown"
        )
        allowed = (
            ["published_finding"]
            if doc.source == "pubmed" and passages
            else ["development", "organization"]
            if doc.source == "clinicaltrials" and passages
            else []
        )
        if (
            doc.has_results
            and passages
            and (doc.source == "pubmed" or any(e["locator"].startswith("/resultsSection/") for e in passages))
        ):
            allowed.append("efficacy")
        if excluded or not eligible_sections:
            allowed = []
        status = "excluded" if excluded else "limited"
        date_number = int(
            re.sub(r"\D", "", (doc.updated_date or doc.published_date or "0000")[:10]).ljust(8, "0")[:8]
        )
        bucket_priority = {
            "general": 0,
            "specific_population": 1,
            "historical_or_unverified": 2,
            "excluded": 3,
        }
        order = [
            bucket_priority[bucket],
            -relevance,
            priority,
            -int(doc.has_results),
            -date_number,
            doc.canonical_id,
        ]
        ranked.append(
            {
                **doc.model_dump(exclude={"snapshot", "passages"}),
                "id": cid,
                "snapshot_id": f"{doc.source}:{doc.canonical_id}:{snapshot_hash[:24]}",
                "snapshot_hash": snapshot_hash,
                "snapshot": doc.snapshot,
                "is_synthetic": bool(doc.snapshot.get("synthetic")),
                "evidence": passages,
                "evidence_class": evidence_class,
                "class_priority": priority,
                "relevance_terms_matched": relevance,
                "relevance_terms_total": len(terms),
                "family_id": family,
                "family_basis": basis,
                "allowed_claim_types": allowed,
                "decision": status,
                "scope": scope,
                "population_tags": tags,
                "display_bucket": bucket,
                "eligible_sections": eligible_sections,
                "reason_codes": reasons,
                "policy_version": POLICY_VERSION,
                "ordering": order,
            }
        )
    ranked.sort(key=lambda x: tuple(x["ordering"]))
    families = {}
    for i, item in enumerate(ranked, 1):
        item["rank"] = i
        item["family_count"] = sum(x["family_id"] == item["family_id"] for x in ranked)
        item["duplicate_of"] = families.get(item["family_id"])
        families.setdefault(item["family_id"], item["id"])
    return ranked


def validate_claim(candidate: dict, citations: list[dict]) -> tuple[bool, list[str], list[dict]]:
    reasons = []
    refs = []
    by_evidence = {e["id"]: (c, e) for c in citations for e in c["evidence"]}
    if candidate["claim_type"] in {"current_care", "approval"}:
        reasons.append("REGISTERED_GUIDELINE_OR_REGULATORY_EVIDENCE_REQUIRED")
    if re.search(
        r"\b(?:FDA[- ]approved|standard of care|recommended first[- ]line)\b", candidate["text"], re.I
    ):
        reasons.append("UNVERIFIED_REGULATORY_OR_CARE_LANGUAGE")
    if re.search(r"\b(?:you should|patients should|prescribe|start taking)\b", candidate["text"], re.I):
        reasons.append("PATIENT_RECOMMENDATION_OUT_OF_SCOPE")
    for ref in candidate["references"]:
        pair = by_evidence.get(ref["evidence_id"])
        if not pair:
            reasons.append("UNKNOWN_EVIDENCE_ID")
            continue
        citation, evidence = pair
        if citation["decision"] == "excluded":
            reasons.append("EXCLUDED_SOURCE")
        if candidate["claim_type"] not in citation["allowed_claim_types"]:
            reasons.append("CLAIM_TYPE_NOT_PERMITTED")
        if candidate["section"] not in citation.get("eligible_sections", []):
            reasons.append("SECTION_SCOPE_NOT_PERMITTED")
        if candidate["section"] == "emerging" and candidate["claim_type"] != "development":
            reasons.append("EMERGING_REQUIRES_DEVELOPMENT_CLAIM")
        if candidate["section"] == "organizations" and candidate["claim_type"] != "organization":
            reasons.append("ORGANIZATIONS_REQUIRE_DOCUMENTED_ROLE")
        if ref["quote"] not in evidence["text"]:
            reasons.append("QUOTE_NOT_IN_SNAPSHOT")
        refs.append(
            {
                **ref,
                "citation_id": citation["id"],
                "locator": evidence["locator"],
                "snapshot_hash": citation["snapshot_hash"],
            }
        )
    if not refs:
        reasons.append("NO_VALID_REFERENCE")
    if candidate["claim_type"] == "organization":
        role_evidence = {
            e["id"]
            for c in citations
            for e in c["evidence"]
            if any(role["locator"] == e["locator"] for role in c["organization_roles"])
        }
        if not any(r["evidence_id"] in role_evidence for r in refs):
            reasons.append("DOCUMENTED_ORGANIZATION_ROLE_REQUIRED")
    return not reasons, list(dict.fromkeys(reasons)), refs


def find_conflicts(claims: list[dict], citations: list[dict]) -> list[dict]:
    """Potential opposite findings only when intervention/population/outcome explicitly match."""
    conflicts = []
    family = {c["id"]: c["family_id"] for c in citations}

    def normalize(s):
        return " ".join(re.findall(r"\w+", s.lower()))

    for i, a in enumerate(claims):
        for b in claims[i + 1 :]:
            key_a = tuple(normalize(a.get(k, "")) for k in ["intervention", "population", "outcome"])
            key_b = tuple(normalize(b.get(k, "")) for k in ["intervention", "population", "outcome"])
            if (
                not all(key_a)
                or any(x in {"unknown", "not specified", "unspecified"} for x in key_a)
                or key_a != key_b
            ):
                continue
            if {a["direction"], b["direction"]} != {"positive", "negative"}:
                continue
            a_f = {family[r["citation_id"]] for r in a["references"]}
            b_f = {family[r["citation_id"]] for r in b["references"]}
            conflicts.append(
                {
                    "id": "conf_" + digest([a["id"], b["id"]])[:24],
                    "claim_ids": [a["id"], b["id"]],
                    "citation_ids": list(
                        dict.fromkeys([r["citation_id"] for r in a["references"] + b["references"]])
                    ),
                    "type": "within_study_disagreement" if a_f & b_f else "potential_opposing_findings",
                    "summary": f"Opposite extracted findings for {a['intervention']} / {a['outcome']}. Both accounts are preserved; no winner is selected.",
                    "resolution": "Analyst review required: compare population, comparator, endpoint, follow-up and source dates.",
                    "status": "unresolved",
                    "review_needed": True,
                }
            )
    return conflicts
