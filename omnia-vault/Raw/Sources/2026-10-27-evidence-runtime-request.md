---
Title: "Owner request to implement the evidence-processing application"
Reference: "Owner request in the current Codex session, captured 2026-10-27"
ContentType:
  - "markdown"
Created: 2026-10-27
Processed: true
tags:
  - "source"
---

# Implementation Request

The owner states that another chat is preparing frontend/backend directories and asks this workstream to implement the layer after sourcing, based on the vault and the relevant final interview discussion. The required behavior covers citation-ranking criteria, conflicting citations, and connecting retrieved knowledge to its citations. The request also authorizes building the frontend, backend and integrated local solution, applying the vault's frontend skills, using the provided NCBI/OpenAI credentials, and using PostgreSQL for storage with Docker if needed.

"NCIB" is interpreted as NCBI, which provides PubMed access. The request does not establish a new numerical trust formula, clinical grading scheme or additional medical institution approval. The relevant final transcript is already captured in `Raw/Sources/2026-10-27-sourcing-discovery-transcript.md`: US scope, explicit fixed source policy, design-time expert validation distinct from runtime behavior, PubMed for literature and ClinicalTrials.gov for emerging development/organization roles. Source identities are not chosen dynamically by the model.

Actual credentials are read only from the ignored backend environment file; their values are deliberately absent from this source. The configured model variable was blank, so the implementation uses a configurable `gpt-4.1-mini` default, disclosed to the owner and verified with the supplied account. This request supersedes the earlier planning-only scope for implementation and replaces the proposed SQLite demo storage with PostgreSQL.
