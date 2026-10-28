# Evidence Desk

Healthcare condition intelligence for a US health system strategy team. This repository combines the backend, frontend, project vault, client presentation and sanitized AI project history.

## Contents

| Folder | Contents |
| --- | --- |
| `backend/` | FastAPI, evidence policy, source connectors, PostgreSQL storage, Docker Compose and tests |
| `frontend/` | React/TypeScript Evidence Desk workbench |
| `omnia-vault/` | Project knowledge, source captures, source attachments, design decisions and handoffs |
| `Presentation/` | Three-slide `Evidence_Desk_deck.pptx` and visual previews |
| `AI History/` | Every discovered project chat and supporting council/Claude session, with a coverage manifest |

## Run locally

1. Copy `backend/.env.example` to `backend/.env` and fill in your own API credentials.
2. From `backend/`, run `docker compose up -d --build`.
3. Open http://localhost:5173. The API runs on http://localhost:8000.

The published files contain no actual API credentials. Database contents, running-service state, dependency caches and local editor settings are not part of the repository.

## Current scope

The local prototype retrieves PubMed/NCBI and ClinicalTrials.gov records, checks source identity and applicability, retains claim-to-source evidence, separates specific populations and exports cited reports. Current standard-care statements require an applicable US guideline connector, and approval claims require appropriate FDA evidence; both remain coverage gaps. Domain review and shared-pilot operations remain required. The latest bounded example contains eight records and six statements for specific populations, with general sections unavailable.

## Project history

`AI History/README.md` explains the archive, redactions and snapshot cutoff. It includes human/assistant messages and visible tool records, excluding private internal reasoning and system/developer scaffolding. Original raw sessions and credentials stay local. `SOURCE_REPOSITORIES.json` records the source commits; this is one combined source snapshot, with no submodules or nested Git repositories.

The live presentation is named **Evidence Desk_deck**: https://chatgpt.com/space/page_6776fb97e91c8191aa54596235d43dfc (access follows the original account permissions). The PPTX can be opened independently.
