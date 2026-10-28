"""Fixed-host public connectors. Credentials never enter snapshots, errors or source URLs."""

import asyncio, re, time
from defusedxml import ElementTree as ET
import httpx
from .config import get_settings
from .schemas import SourceDocument, utcnow
from .scope import resolve_scope, trial_population


class SourceFailure(Exception):
    def __init__(self, code: str):
        self.code = code


def text(node) -> str:
    return "".join(node.itertext()).strip() if node is not None else ""


def pub_date(article) -> str | None:
    for path in [".//ArticleDate", ".//JournalIssue/PubDate"]:
        node = article.find(path)
        if node is not None:
            year = node.findtext("Year")
            if not year:
                m = re.search(r"\b(19|20)\d{2}\b", node.findtext("MedlineDate", ""))
                if m:
                    return m.group(0)
                continue
            month = node.findtext("Month")
            day = node.findtext("Day")
            if month and month.isdigit():
                return f"{year}-{int(month):02d}" + (f"-{int(day):02d}" if day and day.isdigit() else "")
            return year
    return None


def parse_pubmed(xml: str, retrieved_at: str) -> list[SourceDocument]:
    root = ET.fromstring(xml)
    docs = []
    for item in root.findall(".//PubmedArticle"):
        pmid = item.findtext("./MedlineCitation/PMID", "")
        if not re.fullmatch(r"\d{1,10}", pmid):
            continue
        title = text(item.find(".//ArticleTitle"))
        abstract = [
            {"label": n.get("Label", "Abstract"), "text": text(n)}
            for n in item.findall(".//Abstract/AbstractText")
            if text(n)
        ]
        ids = {n.get("IdType"): text(n) for n in item.findall(".//ArticleId")}
        types = [text(n) for n in item.findall(".//PublicationType")]
        comments = [n.get("RefType", "") for n in item.findall(".//CommentsCorrections")]
        authors = [
            " ".join(filter(None, [n.findtext("ForeName"), n.findtext("LastName")]))
            or n.findtext("CollectiveName", "")
            for n in item.findall(".//AuthorList/Author")
        ]
        all_text = " ".join(x["text"] for x in abstract)
        ncts = sorted(
            set(
                re.findall(
                    r"\bNCT\d{8}\b",
                    all_text + " " + " ".join(text(n) for n in item.findall(".//AccessionNumber")),
                )
            )
        )
        snapshot = {
            "pmid": pmid,
            "title": title,
            "abstract": abstract,
            "publication_types": types,
            "authors": authors,
            "journal": text(item.find(".//Journal/Title")),
            "identifiers": ids,
            "publication_date": pub_date(item),
            "comments": comments,
            "xml": ET.tostring(item, encoding="unicode"),
        }
        passages = [{"locator": f"/abstract/{i}/text", "text": a["text"]} for i, a in enumerate(abstract)]
        docs.append(
            SourceDocument(
                source="pubmed",
                canonical_id=pmid,
                url=f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
                title=title,
                published_date=snapshot["publication_date"],
                retrieved_at=retrieved_at,
                publication_types=types,
                doi=ids.get("doi"),
                nct_ids=ncts,
                journal=snapshot["journal"],
                authors=authors,
                has_results=any(
                    x["label"].lower() in {"results", "findings", "results and conclusions"} for x in abstract
                ),
                retracted="Retracted Publication" in types or "RetractionIn" in comments,
                corrected="ErratumIn" in comments or "UpdateIn" in comments,
                access_level="abstract_only" if abstract else "metadata_only",
                snapshot=snapshot,
                passages=passages,
            )
        )
    return docs


def parse_trial(study: dict, retrieved_at: str) -> SourceDocument:
    protocol = study.get("protocolSection", {})
    identity = protocol.get("identificationModule", {})
    nct = identity.get("nctId", "")
    if not re.fullmatch(r"NCT\d{8}", nct):
        raise SourceFailure("INVALID_NCT_RECORD")
    desc = protocol.get("descriptionModule", {})
    status = protocol.get("statusModule", {})
    design = protocol.get("designModule", {})
    sponsor = protocol.get("sponsorCollaboratorsModule", {})
    passages = []

    def passage(pointer, value):
        if isinstance(value, str) and value.strip():
            passages.append({"locator": pointer, "text": value})

    passage("/protocolSection/identificationModule/briefTitle", identity.get("briefTitle"))
    passage("/protocolSection/descriptionModule/briefSummary", desc.get("briefSummary"))
    passage("/protocolSection/statusModule/overallStatus", status.get("overallStatus"))
    passage("/protocolSection/identificationModule/officialTitle", identity.get("officialTitle"))
    passage(
        "/protocolSection/statusModule/lastUpdatePostDateStruct/date",
        status.get("lastUpdatePostDateStruct", {}).get("date"),
    )
    passage(
        "/protocolSection/eligibilityModule/eligibilityCriteria",
        protocol.get("eligibilityModule", {}).get("eligibilityCriteria"),
    )
    for field in ["minimumAge", "maximumAge", "sex"]:
        passage(
            f"/protocolSection/eligibilityModule/{field}", protocol.get("eligibilityModule", {}).get(field)
        )
    for i, condition in enumerate(protocol.get("conditionsModule", {}).get("conditions", [])):
        passage(f"/protocolSection/conditionsModule/conditions/{i}", condition)
    interventions = protocol.get("armsInterventionsModule", {}).get("interventions", [])
    for i, intervention in enumerate(interventions):
        passage(f"/protocolSection/armsInterventionsModule/interventions/{i}/name", intervention.get("name"))
    for i, location in enumerate(protocol.get("contactsLocationsModule", {}).get("locations", [])):
        passage(f"/protocolSection/contactsLocationsModule/locations/{i}/country", location.get("country"))
    roles = []
    lead = sponsor.get("leadSponsor", {})
    if lead.get("name"):
        pointer = "/protocolSection/sponsorCollaboratorsModule/leadSponsor/name"
        passage(pointer, lead["name"])
        roles.append(
            {
                "name": lead["name"],
                "role": "lead_sponsor",
                "locator": pointer,
                "study_id": nct,
                "organization_class": lead.get("class", "UNKNOWN"),
            }
        )
    for i, collaborator in enumerate(sponsor.get("collaborators", [])):
        if collaborator.get("name"):
            pointer = f"/protocolSection/sponsorCollaboratorsModule/collaborators/{i}/name"
            passage(pointer, collaborator["name"])
            roles.append(
                {
                    "name": collaborator["name"],
                    "role": "collaborator",
                    "locator": pointer,
                    "study_id": nct,
                    "organization_class": collaborator.get("class", "UNKNOWN"),
                }
            )
    return SourceDocument(
        source="clinicaltrials",
        canonical_id=nct,
        url=f"https://clinicaltrials.gov/study/{nct}",
        title=identity.get("officialTitle") or identity.get("briefTitle", nct),
        published_date=status.get("studyFirstSubmitDate"),
        updated_date=status.get("lastUpdatePostDateStruct", {}).get("date"),
        retrieved_at=retrieved_at,
        phase=", ".join(design.get("phases", [])) or None,
        status=status.get("overallStatus"),
        has_results=bool(study.get("hasResults") or study.get("resultsSection")),
        nct_ids=[nct],
        access_level="registry_record",
        snapshot=study,
        passages=passages,
        organization_roles=roles,
        population=trial_population(protocol),
        study_type=design.get("studyType"),
        primary_purpose=design.get("designInfo", {}).get("primaryPurpose"),
        interventions=interventions,
    )


class Sources:
    def __init__(self):
        self.settings = get_settings()
        self.client = httpx.AsyncClient(
            timeout=self.settings.source_timeout_seconds,
            follow_redirects=False,
            headers={"User-Agent": "HealthcareEvidencePrototype/0.1", "Accept": "application/json"},
        )
        self.ncbi_lock = asyncio.Lock()
        self.last_ncbi = 0.0

    async def close(self):
        await self.client.aclose()

    async def request(self, url, *, params=None, data=None, ncbi=False):
        for attempt in range(2):
            try:
                if ncbi:
                    async with self.ncbi_lock:
                        # Conservative 3 rps even when an API key exists.
                        await asyncio.sleep(max(0, 0.36 - (time.monotonic() - self.last_ncbi)))
                        self.last_ncbi = time.monotonic()
                        response = (
                            await self.client.post(url, data=data)
                            if data
                            else await self.client.get(url, params=params)
                        )
                else:
                    response = await self.client.get(url, params=params)
                if response.status_code in {429, 500, 502, 503, 504} and attempt == 0:
                    retry = response.headers.get("retry-after", "1")
                    try:
                        delay = float(retry)
                    except ValueError:
                        delay = 1.0
                    if delay > 4:
                        raise SourceFailure("RETRY_AFTER_EXCEEDS_BUDGET")
                    await asyncio.sleep(max(0.5, delay))
                    continue
                if response.status_code >= 400 or response.is_redirect:
                    raise SourceFailure(
                        "SOURCE_AUTHENTICATION_FAILED"
                        if response.status_code in {401, 403}
                        else f"UPSTREAM_HTTP_{response.status_code}"
                    )
                if len(response.content) > 4_000_000:
                    raise SourceFailure("RESPONSE_SIZE_LIMIT")
                return response
            except (httpx.TimeoutException, httpx.NetworkError):
                if attempt == 0:
                    continue
                raise SourceFailure("SOURCE_NETWORK_UNAVAILABLE") from None
        raise SourceFailure("RETRY_LIMIT")

    def ncbi_params(self):
        params = {"tool": "healthcare_evidence_prototype"}
        if self.settings.ncbi_api_key.get_secret_value():
            params["api_key"] = self.settings.ncbi_api_key.get_secret_value()
        if self.settings.ncbi_email:
            params["email"] = self.settings.ncbi_email
        return params

    async def pubmed(
        self, condition: str, count: int, ids: list[str] | None = None, populations: list[str] | None = None
    ):
        explicit_ids = ids is not None
        if count <= 0 or ids == []:
            return [], {
                "source": "pubmed",
                "status": "not_attempted",
                "reason": "No identifiers requested or source budget exhausted.",
            }
        focus = f'"{condition}"[Title/Abstract]'
        if resolve_scope(condition, allow_ambiguous=True)["condition_key"] == "type_2_diabetes":
            focus = '("type 2 diabetes"[Title] OR "diabetes mellitus, type 2"[Title] OR T2DM[Title])'
        term = (
            f"{focus} AND humans[MeSH Terms] AND "
            '("Practice Guideline"[Publication Type] OR "Guideline"[Publication Type] OR '
            '"Systematic Review"[Publication Type] OR "Meta-Analysis"[Publication Type] OR '
            '"Randomized Controlled Trial"[Publication Type])'
        )
        if populations:
            term += " AND " + " AND ".join(f'"{p.replace("_", " ")}"[Title/Abstract]' for p in populations)
        capped = ids is not None and len(ids) > count
        if ids is None:
            search = await self.request(
                "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi",
                data={
                    **self.ncbi_params(),
                    "db": "pubmed",
                    "term": term,
                    "retmax": count,
                    "retmode": "json",
                    "sort": "pubdate",
                },
                ncbi=True,
            )
            result = search.json().get("esearchresult", {})
            if "ERROR" in search.text or result.get("errorlist"):
                raise SourceFailure("NCBI_QUERY_REJECTED")
            ids = result.get("idlist", [])
            capped = int(result.get("count", 0)) > len(ids)
        if not ids:
            return [], {
                "source": "pubmed",
                "status": "no_matches",
                "query": term,
                "cap": count,
                "truncated": False,
            }
        response = await self.request(
            "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi",
            data={**self.ncbi_params(), "db": "pubmed", "id": ",".join(ids[:count]), "retmode": "xml"},
            ncbi=True,
        )
        try:
            docs = parse_pubmed(response.text, utcnow().isoformat())
        except Exception:
            raise SourceFailure("NCBI_RECORD_PARSE_FAILED") from None
        return docs, {
            "source": "pubmed",
            "status": "success" if docs else "no_matches",
            "query": None if explicit_ids else term,
            "identifiers": ids[:count] if explicit_ids else None,
            "sort": None if explicit_ids else "publication_date_descending",
            "retrieved": len(docs),
            "cap": count,
            "truncated": capped,
            "retrieved_at": utcnow().isoformat(),
        }

    async def trials(
        self, condition: str, count: int, ids: list[str] | None = None, populations: list[str] | None = None
    ):
        if count <= 0 or ids == []:
            return [], {
                "source": "clinicaltrials",
                "status": "not_attempted",
                "reason": "No identifiers requested or source budget exhausted.",
            }
        params = {"format": "json", "pageSize": count}
        if ids:
            params["filter.ids"] = ",".join(ids[:count])
        else:
            params["query.cond"] = condition
            params["sort"] = "LastUpdatePostDate:desc"
            params["filter.advanced"] = (
                "AREA[StudyType]INTERVENTIONAL AND AREA[DesignPrimaryPurpose]TREATMENT"
            )
            params["filter.overallStatus"] = (
                "RECRUITING,NOT_YET_RECRUITING,ACTIVE_NOT_RECRUITING,ENROLLING_BY_INVITATION"
            )
            if populations:
                params["query.term"] = " AND ".join(p.replace("_", " ") for p in populations)
        response = await self.request("https://clinicaltrials.gov/api/v2/studies", params=params)
        try:
            result = response.json()
            docs = [parse_trial(s, utcnow().isoformat()) for s in result.get("studies", [])]
        except Exception:
            raise SourceFailure("TRIAL_RECORD_PARSE_FAILED") from None
        return docs, {
            "source": "clinicaltrials",
            "status": "success" if docs else "no_matches",
            "query": condition,
            "filters": {k: v for k, v in params.items() if k not in {"format", "pageSize"}},
            "retrieved": len(docs),
            "cap": count,
            "truncated": bool(result.get("nextPageToken")) or (ids is not None and len(ids) > count),
            "retrieved_at": utcnow().isoformat(),
        }

    async def collect(self, condition, count, pmids=None, nct_ids=None, population="general"):
        scope = resolve_scope(condition, population)
        populations = [p for p in scope["population"] if p != "general"]

        async def guarded(source, fn):
            try:
                return await fn
            except SourceFailure as exc:
                return [], {"source": source, "status": "failed", "reason": exc.code}
            except Exception:
                return [], {"source": source, "status": "failed", "reason": "SOURCE_ADAPTER_ERROR"}

        explicit = pmids is not None or nct_ids is not None
        n_pub = min(len(pmids or []), count) if explicit else max(2, count // 2)
        n_trial = min(len(nct_ids or []), count - n_pub) if explicit else count - n_pub
        results = await asyncio.gather(
            guarded(
                "pubmed", self.pubmed(scope["condition"], n_pub, pmids if explicit else None, populations)
            ),
            guarded(
                "clinicaltrials",
                self.trials(scope["condition"], n_trial, nct_ids if explicit else None, populations),
            ),
        )
        return [d for docs, _ in results for d in docs], [
            {**attempt, "scope": scope} for _, attempt in results
        ]
