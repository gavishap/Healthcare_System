---
Title: "Evidence Desk implementation and verification record"
Reference: "Local backend/frontend repositories, automated checks and sanitized live API results captured 2026-10-27"
ContentType:
  - "markdown"
Created: 2026-10-27
Processed: true
tags:
  - "source"
---

# Implemented Evidence Pipeline

Original engineering record. This documents observed implementation behavior, not clinical validation or a medical literature review. Application code belongs in the separate `backend/` and `frontend/` repositories, not this vault.

## Actual Runtime

- FastAPI/Pydantic API, React/TypeScript/Vite interface, PostgreSQL 17 storage and Docker Compose. Local ports are 5173 for the interface, 8000 for API and 55432 for Postgres. All published ports bind to loopback. PostgreSQL uses a named volume; other existing services/databases were left in place.
- Backend settings explicitly load the ignored `.env`. OpenAI and NCBI keys were present and used successfully. No credential values are captured in source notes, fixtures, frontend or build contexts. OpenAI's official base URL is explicit; there is no implicit provider swap. Blank model configuration resolves to `gpt-4.1-mini`.
- Direct PubMed ESearch/EFetch via NCBI and ClinicalTrials.gov API v2 are implemented. PubMed discovery filters guideline/review/meta-analysis/randomized-trial publication types and sorts by publication date. Trial discovery filters active development/recruitment states and sorts by last update. Queries, filters, dates, failures and caps remain visible. These are bounded searches, not comprehensive clinical reviews.
- Upstream integration: `POST /api/evidence/process` takes condition/scope and canonical PMID/NCT identifiers, then re-fetches authoritative records. Caller-supplied source URLs, abstracts or authority flags are not accepted. `POST /api/research-runs` performs fixed-source discovery and the same downstream processing itself.

## Citation Controls

- Canonical source ID/host verification; no recursive citation chasing or arbitrary URL fetch. Retractions and mismatched identities are excluded, corrections/access/applicability limitations are flagged.
- Deterministic ordering: admission, condition-term match, evidence class, results availability, source date and stable ID. This is research priority, not a probability of truth or a treatment leaderboard. Awards, popularity, years in business and model agreement do not establish authority.
- Snapshots are immutable, content-hashed JSON records. Evidence passages have exact JSON-pointer locators and source-version links. Claims retain evidence IDs, exact quotations, source IDs, hashes and a support-check result. PostgreSQL foreign keys connect these records.
- Explicit NCT identifiers group evidence families; DOI links identify a publication. Unknown underlying study overlap remains unknown. Concurrent runs admit a shared snapshot atomically without overwriting it.
- Models cannot approve policy, source identity or clinical authority. One real strict `get_evidence_passages` function call reads selected saved evidence; schema-constrained extraction and a separate automated semantic review follow. At most three model requests are made, with bounded text/output/record/time limits and no hidden retry/provider escalation.
- Exact quote/reference checks are separate from semantic review. Unknown IDs, altered quotes, excluded sources and unsupported claim types are rejected. Uncited model limitation notes are withheld instead of becoming uncited clinical conclusions in the report. That tightened behavior is recorded as policy `us-evidence-2026-10-27.v2`; earlier run versions remain historical.
- Potential conflicts are detected when accepted opposing findings explicitly match intervention, population and outcome. Both findings and their sources remain visible, unresolved, with analyst review required. This exact-match detector can miss synonyms and nuanced contradictions; no detected conflict is not consensus.

## Interface And Export

The interface offers condition/scope confirmation, actual stage events, saved research, a three-section briefing, citation register, source/evidence drawer, conflict view, fixed policy explanation and Markdown/JSON exports. Exports retain source IDs, quotations, locators, snapshot hashes, source dates and the run's actual policy version. External text is escaped as text. Synthetic examples are conspicuously labeled; fictional source IDs are not linked as real publications. Saved runs can be opened by a `run` query parameter.

Applied the vault's UI/UX Pro Max skill. The initial health/wellness marketing result did not fit; a narrower internal-analytics search supplied useful dashboard/accessibility guidance. The application's deliberate fallback design is recorded in frontend `DESIGN.md`. Fonts are self-hosted, controls are semantic, native dialog focus/Escape behavior is used, and reduced motion is respected.

## Verification Observed

- 20 automated backend tests pass against actual PostgreSQL. Coverage includes exact quotes/IDs, retractions, lookalike hosts, current-care/approval gates, source locators, duplicate study families, opposing findings, input restrictions, parser behavior, FK provenance, source-ID-only integration, optional application-token authentication, safe report rendering, bounded model inputs, concurrent snapshot admission and withholding uncited model conclusions.
- Production frontend builds and Docker image builds pass. Browser checks pass for the citation register, evidence drawer/hash/locators, Escape, cited Markdown export, policy view, synthetic opposing claims, absence of false original-source links, 375px phone and landscape widths, reduced motion and absence of browser runtime errors. Desktop/mobile screenshots are local ignored artifacts under frontend `data/`.
- The final policy-v2 live API run `546eeb36-85e5-4293-821c-8ad79bdcb224` uses type 2 diabetes as the research example. It retrieves four PubMed records and four ClinicalTrials.gov records, saves ten accepted/structured claims, withholds three candidate claims, and records one executed evidence tool call across three model requests. No conflict is detected in that bounded extraction. This is an integration observation, not a medical accuracy rate.
- The final live result is `partial` because a checked applicable US guideline is absent and result caps are reached. All model limitation notes without references are withheld. The synthetic policy run separately demonstrates preserving two opposing claims and one unresolved conflict without making medical assertions about a real treatment.
- Actual configured key values are absent from candidate tracked code and frontend builds; real environment files remain untracked. The API supports an optional local application bearer token, which is separate from upstream keys and is not tenant identity.

## Remaining Limits

No checked current US guideline or FDA adapter is implemented in this slice. Standard-of-care and approval claims are withheld. PubMed access is abstract-only where available; study applicability and scientific correctness require expert review. Model support review is probabilistic. User identity/tenants, durable distributed workers, production migrations/backup governance, hosted web-search discovery and clinical policy approval remain future work. Restart marks unfinished local jobs interrupted. No stakeholder slide or external publication/push is performed by this implementation.

Implementation uses current official references: [OpenAI structured outputs](https://developers.openai.com/api/docs/guides/structured-outputs), [function calling](https://developers.openai.com/api/docs/guides/function-calling), [Python SDK](https://github.com/openai/openai-python), [SQLAlchemy Postgres/psycopg](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html). Public documentation does not substitute for the actual service checks recorded above.
