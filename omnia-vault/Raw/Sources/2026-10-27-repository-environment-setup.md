---
Title: "Owner request and verified local repository/environment setup"
Reference: "Owner message and local setup checks, 2026-10-27"
ContentType:
  - "markdown"
Created: 2026-10-27
Processed: true
tags:
  - "source"
---

# Repository And Environment Setup

Owner request: "create a .env file for me as well as make the frontend and backend repos. im going to give you the ncib api key to use and the openai key"

The NCBI name is normalized in configuration; the supplied request is preserved above. No actual API keys are supplied in this message.

## Observed Setup

Created local Git repositories `backend/` and `frontend/` as siblings of `omnia-vault/` at the Obsidian workspace root. Both use branch `main`. Backend initial commit: `6fe01b9`. Frontend initial commit: `f60b39e`. Each commits a README, agent handoff instructions, `.gitignore` and `.env.example`. No remote is configured and no application implementation or dependencies are added.

Backend `.env` contains blank `OPENAI_API_KEY`, `NCBI_API_KEY`, `OPENAI_MODEL` and optional `NCBI_EMAIL` entries. Frontend `.env` contains only `VITE_API_BASE_URL=http://127.0.0.1:8000`, a public proposed React/Vite setting. No server is running there as a result of this setup. The eventual architecture may adapt the frontend setting to its chosen framework.

Verified via Git checks that `.env`, `.env.local` and `.env.production` are ignored in both repositories, while `.env.example` is trackable. Verified after the initial commits that `.env` is absent from tracked files, the working trees are clean, and neither repository has a remote. Verified empty backend key/model fields without emitting their values.

The environment files are preparation only: no loader, startup command, model selection, API authentication, web search or runtime sourcing exists yet. Actual credentials stay out of source captures and committed examples. Application code remains in its respective repository, separate from vault knowledge.
