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

# Healthcare Evaluation Plan

> [!info] Source and decision status
> The interview and PDF establish requirements; the authored design and researched documentation support the proposals. Technical choices remain proposed until adopted.

## What Correctness Means

Evaluate source retrieval, claim support, policy decisions and user interpretation separately. A well-formed response and a real citation do not prove the sentence follows from the evidence. Model agreement is not a ground-truth label. A domain reviewer must assess the supported condition's guideline mapping and representative clinical statements before real strategy reliance.

## Proposed Test Set

| Case | Expected observable behavior |
|---|---|
| Valid supported condition | Three sections populated or explicitly gapped; claim citations inspectable |
| Ambiguous acronym/subtype | User confirmation before research |
| Unsupported condition | Honest unsupported/limited coverage state |
| Registry record without results | Pipeline description only; no efficacy inference |
| Generic label listing without approval proof | Regulatory status unknown; no invented approval |
| Review plus three news copies of one trial | One evidence family when lineage can be verified |
| Circular citation with no primary record | Exclude as independent support; show reason |
| New press item conflicts with guideline | Keep dates/scope/conflict; no automatic guideline replacement |
| Abstract-only or paywalled source | Access level visible; no claim about unseen full text |
| Corrected/retracted/superseded source | Applicable policy flag/exclusion; no quiet reuse |
| Source outage/429/gateway failure | Bounded timeout and partial/source-only view with warning |
| Invented evidence ID or false quote | Claim rejected or one repair; never render as verified |
| Prompt injection in source | Cannot change tool permissions, policy or report instructions |
| Private-address URL/redirect | No fetch; typed rejection |
| Restart/cancel/duplicate request | Interrupted/cancelled or same idempotent run; no false complete |
| Replay fixture | Original retrieval time and replay label persist through export |

Use deterministic sanitized fixtures for edge cases and a small live smoke suite for adapter availability. Keep synthetic policy fixtures labeled. Version reviewer-labeled cases; record disagreement rather than treating majority model votes as truth. Tests should target consequential behavior rather than mirror implementation internals.

## Release Gates And Measurements

Prototype gate: demonstrate one supported-condition live path, one contradiction/eligibility example and one source failure/replay case. All rendered factual claims have valid evidence IDs/locators; no known unsupported clinical statement is accepted in the reviewed demo set. This is a release criterion, not an achieved result.

Pilot measurements: reviewer-labeled claim support precision, citation/reference validity, retrieval relevance on a curated set, current-care guideline applicability, company-role accuracy, duplicate-family errors, conflict detection, abstention correctness, latency percentiles, cost per run, provider failure rate and user time to a usable briefing. Set numerical quality targets with the domain reviewer after a baseline; do not invent 95% accuracy or ROI.

Log result caps and sources attempted. A finite test set cannot establish comprehensive literature coverage or clinical safety. User feedback and new failure cases trigger policy/prompt revisions and reruns of meaningful regression cases.

See [[Wiki/Concepts/healthcare-product-scope|Acceptance criteria]] and [[Wiki/Concepts/healthcare-delivery-roadmap|Demo sequence]].
