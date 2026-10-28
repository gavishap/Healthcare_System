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

# Healthcare Architecture Decisions

> [!info] Source and decision status
> The interview and PDF establish requirements; the authored design and researched documentation support the proposals. Technical choices remain proposed until adopted.

## ADR-001: Explicit Workflow With Deterministic Evidence Policy

**Status:** Proposed. **Date:** 2026-10-27. **Deciders:** Owner; domain reviewer validates evidence policy before pilot reliance.

**Context:** The strategy briefing needs live sources, transparent trust logic and a demonstrable slice in roughly two hours. The interviewer explicitly challenges model-voted authority and treatment recommendations.

**Decision:** Use deterministic source/claim eligibility, independent evidence facets, bounded model extraction/tool requests and cited synthesis. Use the LLM council for development decisions. Defer a runtime multi-model critic until evaluation proves benefit.

**Options:** A model-led autonomous council offers breadth but adds cost, latency, opaque agreement and difficult debugging. A rules-only extractor is reproducible but weaker for concise synthesis. The proposed hybrid preserves explainable control and uses models for text work.

**Consequences:** Evidence policy and supported guideline mappings require expert validation. The system can abstain and expose gaps. It must not market a facet ordering as medical certainty. Reopen if labeled evaluation shows an advisory critic materially catches unsupported claims within the budget.

## ADR-002: Modular Python API And Thin React UI

**Status:** Proposed. **Date:** 2026-10-27. **Decider:** Owner.

**Decision:** FastAPI/Pydantic plus React/TypeScript; SQLite and snapshots for local demonstration, PostgreSQL/object storage/durable worker for pilot. Use one application deployment boundary initially.

| Option | Complexity | Main strength | Main cost |
|---|---|---|---|
| FastAPI + React | Moderate | Explicit typed data pipeline and flexible evidence UI | Two-language setup |
| One TypeScript full-stack service | Moderate | One language and potentially faster familiar scaffold | Less advantage if Python is the established retrieval toolset |
| Streamlit | Low | Fastest fallback to a working end-to-end slice | Less UI control and later frontend migration |
| n8n as core | Low initial, rising with complex policy | Provided environment and visible wiring | Evidence contracts/tests/versioning harder to keep in one place |
| Multi-service autonomous agents | High | Independent runtime roles | Unjustified setup and operational burden for this slice |

**Consequences:** Choose the fastest already-proven scaffold when the actual build begins. No evidence in the transcript establishes the team's relative framework speed, so the preferred stack remains a recommendation. Reopen if setup consumes the retrieval/demo budget or existing client infrastructure requires another platform.

## ADR-003: Supported Conditions Before Universal Coverage

**Status:** Proposed. **Date:** 2026-10-27. **Decider:** Owner with domain reviewer.

**Decision:** Start with one condition and an explicitly checked applicable guideline. Use live public trial/publication queries and expose unavailable sections. Expand only with tested source coverage.

**Tradeoff:** Less breadth in the demo, stronger honesty about care-standard support. Generic search across arbitrary diseases would increase recall but does not establish accessible, current, applicable guideline evidence. Reopen after a reviewed condition catalog and source-coverage tests exist.

## Follow-up

- [ ] Confirm the preferred stack against actual remaining interview time.
- [ ] Select a condition, geography, guideline and reviewer.
- [ ] Verify the enterprise gateway's real tool/structured-output path.
- [ ] Resolve the council's surviving dissent and record any owner changes.

See [[Wiki/Concepts/healthcare-council-verdict|Council record]] and [[Wiki/Concepts/healthcare-application-architecture|Full design]].

> [!note] Council amendment
> The available council favors a Streamlit shell for a strict two-hour demo without a proven scaffold. FastAPI/React is the proposed target product; keep domain contracts reusable. The outsider favors a single TypeScript service. Claude seats/review are pending authentication, so this is not cross-model consensus. See [[Wiki/Concepts/healthcare-council-verdict]].
