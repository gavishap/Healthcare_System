# Healthcare System Frontend

Evidence Desk is a React/TypeScript/Vite analyst workbench. It includes condition/scope confirmation, actual run progress, saved research, a cited briefing, deterministic citation register, source/evidence drawer, potential conflicts, policy explanation and Markdown/JSON exports. The backend and Postgres contain all model credentials and storage.

## Run locally

Preferred complete setup: from the sibling backend repository run `docker compose up -d --build`, then open [Evidence Desk](http://localhost:5173).

For frontend development use `npm ci` and `npm run dev` with the backend on port 8000. Vite proxies `/api` to the backend. Optional `VITE_API_BASE_URL` overrides that public endpoint for local development; the Docker image uses the same-origin Nginx proxy. Production build: `npm run build`.

The optional local application token is held in memory only. It is unrelated to OpenAI/NCBI keys. Fonts are self-hosted in the build; the app has no third-party script or font dependency at runtime.

## Product boundaries

Source identity/provenance checks and automated claim support are distinct from clinical correctness. The current slice deliberately shows standard-of-care coverage as unavailable because no checked applicable guideline is connected. Trial registration is not approval or benefit. Conflict detection is bounded and exact-match-based; no finding of conflict is not scientific consensus. Synthetic examples are conspicuously labeled and not presented as live publications.

Design follows the vault's UI/UX Pro Max guidance with an application-specific direction in `DESIGN.md`: restrained teal, readable data tables, text-based status, focus-managed native evidence dialog, keyboard tab navigation, responsive views and reduced motion.


## Local configuration

The ignored `.env` file contains the public development setting `VITE_API_BASE_URL=http://127.0.0.1:8000`. Docker runs the API at this local address, while its frontend image uses the same-origin `/api` proxy and does not copy `.env` into the build.

Frontend build-time environment values can become visible in browser assets. Store OpenAI and NCBI credentials only in `backend/.env`; the frontend should call the backend for sourcing. The committed `.env.example` contains public settings only.

## Integration context

The Obsidian workspace contains this repository, `backend/`, and `omnia-vault/` as sibling folders. Interface and evidence policy planning live under `omnia-vault/Wiki/Concepts/`:

- `healthcare-briefing-interface.md`
- `healthcare-sourcing-contract.md`
- `healthcare-evidence-policy.md`

The interface presents condition research for a U.S. health system strategy team, including source provenance, development stages, organization roles, conflicts and missing coverage. It does not provide patient-specific treatment recommendations.

## Browser verification

`scripts/verify-ui.cjs` runs isolated headless browser checks. Install `playwright` locally or set `PLAYWRIGHT_MODULE` to an available bundled module. Set `PLAYWRIGHT_BROWSER_CHANNEL=msedge` or `chrome` to use an installed browser if the Playwright browser is unavailable. Run `node scripts/verify-ui.cjs` after the live backend smoke run. Screenshots and the verification report go into ignored `data/`.

There is no remote configured. Create or attach the intended remote separately.
