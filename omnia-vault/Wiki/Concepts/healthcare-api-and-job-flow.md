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

# Healthcare API And Job Flow

> [!info] Source and decision status
> The interview and PDF establish requirements; the authored design and researched documentation support the proposals. Technical choices remain proposed until adopted.

## Proposed API

| Endpoint | Contract |
|---|---|
| `POST /api/conditions/resolve` | Validated condition query -> candidates, ambiguity and supported coverage |
| `POST /api/research-runs` | Confirmed scope, filters, live/replay mode + idempotency key -> 202 and run ID |
| `GET /api/research-runs/{id}` | State, stages, warnings, coverage, budget use and eventual briefing reference |
| `POST /api/research-runs/{id}/cancel` | Request cooperative cancellation; no new work once accepted |
| `GET /api/briefings/{id}` | Typed section/claim/evidence IDs, dates, gaps, conflicts and versions |
| `GET /api/evidence/{id}` | Inspectable source metadata, excerpt/locator, policy reasons and safe canonical link |
| `GET /api/briefings/{id}/export` | Cited JSON/Markdown; polished PDF export deferred |

Pilot endpoints require authenticated run ownership/tenant checks on every ID. Local demo binds to loopback. Poll run status for the prototype; add server-sent events only if polling harms the experience. Server keys and raw internal prompts are never included in public API responses.

## State Machine

`created -> resolving -> fetching -> normalizing -> extracting -> validating -> complete | partial | failed` with `cancelled` and `interrupted` terminal states. Scope is confirmed before creation; resolving checks the canonical scope/registry. Persist stage transitions, source attempts, timestamps and reasons. Do not use a green complete status when essential coverage is missing.

The local demo can use one process and a tracked background coroutine with persisted records. That work is not durable: restart marks active runs interrupted and offers explicit retry/replay. FastAPI BackgroundTasks alone must not be described as reliable distributed job execution. Before a shared pilot, add a separate worker with durable queue/DB job records, leases, bounded retries, checkpoints and idempotent stage writes.

## Budgets And Error Semantics

Initial targets, to validate rather than advertise as measured: about 10 seconds per external source attempt, one retry for transient network/429/5xx only when the overall deadline permits, and a 90-second end-to-end run ceiling. Honor Retry-After; use jitter and a per-provider limiter. Public PubMed access has documented rate limits; multiple workers must share the limit. Cap model requests/tokens and reserve time to validate/render a partial result.

Record source statuses separately: success, no results, timeout, rate-limited, unavailable, unsupported. No-results is not evidence of absence. One failed source need not discard good evidence from another, but missing guidelines prevent a claim of verified current care. A gateway failure may allow a clearly labeled source-only results view, never a fabricated generated briefing.

Idempotency binds the same creation key to the same caller and scope. Concurrent retries must not duplicate a run. Tool-call IDs and source-write keys prevent duplicates; cancellation/deadline checks occur between awaits/stages. Never retry permanent auth/schema/policy errors indefinitely.

See [[Wiki/Concepts/healthcare-application-architecture|Modules]] and [[Wiki/Concepts/healthcare-evaluation-plan|Failure tests]].
