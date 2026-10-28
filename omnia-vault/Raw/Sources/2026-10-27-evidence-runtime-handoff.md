---
Title: "Evidence runtime baseline checkpoint and concurrent scope correction"
Reference: "Application Git checkpoints, shared working-tree observations and the active chat Trace trial result mismatch"
ContentType:
  - "markdown"
Created: 2026-10-27
Processed: true
tags:
  - "source"
---

# Baseline And Concurrent Work

The evidence application baseline is committed locally: backend `5e62673`, frontend `862f36f`. The baseline includes the core implementation and initial condition-scope additions that arrived in the shared repository during integration. The final baseline test command observed 31 passing backend tests, including the original 20 core tests and added scope regressions. No keys are tracked or exposed in candidate code/client builds; the secret scan passes. The v2 live API run and browser results in the earlier implementation capture remain historical verification evidence.

An active separate chat titled **Trace trial result mismatch** is continuing a client-requested trace of NCT01954147 and condition/population relevance. It is adding policy v3 scope/currency/section eligibility and further regression cases, with changes in the same backend files. Those ongoing edits are preserved and are not reverted, overwritten or represented here as final verified runtime behavior. The policy-v2 live example is not proof that all later policy-v3 changes have been exercised live.

During that work the API connection briefly disconnected, consistent with a local rebuild/restart; this capture does not assert that the in-progress work is broken or complete. Avoid racing another deployment or editing its modules. The owner can continue that correction in its existing chat. A final scope-correction handoff should supersede this concurrency notice once its UI, report, live/recorded trace and deployment checks finish.

This record distinguishes completed baseline implementation from a separate active correction. Domain-reviewed guideline binding/FDA coverage remain absent in the baseline; no current-care or approval claim is manufactured to hide that gap.
