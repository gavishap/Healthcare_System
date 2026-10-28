---
tags:
  - "project"
topics:
  - "healthcare-system"
status: growing
created: 2026-10-27
updated: 2026-10-27
sources:
  - Raw/Sources/2026-10-27-architecture-request.md
  - Raw/Sources/2026-10-27-prototype-challenge.md
  - Raw/Sources/2026-10-27-discovery-transcript.md
  - Raw/Sources/2026-10-27-architecture-analysis.md
  - Raw/Sources/2026-10-27-architecture-research.md
  - Raw/Sources/2026-10-27-sourcing-request.md
  - Raw/Sources/2026-10-27-sourcing-discovery-transcript.md
  - Raw/Sources/2026-10-27-sourcing-design.md
  - Raw/Sources/2026-10-27-sourcing-research.md
  - Raw/Sources/2026-10-27-openai-sourcing-selection.md
  - Raw/Sources/2026-10-27-repository-environment-setup.md
  - Raw/Sources/2026-10-27-evidence-runtime-request.md
  - Raw/Sources/2026-10-27-evidence-runtime-implementation.md
  - Raw/Sources/2026-10-27-evidence-runtime-handoff.md
  - Raw/Sources/2026-10-27-evidence-scope-trace.md
  - Raw/Sources/2026-10-27-client-presentation.md
  - Raw/Sources/2026-10-27-client-presentation-consolidation.md
  - Raw/Sources/2026-10-27-github-consolidation.md
  - Raw/Sources/2026-10-27-github-publication-verification.md
source_count: 19
aliases: []
---

# Healthcare System

## Goal

Design a condition intelligence application for a health system strategy team: an auditable briefing covering current care, emerging treatments and involved companies/institutions. Preserve the corrected strategy-team scope, live-source requirements and deterministic evidence policy from the interview.

## Status

Evidence Desk is implemented and running locally: React/TypeScript UI, FastAPI API and PostgreSQL in Docker Compose. It retrieves PubMed/NCBI and ClinicalTrials.gov records, authenticates source identity, orders citations deterministically, connects claims to exact saved evidence, preserves potential conflicts and exports cited reports. Start with [[Wiki/Concepts/healthcare-evidence-runtime|the implemented evidence runtime]].

The supplied keys work. The current policy-v3 correction separates general conditions from specific populations, gates emerging activity by trial purpose/status/currency, and makes organization eligibility follow the study. Read [[Wiki/Concepts/healthcare-evidence-scope-trace|the original-result trace and correction]]. Thirty-six backend tests, production builds and browser checks pass. The final same-condition live run retrieves eight records and accepts six statements, all in population-specific evidence; general sections stay unavailable in this bounded sample. Current standard-care and approval content still requires guideline/FDA connectors and domain review.

## Start Here

The [[Wiki/Concepts/healthcare-client-presentation|client presentation]] is ready: three landscape slides explain the client value, evidence workflow, actual prototype and proposed pilot. The original longer deck is consolidated in place; current coverage limitations and source-backed presenter notes remain.

The owner selects OpenAI. The runtime uses direct biomedical connectors and a bounded evidence-read tool. Hosted web search remains an unimplemented supplemental discovery option.

- [[Wiki/Concepts/healthcare-evidence-scope-trace|Original-result trace and population correction]]
- [[Wiki/Concepts/healthcare-evidence-runtime|Implemented application, processing boundary and verification]]
- [[Wiki/Concepts/healthcare-sourcing-plan|First sourcing-layer plan and implementation order]]
- [[Wiki/Concepts/healthcare-sourcing-contract|Sourcing contract for architecture integration]]
- [[Wiki/Concepts/healthcare-discovery-summary|Conversation summary and corrections]]
- [[Wiki/Concepts/healthcare-application-architecture|Full application architecture and diagram]]
- [[Wiki/Concepts/healthcare-council-verdict|Council verdict and dissent]]
- [[Wiki/Concepts/healthcare-architecture-decisions|Proposed architecture decisions]]
- [[Wiki/Concepts/healthcare-delivery-roadmap|Prototype plan and growth path]]
- [[Wiki/Concepts/healthcare-open-questions|Open decisions and assumptions]]

## Local Development Repositories

The Obsidian workspace root contains three sibling repositories: `backend/`, `frontend/` and `omnia-vault/`. Application code and lockfiles live in the application repositories; this vault contains the development knowledge. The owner's combined private [GitHub repository](https://github.com/gavishap/Healthcare_System) now contains their source snapshots, source attachments, `Presentation/Evidence_Desk_deck.pptx` and `AI History/`. Its initial push is verified against the remote branch and GitHub file tree. Thirteen local chat/council/Claude sessions have sanitized visible conversation and tool archives, with unique paths, counts, hashes and an active-chat capture timestamp in the manifest. Source commit identities are retained; original repositories remain intact and the vault's template origin must not receive project material. The separate combined publishing checkout is `../.publish/Healthcare_System/` relative to this vault.

OpenAI and NCBI keys remain only in ignored backend configuration, loaded explicitly by the settings layer. Frontend configuration contains only a public API address. Start the full application from `backend/` with `docker compose up -d --build`. Interface: [localhost:5173](http://localhost:5173); API docs: [localhost:8000/docs](http://localhost:8000/docs). PostgreSQL persists in a named volume on local port 55432, without replacing an existing database on 5432. Actual key values are checked absent from tracked candidates and client builds.

## Work Directions

| Direction | Note |
|---|---|
| Implemented evidence layer and local runtime | [[Wiki/Concepts/healthcare-evidence-runtime]] |
| User/problem and acceptance | [[Wiki/Concepts/healthcare-product-scope]] |
| Condition resolution and source coverage | [[Wiki/Concepts/healthcare-condition-and-source-strategy]] |
| Deterministic evidence policy | [[Wiki/Concepts/healthcare-evidence-policy]] |
| LLMs and server tool calling | [[Wiki/Concepts/healthcare-llm-and-tools]] |
| Data, citations and source versions | [[Wiki/Concepts/healthcare-data-and-provenance]] |
| API and research state machine | [[Wiki/Concepts/healthcare-api-and-job-flow]] |
| Evidence tables and analyst interface | [[Wiki/Concepts/healthcare-briefing-interface]] |
| Security and policy governance | [[Wiki/Concepts/healthcare-security-and-governance]] |
| Evaluation and failure cases | [[Wiki/Concepts/healthcare-evaluation-plan]] |
| Deployment and operations | [[Wiki/Concepts/healthcare-deployment-and-operations]] |

## Next Steps

- [x] Implement and verify one type 2 diabetes live slice with source-linked evidence and explicit coverage gaps.
- [x] Verify NCBI/OpenAI authentication, a real evidence-tool round trip and structured output.
- [x] Build the frontend/backend with persistent PostgreSQL and Docker.
- [ ] Register and validate an accessible current US guideline; add an applicable FDA adapter if approval claims are needed.
- [ ] Validate the evidence policy with a domain reviewer.
- [ ] Define pilot identity, durable jobs, migration/backup policy and expanded source coverage before operational use.

## Related

- [[Wiki/Topics/healthcare-system|Knowledge hub]]
- [[Wiki/Concepts/source-ingestion-workflow|Vault ingestion workflow]]
