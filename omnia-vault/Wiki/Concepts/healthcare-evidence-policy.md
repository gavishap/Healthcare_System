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
  - Raw/Sources/2026-10-27-evidence-runtime-implementation.md
  - Raw/Sources/2026-10-27-evidence-runtime-handoff.md
source_count: 6
aliases: []
---

# Healthcare Evidence Policy And Guardrails

> [!info] Runtime implementation
> Fixed-source identity/admission, deterministic research ordering, snapshot/quote checks, study lineage and potential conflict links are implemented under policy `us-evidence-2026-10-27.v2`. Uncited model limitation notes are withheld. Current-care and approval claims remain blocked without applicable guideline/regulatory evidence. This is a tested engineering policy, not clinical grading or expert certification. See [[Wiki/Concepts/healthcare-evidence-runtime]].

> [!info] Source and decision status
> The interview and PDF establish requirements; the authored design and researched documentation support the proposals. Technical choices remain proposed until adopted.

## Policy Boundary

Use a versioned, domain-reviewed policy. Deterministic rules enforce known metadata and claim eligibility; LLMs extract relevant passages and propose interpretations. Expert review defines/validates the policy. No model can silently promote a rejected record or invent a guideline. All thresholds below are provisional product engineering choices, not a validated medical grading scheme.

## Hard Gates Before Ordering

1. Validate provenance: allowlisted connector, canonical source identity, source version/snapshot and recoverable locator. An allowlisted domain alone is insufficient.
2. Check condition/subtype/population, jurisdiction, source scope and dates. Uncertain applicability is a visible limitation, not an assumed match.
3. Quarantine retracted/corrected/superseded evidence as applicable to the claim. Missing metadata stays unknown. A withdrawn therapy can still appear as historical context or a safety update with an explicit label.
4. Enforce claim-specific evidence requirements. Standard-care claims require applicable current guideline support; approval claims require the relevant regulatory record; a trial record with no results can support development-stage claims only.
5. Require exact existing evidence IDs and locators for every proposed claim. Check quoted spans against the saved snapshot. News/circular references without recoverable evidence never pass as independent support.

## Show Evidence Facets

Expose source class, study design, phase, status, results availability, population applicability, jurisdiction, guideline currency, regulatory status, access level and conflict flags separately. Store `policy_version`, `decision`, `reason_codes`, `review_needed`, and `evidence_family_id`. Use labels such as eligible/limited/excluded and their reasons; avoid a fake 0–100 truth score.

Default ordering is deterministic within comparable categories: applicability, eligible evidence class for that claim, results availability, then the relevant update/publication date and a stable identifier. Keep regulatory status and trial phase as separate facets rather than collapsing them into one hierarchy. The UI can sort pipeline entries by phase; it must not call the first entry the best therapy. If a weighted research-priority score is later requested, publish the formula, show missing inputs, and obtain domain review before using it.

## Contradictions And Citation Families

Retain contradictory claims with their evidence, dates, population and endpoints. An LLM can flag likely disagreement; distinguish genuine contradiction from different indications or time periods. Do not average incompatible results or let a majority of articles overrule the applicable regulator on approval status. Two articles about one study count as one evidence family. Link systematic reviews to included studies when recoverable; unknown overlap must remain unknown rather than fabricated independence.

Demonstration scenario (synthetic policy fixture): a news article calls a therapy a breakthrough, a registry entry is phase 2 with no results, an applicable FDA search has no verified approval match, and a guideline does not mention it. Output may state the registered investigational study and sponsor, mark efficacy unestablished in retrieved evidence and approval unknown, and exclude it from current-care claims. No search match is not proof of nonapproval. This is a logic fixture, not a claim about any real treatment.

## LLM Guardrails

Treat source text as untrusted data. Policy/schema/reference checks run outside the model. Semantic checking may flag weak support but cannot prove correctness. Unsupported claims are removed or sent to review; do not merely attach a citation to an otherwise unsupported sentence. Model agreement never substitutes for source support or expert judgment.

See [[Wiki/Concepts/healthcare-llm-and-tools|Runtime boundary]], [[Wiki/Concepts/healthcare-security-and-governance|Security]], and [[Wiki/Concepts/healthcare-evaluation-plan|Policy tests]].
