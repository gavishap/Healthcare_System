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

# Healthcare Deployment And Operations

> [!info] Source and decision status
> The interview and PDF establish requirements; the authored design and researched documentation support the proposals. Technical choices remain proposed until adopted.

## Local Prototype

Build the React UI and serve static assets with FastAPI under one origin; use one backend process, SQLite and a local snapshot directory. During development Vite may run separately with an API proxy. Bind the demo to loopback, load model credentials from an untracked environment file, and provide a startup check for gateway/source availability. Store exact dependency versions in a lockfile during implementation; no versions are selected merely from memory in this plan.

A local request background task is interruptible by process restart. Persist run metadata and mark active runs interrupted on boot. Provide a cached/replay evidence fixture clearly labeled with fetch time. No cache or fixture is described as a fresh live retrieval.

## Optional Hosted Demo

A single container can serve the API and built UI. Add a health endpoint, server-side secret injection, HTTPS, access restriction, request caps, and persistent storage suitable for the deployment platform. Never place SQLite on an ephemeral filesystem and call the history durable. Cloud hosting is a bonus only after the core live demo works; it is not authorized to execute in this planning turn.

## Shared Pilot

Move metadata to PostgreSQL and snapshots to object storage. Keep the modular API and add a durable worker/queue or DB-backed job leasing with checkpoints. Introduce migrations, immutable source versions, tenant/run authorization, backups and tested restore, retention controls and safe deployment rollback. Use job IDs to join traces across API, worker, tools, model and report. A pilot worker cannot rely on an HTTP process remaining alive.

Version prompts, policies, parsers and model routes alongside each run. Monitor source availability, freshness/coverage gaps, unsupported claims rejected, review backlog, rate-limit errors, p50/p95 completion time and actual model usage/cost. Budgets and dollar costs depend on the supplied gateway configuration and are unmeasured. Separate stale-source age from recent retrieval time in monitoring.

Refresh scheduling is a later feature; n8n could trigger server APIs when needed. Do not build an ingestion platform, vector service or autonomous crawler until measured usage supports it. Store observability content sparingly and redact secrets/accidental personal data.

See [[Wiki/Concepts/healthcare-api-and-job-flow|Run durability]] and [[Wiki/Concepts/healthcare-security-and-governance|Security requirements]].
