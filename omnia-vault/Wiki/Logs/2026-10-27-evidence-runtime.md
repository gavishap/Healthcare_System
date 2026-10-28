---
tags:
  - "log"
topics:
  - "healthcare-system"
status: growing
created: 2026-10-27
updated: 2026-10-27
sources:
  - Raw/Sources/2026-10-27-evidence-runtime-request.md
  - Raw/Sources/2026-10-27-evidence-runtime-implementation.md
  - Raw/Sources/2026-10-27-evidence-runtime-handoff.md
source_count: 3
aliases: []
---

# Evidence Runtime Implemented

Built the FastAPI/PostgreSQL evidence pipeline and React analyst interface in the sibling application repositories, with Docker Compose for a working local application. Existing upstream keys are used from ignored backend configuration; no keys are exposed to the client or committed.

Implemented fixed PubMed/NCBI and trial connectors, source identity and snapshot authentication, deterministic ordering, exact claim/passages, semantic support review, explicit study lineage, potential opposing findings, inspectable citation drawer and cited Markdown/JSON exports. The sourcing workstream can hand off canonical PMID/NCT identifiers to the implemented processing endpoint.

Twenty backend tests, actual API/model retrieval, frontend/Docker builds and browser checks pass. The final v2 live example contains eight source records and ten accepted/structured claims; three candidates and uncited model limitation notes are withheld. A separate labeled synthetic example demonstrates both sides of a conflict.

Current care/approval coverage remains incomplete because no checked guideline/FDA adapter exists in this slice. Jobs are local and single-process; domain review and production infrastructure remain open. See [[Wiki/Concepts/healthcare-evidence-runtime|Implemented runtime]].
