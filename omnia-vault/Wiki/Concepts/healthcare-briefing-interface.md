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

# Healthcare Briefing Interface

> [!info] Source and decision status
> The interview and PDF establish requirements; the authored design and researched documentation support the proposals. Technical choices remain proposed until adopted.

## Proposed Screen

A single workbench begins with a condition input and candidate confirmation. The scope line always displays condition/subtype, jurisdiction, as-of date, live/replay mode and evidence coverage. Run progress shows actual source attempts, not simulated animation.

The completed briefing contains an executive summary and three core sections: current care landscape, emerging pipeline, and companies/institutions. Each section exposes evidence gaps even when another section succeeds. The executive summary is derived from validated claims and preserves their citations.

## Useful Visuals

- A pipeline table/timeline: intervention, phase, status, results availability, sponsor, last source update, evidence link. Phase labels and unknowns are explicit.
- An evidence comparison table: source class, applicability, publication/update dates, access level, policy reasons and conflict flags. Sort within a meaningful category; do not display a universal best-treatment leaderboard.
- A company/institution view: role-specific relationships to trials/interventions. Counts represent retrieved evidence, not market share or innovation performance.

Start with tables because they expose the required distinctions and are quick to ship. Add charts only when they answer a concrete strategy question. A missing result is not zero; inaccessible evidence is not a negative finding. Do not compare efficacy across studies with different populations/endpoints as though it were a controlled comparison.

## Evidence Drawer

Click a claim citation to see the source title/identifier, canonical URL, publication/update/retrieval dates, exact excerpt and section/JSON locator, applicability, source access level, evidence family, policy version and inclusion/exclusion reasons. Mark conflicting sources and show both accounts. Render source text as escaped text; do not trust external HTML.

Empty and partial states should say what could not be retrieved and what the analyst can do next. Unsupported conditions receive a specific explanation and supported candidates. Replay retains the original fetch timestamp in the header and export. Provide a concise strategy-use scope statement in the report; avoid cluttering each user action with engineering details.

See [[Wiki/Concepts/healthcare-product-scope|User acceptance]] and [[Wiki/Concepts/healthcare-data-and-provenance|Evidence fields]].
