---
tags:
  - "concept"
topics:
  - "healthcare-system"
status: growing
created: 2026-10-27
updated: 2026-10-27
sources:
  - Raw/Sources/2026-10-27-architecture-analysis.md
  - Raw/Sources/2026-10-27-discovery-transcript.md
  - Raw/Sources/2026-10-27-prototype-challenge.md
  - Raw/Sources/2026-10-27-architecture-research.md
  - Raw/Sources/2026-10-27-sourcing-discovery-transcript.md
  - Raw/Sources/2026-10-27-sourcing-request.md
  - Raw/Sources/2026-10-27-sourcing-design.md
  - Raw/Sources/2026-10-27-openai-sourcing-selection.md
source_count: 8
aliases: []
---

# Healthcare Open Questions

> [!info] Source and decision status
> The interview and PDF establish requirements; the authored design and researched documentation support the proposals. Technical choices remain proposed until adopted.

## Decisions Still Open

| Question | Working recommendation | Why it matters |
|---|---|---|
| Actual time remaining? | Re-budget the 120-minute plan before build | The transcript is not a live timer |
| First condition and subtype? | One well-covered supported condition | Determines guideline availability and test cases |
| Applicable current guideline and access rights? | Manually checked source registry entry | Critical dependency for standard-care section |
| Who validates policy and claims for actual operation? | Name a domain reviewer; prototype exercise assumes client validation only | Engineering facets are not clinical grading; the exercise assumption is not actual approval |
| OpenAI model, credentials and account search capabilities? | Responses API, backend key and startup capability probe | Provider is selected; key/model and real hosted-search access remain untested |
| Fastest proven scaffold? | FastAPI/React preferred; Streamlit deadline fallback | No transcript evidence establishes framework speed |
| Auth/tenant/retention requirements? | Local single-user demo, define before pilot | Changes access/storage/operations requirements |
| Budget, run targets and refresh schedule? | Bounded configurable requests; measure first | No reliable cost/latency baseline yet |
| Which organizations and roles matter? | Sponsor/collaborator/applicant/affiliation separately | Ownership and commercial claims need additional evidence |
| Repository sharing destination? | Separate application repository later | Template origin must not receive project material |
| Should future chats be shared? | Only with explicit scope and redaction | Optional in transcript; not authorized now |

These questions do not block the present strategy and notes. They block unsupported claims of production readiness or comprehensive medical coverage. Proposed defaults are not client agreements.

## Resolved By The Extended Interview

U.S. jurisdiction is explicit, not an outstanding assumption. PubMed and clinical-trials records are the named starting points; authority stays in a fixed source policy. The interviewer permits assuming client validation for the prototype. The [[Wiki/Concepts/healthcare-sourcing-plan|sourcing draft]] proposes adult type 2 diabetes with an ADA guideline anchor and targeted FDA checks; that condition/guideline selection and real operational review remain open.

The owner's follow-up selects OpenAI. The sourcing plan uses Responses API hosted search for supplemental discovery; the model, credential, budget and actual account capability checks remain open.

## Evidence That Reopens The Architecture

- Guideline access fails for the chosen condition -> change the supported demo condition or mark current-care coverage unavailable.
- Gateway lacks required tool/structured-output support -> adapt transparently or request an approved route; never simulate success.
- Labeled evaluation shows unsupported claims persist -> strengthen abstention and review before expanding coverage.
- Pilot concurrency/restart requirements arrive -> adopt durable jobs and shared storage before launch.
- Measured setup time exceeds the demo budget -> use the fastest complete vertical slice and record the stack change.

See [[Wiki/Projects/healthcare-system|Project hub]] and [[Wiki/Concepts/healthcare-architecture-decisions|Proposed decisions]].
