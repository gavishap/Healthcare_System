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
  - Raw/Sources/2026-10-27-connector-smoke-check.md
  - Raw/Sources/2026-10-27-sourcing-discovery-transcript.md
  - Raw/Sources/2026-10-27-sourcing-research.md
  - Raw/Sources/2026-10-27-sourcing-design.md
source_count: 8
aliases: []
---

# Healthcare Condition And Source Strategy

> [!info] Source and decision status
> The interview and PDF establish requirements; the authored design and researched documentation support the proposals. Technical choices remain proposed until adopted.

## Condition Resolution

The extended interview explicitly fixes the prototype to the United States and suggests PubMed for current-care literature plus clinical-trials records for emerging treatments and companies. The detailed [[Wiki/Concepts/healthcare-sourcing-plan|sourcing plan]] preserves those decisions, adds a condition-specific guideline anchor, and scopes FDA/CDC to relevant regulatory/public-health claims. Adult type 2 diabetes with ADA guidance is a proposed first profile, not a condition chosen by the interviewer.

Keep raw input, canonical label, terminology identifier when available, aliases, selected subtype/population, jurisdiction and user confirmation. Start with a small curated condition catalog linked to MeSH; fuzzy matching proposes candidates only. Lexical match scores are search aids, not clinical confidence. Unknown or ambiguous terms produce clarification or an explicit unsupported-state response. Do not use an LLM guess to merge distinct conditions.

## Source Plan By Claim Type

| Research need | Proposed source | Permitted inference and limit |
|---|---|---|
| Standard of care | Current authoritative guideline for relevant geography/population | Attribute the recommendation and scope; approval/literature alone cannot substitute |
| Published evidence | PubMed metadata plus accessible abstracts/full text | Indexing is not validation; abstract-only access must be labeled |
| Development pipeline | ClinicalTrials.gov API v2 | Stage, status, sponsor, interventions, dates; registration alone is not benefit |
| Regulatory status | Applicable FDA approval record/label/history for covered products | Exact indication, population and date; not every medical intervention is covered |
| Companies/institutions | Trial sponsor/collaborator data, regulatory applicant, publication affiliations | Evidence supports the specific role only; no inferred ownership or commercial availability |
| Recent discovery | Optional news/press leads | Follow to underlying primary evidence; exclude unsupported promotional claims |

An FDA source is authoritative for the applicable regulatory fact. It does not automatically outrank a well-designed study on every efficacy question, or replace a guideline for care standards. Likewise, a review can contextualize evidence without multiplying the independent trial count.

## Retrieval Boundaries

For the first demo, select one condition with an accessible, date-checked guideline and enough real pipeline data. Type 2 diabetes is a candidate used only for API smoke requests; it has not been accepted as the demo condition or clinically reviewed. Expand to 2–3 supported conditions only after the first complete flow works. Unsupported terms should not trigger a promise of comprehensive research.

Fetch current records, and store both underlying source publication/update dates and the retrieval timestamp. A 30/60-day view is optional for new activity; retrieve established guidelines outside that window. Show query, filters, result caps and sources attempted so users can assess incomplete coverage. Fetching today does not make an old trial record current.

Public smoke requests on 2026-10-27 returned JSON from PubMed ESearch and ClinicalTrials.gov. This proves limited connectivity, not correct clinical retrieval or working application adapters. Guideline discovery/access is the critical unverified dependency; a generic NICE listing returned 403 and UK guidance cannot silently stand in for US care standards.

See [[Wiki/Concepts/healthcare-evidence-policy|Evidence rules]], [[Wiki/Concepts/healthcare-data-and-provenance|Source identity]], and [[Wiki/Concepts/healthcare-evaluation-plan|Evaluation]].
