---
tags:
  - "concept"
topics:
  - "healthcare-system"
status: growing
created: 2026-10-27
updated: 2026-10-27
sources:
  - Raw/Sources/2026-10-27-healthcare-architecture-council.md
  - Raw/Sources/2026-10-27-architecture-request.md
source_count: 2
aliases: []
---

# Healthcare Council Verdict

## Council Verdict: Healthcare Briefing Architecture

**The bench:** Skeptic — Codex; Rebuilder — Claude unavailable; Maximalist — Claude unavailable; Outsider — Codex (isolated); Operator — Codex. This is an incomplete three-seat council with one Codex blind review, not a completed cross-model council. Claude Code authentication failed twice per seat with “OAuth session expired and could not be refreshed.” A later read-only auth check still reports logged out. The owner says they will sign in; no Claude opinion is attributed until a successful invocation exists.

### Consensus

All three available seats independently favor a narrow supported-condition slice, explicit provenance, deterministic evidence controls, bounded LLM work and visible uncertainty. All reject an autonomous runtime council as a substitute for evidence authority. Current applicable guideline coverage is the critical dependency; live retrieval and citation presence do not establish medical correctness.

### Dissent

Skeptic and Operator choose Streamlit for the strict two-hour prototype because no application scaffold exists. Outsider chooses one TypeScript full-stack service to avoid a later migration and reduce language boundaries. The Chair proposes FastAPI/Pydantic plus React as the target application architecture, agreeing with the majority that a Streamlit shell is the safer initial demo when setup time is unproven. No seat establishes the team's actual framework speed, so the target stack recommendation has moderate confidence and remains proposed.

Operator allows an optional LLM summary/deterministic fallback. The owner's requested LLM/tool-calling architecture still requires a real tool-call round trip in the intended demo; a source-only fallback must be labeled as degraded and cannot be represented as satisfying that capability. This preserves the useful failure path without silently changing the requirement.

### Caught In Review

The Codex reviewer selects the Operator opinion as the strongest executable plan, identifies overbroad day-one scope in the Outsider proposal, and adds an explicit demonstration acceptance contract: check semantic support, missing guidelines, registry versus efficacy/approval, evidence deduplication and partial-source visibility. The reviewer also restores the current authorization boundary (planning/notes only) and the business pitch as a separate planned deliverable. The second bench's review is absent because Claude is unavailable.

### The Chair's Ruling

Recommend a condition intelligence workbench for strategy analysts, with separate current-care, emerging-pipeline and organization views. Use explicit workflow stages, fixed source adapters, versioned claim-specific evidence rules, bounded tool calls, and cited synthesis. Show source/update/retrieval dates, eligibility reasons, conflicts and evidence-family links. No treatment leaderboard or opaque scalar trust score.

Target the full-stack product as a modular FastAPI/Pydantic service and thin React/TypeScript UI. Use SQLite/local immutable snapshots for a local single-user demonstration and PostgreSQL/object storage/durable workers for a shared pilot. With an unproven scaffold and a hard two-hour build window, begin with reusable Python domain modules in a Streamlit interface, then expose the same domain contracts through FastAPI/React. A one-language TypeScript service is a credible alternative if it is demonstrably the fastest proven team scaffold. Do not claim that this condition has already been established.

This is engineering advice with moderate confidence, limited by missing Claude perspectives, unknown team scaffold speed, unchosen guideline/condition and untested enterprise credentials. Domain experts must validate clinical evidence rules. Reopen the stack if setup exceeds the demo budget; reopen coverage if no applicable current guideline is available; reconsider an advisory critic only if labeled evaluations show measurable benefit at acceptable cost/latency.

### First Move

Select one condition and jurisdiction, then verify an accessible current guideline and one inspectable claim-to-source example before implementation.

## Full Record

[Full council session](../../_relay/council/2026-10-27-healthcare-briefing-architecture.md)

See [[Wiki/Concepts/healthcare-application-architecture|Architecture]], [[Wiki/Concepts/healthcare-architecture-decisions|Decisions]], and [[Wiki/Concepts/healthcare-delivery-roadmap|Delivery plan]].
