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
  - Raw/Sources/2026-10-27-healthcare-architecture-council.md
source_count: 5
aliases: []
---

# Healthcare Delivery Roadmap

> [!info] Source and decision status
> The interview and PDF establish requirements; the authored design and researched documentation support the proposals. Technical choices remain proposed until adopted.

## Proposed 120-Minute Build Slice

This is an implementation plan for the interview constraint, not a record of elapsed work or a promise that planning has left the full window available. Reassess time remaining before starting. Reserve the separate slide/Q&A time described by the sources.

| Minutes | Deliverable | Cut if behind |
|---|---|---|
| 0–10 | Confirm one supported condition/jurisdiction; validate gateway auth, real tool-call round trip and output schema; choose accessible guideline | Change supported condition if guideline unavailable; disclose gateway limits |
| 10–30 | Source adapters for checked guideline, ClinicalTrials.gov and PubMed; save provenance and one replay fixture | FDA live adapter can defer, with approval status unknown |
| 30–50 | Typed records, deduplication and deterministic eligibility/reason codes | Use facets, no numeric scoring or complex graph |
| 50–75 | Bounded model extraction/tool dispatch and cited synthesis; reference checks and partial outputs | Omit optional critic/council runtime |
| 75–95 | Minimal interface: condition, progress, three sections, evidence drawer and tables | Use Streamlit if no working React scaffold; drop chart polish |
| 95–110 | Verify supported case, ambiguity, unsupported claim and source-failure behavior | Focus consequential checks and truthful limitations |
| 110–120 | Demo rehearsal, README/setup, sanitized fixtures and known gaps; prepare repository contents | Skip cloud deployment |

If actual remaining time is substantially shorter, deliver one cited vertical slice with transparent gaps and a Streamlit interface rather than claiming all capabilities are complete. Local deployment meets the transcript's minimum. Prioritize actual model tool calling, real retrieval and visible policy over decorative architecture.

## Demo Narrative And Slide Plan

Walk through the strategy analyst's condition input, ambiguity confirmation, live source retrieval, three-section briefing, one evidence drawer, a trial-without-results guardrail and a partial-source failure. Show source dates and research gaps. Explain deterministic evidence eligibility versus model summarization in plain language.

Plan one stakeholder slide: who needs this and the current manual research burden; how one condition becomes a cited care/pipeline/company briefing; why visible evidence/gaps improve review; what the prototype demonstrates; next validation step. Do not claim quantified time savings, clinical outcomes or ROI without measurement. A slide file is not created by this architecture task.

Repository handoff plan: application code, clear startup instructions, environment variable names without values, architecture/limitations, meaningful checks and permitted small fixtures. The interview requests a repository link and optionally AI chats. Actual sharing/pushing requires the owner's instruction and a destination; never push to the Omnia template origin. Redact secrets, account details, private material and machine paths from any future chat export.

## Beyond The Interview

1. Review policy/guideline mappings with a domain expert and establish a labeled evaluation baseline.
2. Add pilot identity, durable jobs, PostgreSQL/object storage, monitoring and evidence/source-use governance.
3. Expand condition/jurisdiction coverage with checked source registries and measured retrieval quality.
4. Add report comparison, evidence-change tracking, saved research and optional advisory critic only when users need them.

See [[Wiki/Concepts/healthcare-open-questions|Open decisions]] and [[Wiki/Concepts/healthcare-evaluation-plan|Release gates]].

> [!note] Council amendment
> The available council favors a Streamlit shell for a strict two-hour demo without a proven scaffold. FastAPI/React is the proposed target product; keep domain contracts reusable. The outsider favors a single TypeScript service. Claude seats/review are pending authentication, so this is not cross-model consensus. See [[Wiki/Concepts/healthcare-council-verdict]].
