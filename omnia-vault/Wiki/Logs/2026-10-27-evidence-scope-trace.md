---
tags:
  - "log"
topics:
  - "healthcare-system"
status: growing
created: 2026-10-27
updated: 2026-10-27
sources:
  - Raw/Sources/2026-10-27-evidence-scope-trace.md
source_count: 1
aliases: []
---

# Traced And Corrected The Diabetes Briefing Mismatch

Traced the screenshot to its original PostgreSQL run and immutable sources. The actual pregnancy-specific source was a PubMed paper; the linked cord-cell trial excludes pregnancy. Missing population gates placed pregnancy/pediatric findings in general care, while unconditional registry field copying promoted an old unknown-status trial and its sponsor into current activity.

Implemented and locally deployed policy-v3 subtype, focus, population, currency and section eligibility. Added a read-only source-version replay, role checks, explicit guideline-gap wording, legacy notices and date-only display correction. [[Wiki/Concepts/healthcare-evidence-scope-trace|The full trace]] records before/after evidence and the final live run. Thirty-six backend tests and browser/build checks pass. Guideline/FDA connectors and domain review remain open; no historical report or remote publication is changed.
