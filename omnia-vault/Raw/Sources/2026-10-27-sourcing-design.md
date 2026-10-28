---
Title: "Original sourcing-layer design proposal"
Author: "Codex"
Reference: "Original proposal for the owner's sourcing-layer planning request, 2026-10-27"
ContentType:
  - "markdown"
Created: 2026-10-27
Processed: true
tags:
  - "source"
---

# Original Sourcing Design Proposal

This is an authored first draft, not a client-approved policy or implemented application. It uses the extended interview's explicit U.S. scope and PubMed/clinical-trials mapping. FDA is retained for covered regulatory facts; CDC is optional context. Add a condition-specific U.S. guideline publisher to substantiate current-care claims. Propose adult type 2 diabetes and ADA as a small first example, subject to document access and scope checks. The user has a separate architecture agent; this work defines the sourcing boundary and integration contract without choosing its frontend, job queue or deployment.

Use four core source families: a guideline registry entry, PubMed via E-utilities, ClinicalTrials.gov via API v2, and a covered FDA drug-record adapter. Start wiring ClinicalTrials.gov because one structured result yields development metadata plus sponsor/collaborator roles. Prove one NCT record and one organization relation, then PubMed/PMID and article access labels, then the current guideline, then targeted FDA lookup. The final slice includes all required sources or explicit gaps; metadata-only partial progress must not be described as a complete briefing.

The server resolves confirmed condition scope and source policy, executes required sources, stores bounded snapshots and metadata, normalizes stable identifiers, and reports failures separately from no matches. The LLM may propose synonyms, constrained follow-up queries and candidate evidence spans. It cannot choose a new authority, alter the policy, call arbitrary URLs or label an unsupported treatment standard care. Provider adapters expose model generation and optional search separately: a plain LLM key is not proof of web-search capability. Probe supplied route authentication, tool calling and structured output; public biomedical APIs use their own access arrangements. Keep credentials in backend environment variables, never in notes, request bodies, logs or browser clients.

Fixed authority is claim-specific. A guideline supports attributed recommendations within its scope; a trial record supports registered stage/status/sponsor and results only where present; a regulator supports applicable product/indication decisions; a paper supports statements within the material actually retrieved. Do not infer government endorsement from registry inclusion or PubMed indexing. Reviews contextualize and may synthesize evidence, but do not add independent study counts. Company ownership, manufacturing and commercial rights require separately supported roles. News, promotional releases and awards cannot establish efficacy or current care. A condition unrelated to the supported profile gets an unsupported/clarification response, not expansive invented research.

Maintain source document/version, hash, access level, study family and evidence IDs, record dates and retrieval time, excerpt plus JSON-pointer/page/section locator, applicability, potential correction/retraction/supersession flags, and separate regulatory status. Preserve missing metadata as unknown. Resolve duplicate PMID/DOI/NCT IDs and study links only where supported. Preserve conflicts and historical versions. Runtime sourcing returns candidate evidence and provenance to the deterministic validator; admissibility by claim type and final claim validation remain explicit downstream steps. A candidate passing metadata screening is not medically validated.

Use bounded retrieval: initial target at most 20 candidates across connectors, source-specific reserved slots, at most two model follow-up rounds/four supplemental tool calls, one source-controlled document link hop and no recursive news citation crawling. All are engineering defaults, adjustable after evaluation rather than a medical scoring system. Store searched queries, filters, pagination/truncation, skipped items and connector states. Carry global research relevance separately from U.S. jurisdiction of care/approval; record study geography and applicability without assuming all studies in ClinicalTrials.gov are U.S.-based. Recent 30/60-day views supplement established guidance. Publication date and last registry update mean different things.

Acceptance checks should include a real inspectable NCT and sponsor role, accessible guideline passage and PMID, indication-specific FDA evidence or explicit unknown, no-results trial limitation, misleading FDA label, circular citation, duplicate study, retraction/supersession, contradictory evidence, unknown organization role, unrelated subtype, malicious source text, inaccessible text, connector failure and a model budget stop. All surfaced evidence references resolve exactly; negative test cases never become affirmative care/efficacy/approval claims. This is necessary engineering validation and does not certify clinical truth. Prototype policy is assumed approved within the exercise only; real use requires actual domain review. No runtime code, key, end-to-end test or clinical evidence review exists in this draft session.
