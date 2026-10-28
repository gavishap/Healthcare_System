# Frontend workspace

- This repository is the frontend implementation workspace. The sibling `omnia-vault/` repository stores project knowledge; read its `AGENTS.md` and `_relay/STATE.md` for the shared handoff.
- Interface and evidence policy notes live in `omnia-vault/Wiki/Concepts/`. Keep application code in this repository.
- Never place OpenAI or NCBI credentials in frontend environment files, browser storage, source code, or bundles. The client talks to the backend.
- `VITE_API_BASE_URL` is a proposed public development setting, not a working server or a final framework decision.
- Show provenance, missing coverage and source limitations. Do not label trial registration as proven benefit or rank treatments as best for a patient.
