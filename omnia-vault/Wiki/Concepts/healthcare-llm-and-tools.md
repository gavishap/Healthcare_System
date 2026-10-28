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
source_count: 4
aliases: []
---

# Healthcare LLM And Tool Calling

> [!info] Source and decision status
> The interview and PDF establish requirements; the authored design and researched documentation support the proposals. Technical choices remain proposed until adopted.

## Two Separate Councils

The development council compares architectures and exposes dissent. It does not run inside every user research request. The application initially uses one gateway-backed model with a bounded extraction/synthesis workflow. An optional later critic can flag unsupported claims; a second model is advisory, never an authority vote.

## Runtime Responsibilities

The workflow always attempts required supported-condition sources; the model cannot skip the guideline attempt or hide retrieval failures. It may propose a small number of supplemental search queries through typed tools after inspecting the coverage gaps. This satisfies tool calling while keeping control in the server.

| Tool | Input contract | Returns |
|---|---|---|
| `search_trials` | canonical condition ID, bounded query, optional stage/status, capped count | Normalized study records and provenance IDs |
| `search_pubmed` | canonical condition ID, bounded query/date window, capped count | Metadata/excerpts plus access labels |
| `get_guideline` | supported guideline registry ID | Checked document version/sections and limitations |
| `lookup_regulatory_record` | normalized intervention + indication + jurisdiction | Matched record or unknown/ambiguous, never inferred approval |

These are proposed function contracts. The backend maps IDs to fixed endpoints and validates all arguments. Do not expose arbitrary URL fetch, SQL, shell execution, filesystem access, email or deployment tools to the model. Organization links are extracted from typed evidence and role-checked without a broad web crawler in the demo.

## Bounded Sequence

1. Deterministic condition confirmation and source plan.
2. Parallel required-source fetches; metadata screening and snapshots.
3. Optional tool-call round: model proposes gap-filling searches; server validates and executes. Proposed ceiling: two rounds, four supplemental tool calls total.
4. Extract candidate claims/organizations from bounded evidence packets. Model returns source IDs and locators, never arbitrary citation URLs.
5. Apply claim-specific rules, identify duplicates/conflicts, and synthesize only eligible claims into a typed briefing.
6. Validate references and support; allow one bounded repair of schema/reference errors. Drop unresolved claims and show gaps. Stop on deadline/budget; do not loop until the model sounds confident.

Source and token caps are configurable provisional limits: begin with at most 20 candidate records across sources and a small approved guideline excerpt set. Track truncation and relevant evidence omitted. Test the cap on the selected condition rather than claiming it guarantees coverage.

## Gateway Adapter

`generate_structured(schema, evidence_packet, tools, budget)` returns validated data or a typed error, plus model route, prompt version and usage. Backend environment variables hold gateway URL/model/key; no key was supplied in this planning session. First implementation step must verify a real function-tool request/result round trip and structured-output behavior against the supplied enterprise gateway. Public support is insufficient proof of this exact configuration.

If structured output is unavailable, request JSON and validate locally with a bounded repair. If tool calling is unavailable, use a supported route only with authorization or explicitly report the limitation; do not call a deterministic fetch a successful model tool call. Never silently swap providers. Expert feedback changes versioned prompts/policy and evaluation fixtures, not live model weights.

See [[Wiki/Concepts/healthcare-api-and-job-flow|Workflow states]] and [[Wiki/Concepts/healthcare-evidence-policy|Claim controls]].
