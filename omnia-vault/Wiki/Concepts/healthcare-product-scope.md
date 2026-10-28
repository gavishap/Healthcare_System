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

# Healthcare Product Scope

> [!info] Source and decision status
> The interview and PDF establish requirements; the authored design and researched documentation support the proposals. Technical choices remain proposed until adopted.

## Proposed Product

A condition intelligence workbench that helps health system strategy analysts prepare an auditable care-landscape and innovation briefing. The result supports research triage, service-line planning and conversations about institutions/companies. It makes no claim to choose therapy for an individual.

The minimum input is a condition name. Proposed explicit defaults are US jurisdiction and an as-of time; both remain assumptions until confirmed. Offer subtype/population clarification only when needed. A recent-activity window filters the emerging-evidence view; it does not erase older guidelines that remain current.

## User Flow

1. Enter a condition. Show normalized candidates, synonyms and scope. Ambiguous acronyms require confirmation.
2. Confirm the research scope. Display supported-source coverage before promising a complete briefing.
3. Generate with visible retrieval stages and partial failures.
4. Read an executive summary, current care landscape, emerging pipeline, and companies/institutions.
5. Open any factual claim to inspect its evidence, dates, excerpt, applicability, conflicts and inclusion reason.
6. Filter/sort evidence facets; export a report that retains citations, as-of time, policy version and gaps.

## Acceptance Criteria

| ID | Observable outcome |
|---|---|
| R1 | Condition ambiguity never silently changes the research population |
| R2 | Three required sections exist, or show a specific evidence gap |
| R3 | At least one visibly live primary retrieval is demonstrated |
| R4 | Every rendered factual claim has existing, inspectable evidence references |
| R5 | Rules determine claim eligibility and labels; model agreement cannot override a rejection |
| R6 | Trials, approval and care standards remain distinct; geography is visible |
| R7 | A failed source produces a coverage warning/partial state, never an invented conclusion |
| R8 | Evidence comparison avoids patient-specific treatment recommendations |
| R9 | A recorded replay shows original fetch time and is unmistakable from live mode |

Non-goals for the prototype: EHR integration, patient identifiers, prescribing/dosing, comprehensive coverage of every condition, economic ROI estimates without data, automatic procurement choices, autonomous outreach, model fine-tuning, and production compliance claims.

See [[Wiki/Concepts/healthcare-application-architecture|Architecture]], [[Wiki/Concepts/healthcare-briefing-interface|Interface]], and [[Wiki/Concepts/healthcare-open-questions|Open decisions]].
