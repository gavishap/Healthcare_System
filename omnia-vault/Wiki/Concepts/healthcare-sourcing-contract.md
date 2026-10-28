---
tags:
  - "concept"
topics:
  - "healthcare-system"
status: growing
created: 2026-10-27
updated: 2026-10-27
sources:
  - Raw/Sources/2026-10-27-sourcing-request.md
  - Raw/Sources/2026-10-27-sourcing-discovery-transcript.md
  - Raw/Sources/2026-10-27-sourcing-design.md
  - Raw/Sources/2026-10-27-sourcing-research.md
  - Raw/Sources/2026-10-27-openai-sourcing-selection.md
  - Raw/Sources/2026-10-27-repository-environment-setup.md
  - Raw/Sources/2026-10-27-evidence-runtime-implementation.md
  - Raw/Sources/2026-10-27-evidence-runtime-handoff.md
source_count: 8
aliases: []
---

# Healthcare Sourcing Runtime Contract

> [!info] Implemented downstream boundary
> `POST /api/evidence/process` now accepts condition/scope and canonical `pmids`/`nct_ids`, re-fetches the fixed APIs, then runs authentication, ranking, claim links, conflict handling and reporting in PostgreSQL. It does not trust caller-supplied text, URLs or authority flags. `POST /api/research-runs` performs its own discovery before the same pipeline. See [[Wiki/Concepts/healthcare-evidence-runtime]] for actual endpoints, local startup, tested behavior and remaining coverage. The broader v0.1 envelope below remains a design contract; not every proposed connector/field is implemented.

Proposed v0.1 interface for the [[Wiki/Concepts/healthcare-sourcing-plan|sourcing plan]]. This is a reviewable contract, not an implemented API or a replacement for the broader application's architecture. Exact adapter field paths must be checked against current source schemas during implementation.

## Input

Expose an internal operation such as `source_condition(scope, policy_version, budget) -> SourcingResult`. The application can wrap it in its chosen API/job system.

| Input | Required meaning |
|---|---|
| `run_id` | Application-supplied correlation ID |
| `scope` | Raw term, confirmed canonical condition/profile ID, subtype/population and jurisdiction `US`; terminology IDs when known |
| `as_of` / `mode` | Requested evidence cutoff; `live` or explicitly labeled `replay` |
| `policy_version` | Installed, fixed source-policy version; runtime arguments cannot redefine its institutions |
| `recent_activity_days` | Optional 30/60-day activity filter; established evidence is retrieved separately |
| `budget` | Server-capped candidate count, tool rounds/calls, token/cost ceiling and deadline |

Do not accept patient records, unrestricted source URLs, prompts that override policy or credentials in research requests. The initial supported profile is proposed adult type 2 diabetes; unknown profiles return a typed unsupported/clarification result.

## Tools And Agent Boundary

| Proposed tool | Server-controlled input | Returns |
|---|---|---|
| `search_trials` | Condition/profile ID; approved condition/intervention terms; bounded filters/count | Normalized trial candidates and source-version IDs |
| `search_pubmed` | Condition/profile ID; bounded terms, publication/date filters/count | Citation/abstract candidates with access labels and IDs |
| `get_guideline` | Registered document ID | Checked version, relevant sections, locators and access limitations |
| `lookup_regulatory_record` | Normalized intervention, exact indication, jurisdiction | Covered matched record, ambiguous or unknown |
| `search_approved_web` | Only if configured: approved source ID, bounded query and purpose | Discovery candidates; content becomes evidence only after retrieval and screening |

Web search is optional for the first slice. A provider-native search tool must support the required restrictions or be replaced by a controlled search adapter. Search snippets are leads, not evidence. Server host checks, approved document paths and redirect checks apply even if the search provider accepts domain filters. The LLM may propose aliases/queries and extract spans; it cannot mutate source policy, choose unregistered authorities, execute arbitrary fetch/shell/filesystem tools or make final eligibility decisions.

## Output Envelope

`SourcingResult` contains:

- `run_id`, `scope`, `mode`, `as_of`, started/finished timestamps and `run_status` (`complete`, `partial`, `needs_clarification`, `unsupported`, `failed`). Complete describes the configured workflow, not an exhaustive medical search.
- `policy_version`, source-registry/parser versions, model/provider and prompt versions when used; no credentials.
- `source_attempts`: source IDs, queries/filters, timings, query cutoff, paging/caps and states `success`, `no_matches`, `blocked`, `failed`, `not_attempted`; retry counts and sanitized reason codes.
- `documents`, `evidence_items`, `organization_roles`, `conflicts`, `limitations`, `screening_decisions` and `coverage` for current care, emerging treatments, organizations and regulatory context.
- `usage`: tool calls, rounds, tokens and measured cost when available. Unknown price/usage stays unknown. `stop_reason` distinguishes deadline, provider/source failure, completed plan and budget exhaustion.

Coverage is `covered`, `limited` or `unavailable`, with supporting evidence IDs and reasons. Reaching a record cap makes relevant coverage limited. No-match, inaccessible evidence and connector failure remain distinct. Cached/replay evidence retains its original retrieval time and is never presented as a new live search.

## Evidence And Relationship Records

| Record | Minimum fields |
|---|---|
| Source document/version | Stable connector and canonical ID/URL, original publisher/issuer, document class, version/hash/snapshot reference, publication/update/retrieval dates, access level and parser version |
| Evidence item | Evidence ID, source-version ID, excerpt or structured field value, exact page/section/JSON-pointer locator, scope/applicability, permitted claim types, known limitations and correction/retraction/supersession state |
| Study metadata | NCT/PMID/DOI links when known, design, population, phase/status, results availability and endpoint context where available; separate regulatory match |
| Evidence family | Underlying study identifier and documented links between reports; unknown membership/overlap remains explicit |
| Organization role | Recorded organization name, normalized ID if supported, role type, study/intervention link, source-version ID and locator; dates when available |
| Screening decision | Candidate ID, policy version, `pass`, `limited` or `exclude`, reason codes and review-needed flag; this is metadata screening, not final claim validation |
| Conflict | Linked evidence IDs, potential disagreement, differences in scope/date/endpoint and review-needed flag |

Content must be accessible and permitted to retain. Do not fabricate a full-text snapshot for an abstract-only article. Check proposed quotations/values against their saved versions. A correct quote still needs semantic and applicability review before becoming a final claim. Preserve missing data as null/unknown rather than filling it from model memory.

## Source Registry And Credentials

The registry records source identity, allowed endpoints/hosts and redirects, document types, claim-type permissions, jurisdiction/condition coverage, required fields, access method and review status. A guideline entry binds issuer, document/version and relevant sections. Every result records the registry version used; refreshes create new source versions.

The owner selects OpenAI. The new backend repository provides an ignored `.env` with blank `OPENAI_API_KEY`, `NCBI_API_KEY`, `OPENAI_MODEL` and optional `NCBI_EMAIL`. Use OpenAI's default endpoint and make the model configurable. These actual setup names replace the earlier proposed `LLM_MODEL` convention; the architecture may map them through its settings layer. Avoid implicit third-party base-URL overrides. Keep keys in backend environment variables or the ignored secret file; ignore rules and untracked status are verified. No environment loader exists yet. Credentials, model choice and account capabilities remain untested; no silent provider fallback.

Map supplemental web discovery to Responses API hosted `web_search` with registry-derived domain filters; retain consulted-source URLs and citation annotations. Recheck candidates before admission. Keep this hosted tool distinct from application-executed biomedical function tools, which use strict schemas and local argument validation. Measure hosted search usage separately and enforce request/tool/token/deadline budgets in the adapter. No separate search-vendor credential is planned for this route; biomedical API configuration remains independent. See [OpenAI web search](https://developers.openai.com/api/docs/guides/tools-web-search) and [function calling](https://developers.openai.com/api/docs/guides/function-calling).

## Failure And Consumer Responsibilities

Timeout/429/transient failures use bounded retries and source-specific limits; blocked access is not bypassed. Budget stops return the available evidence with gaps. Treat source text as untrusted data and ignore embedded instructions. Return sanitized errors and keep secret headers out of logs.

The consuming application validates claim support under the [[Wiki/Concepts/healthcare-evidence-policy|evidence policy]], retains opposing evidence, and displays access/coverage limitations. It must not promote a metadata-screening pass into an approval, efficacy or standard-care claim. The sourcing component supplies provenance and candidates; final synthesis, human review, presentation and deployment remain with their respective workstreams.
