# Healthcare System Backend

FastAPI service for a US health system strategy research prototype. It retrieves canonical PubMed/NCBI and ClinicalTrials.gov records, screens and orders citations, preserves snapshots/passages, performs bounded OpenAI extraction and support review, detects potential opposing findings, and stores the result in PostgreSQL.

## Run the complete local application

From this backend repository:

```powershell
docker compose up -d --build
```

Open [Evidence Desk](http://localhost:5173) and [API documentation](http://localhost:8000/docs). All published ports bind to loopback. PostgreSQL uses port 55432 and a named volume, so it does not replace an existing database on 5432. Stop without deleting the volume using `docker compose stop`. Do not use `down -v` unless intentionally discarding this application's saved evidence.

Compose reads the existing ignored `.env` for upstream keys. Neither Docker build context includes secret environment files. The database's default password is a public local-development value; set `POSTGRES_PASSWORD` and the corresponding host `DATABASE_URL` before any shared deployment.

For host development, start only PostgreSQL with `docker compose up -d postgres`, run `uv sync --extra dev`, then `uv run uvicorn app.main:app --host 127.0.0.1 --port 8000 --no-access-log`. Do not run two API instances against this prototype database: local background jobs have a single-process recovery model.

## Evidence and model policy

- Fixed upstream hosts, canonical PMID/NCT matching, source version hashes and exact snapshot locators establish source provenance. NCBI indexing is not medical endorsement.
- Rules run outside the model: retractions/source mismatch are excluded; evidence class, question match, results and source dates determine research ordering. There is no opaque numerical truth score.
- Every accepted claim links through `claim_evidence` to a saved `evidence_passage` and `source_snapshot`. Exact quotes are checked; generated claims also undergo an automated semantic support review. This remains probabilistic and needs analyst/domain review.
- Registry records without results support development/organization statements only. No guideline or FDA adapter is implemented in this slice, so current standard-of-care and approval claims are withheld. The UI displays the coverage gap.
- Claims with opposing directions for the same extracted intervention/population/outcome are preserved and flagged as potential conflicts, with no winner chosen. Exact matching can miss synonyms or nuanced disagreements. No detected conflict does not mean consensus.
- Explicit NCT identifiers link study families. DOI links identify the same publication; unknown underlying-study overlap remains unknown.
- OpenAI performs one strict `get_evidence_passages` function-tool round trip, schema-constrained extraction, then a fresh support-review request. At most three model requests; bounded input/output, record limits, source retries and run deadline. No provider fallback, arbitrary fetch or dynamic authority selection.
- Synthetic fixture mode is explicitly labeled and never substituted for failed live retrieval. Its fictitious source IDs are not real publications.

## Integration after the sourcing layer

`POST /api/evidence/process` accepts discovered canonical identifiers and re-fetches them from fixed APIs before admission. It does not trust caller-supplied abstracts, source-authority flags or citation URLs.

```json
{
  "condition": "Type 2 diabetes",
  "jurisdiction": "US",
  "scope_confirmed": true,
  "mode": "live",
  "use_llm": true,
  "max_records": 12,
  "pmids": ["12345678"],
  "nct_ids": []
}
```

The identifiers above illustrate shape, not a verified diabetes source. Response: 202 with run ID. Poll `GET /api/research-runs/{id}`. The same pipeline can perform its own discovery via `POST /api/research-runs`, without the identifier fields.

Other endpoints: `GET /api/policy`, `GET /api/citations/{id}`, `GET /api/citations/{id}/snapshot`, and `GET /api/research-runs/{id}/export?format=markdown|json`. The export retains source IDs, quotations, locators, hashes, coverage and policy version. Protected endpoints optionally require `Authorization: Bearer <APP_ACCESS_TOKEN>`; do not use an upstream API key as the application token. This is a local single-workspace token, not tenant identity/authorization.

## Verification

```powershell
uv run pytest -q
uv run ruff check app tests scripts --select F
uv run python scripts/smoke.py
```

Tests use real PostgreSQL; the storage test rolls back its transaction and workflow tests clean up their own run rows. The live smoke command calls the configured APIs and incurs bounded model usage; it writes a sanitized result summary under ignored `data/`. With Docker already running, `uv run python scripts/smoke_http.py` verifies the actual API/worker path. Never print `.env` or raw upstream authentication errors.

Schema bootstrap is serialized with a Postgres advisory lock. Versioned production migrations, durable queue/worker leases, tenant access, source-license review and clinical policy validation remain future pilot work. A process restart marks unfinished jobs interrupted; it does not fabricate completion. Do not call the prototype production-ready.

## Local configuration

The ignored `.env` file already exists. Fill in `OPENAI_API_KEY` and `NCBI_API_KEY` there, and set `OPENAI_MODEL` when a model is selected. `NCBI_EMAIL` is an optional contact address for NCBI requests. The committed `.env.example` documents the variable names without credentials.

Settings explicitly load `.env` with environment-variable overrides. `OPENAI_MODEL` defaults to `gpt-4.1-mini` when blank; set a different supported model explicitly. Keep credentials on the backend and redact them from logs, URLs, errors, fixtures and snapshots.

## Integration context

The Obsidian workspace contains this repository, `frontend/`, and `omnia-vault/` as sibling folders. Planning notes live in the Omnia repository:

- `Wiki/Concepts/healthcare-sourcing-plan.md`
- `Wiki/Concepts/healthcare-sourcing-contract.md`
- `Wiki/Concepts/healthcare-application-architecture.md`

The runtime implements OpenAI and NCBI/PubMed access plus ClinicalTrials.gov records/roles. Applicable U.S. guidelines and FDA records remain planned sources with explicit coverage gaps. The implemented processing seam is documented above and in the vault's `healthcare-evidence-runtime.md` note.

There is no remote configured. Create or attach the intended remote separately; do not use the Omnia template remote for application code.
