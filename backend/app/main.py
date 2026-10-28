from contextlib import asynccontextmanager
import asyncio, json, secrets, uuid
from fastapi import FastAPI, Depends, HTTPException, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from sqlalchemy import select, text
from .config import get_settings
from .database import Session, engine, initialize, ResearchRun, RunEvent, Citation, SourceSnapshot
from .policy import POLICY_VERSION, RANKING_RULES
from .schemas import ResearchRequest, ProcessRequest
from .sources import Sources
from .workflow import execute
from .reporting import safe_markdown, source_link
from .scope import resolve_scope, ScopeAmbiguity

tasks: set[asyncio.Task] = set()


@asynccontextmanager
async def lifespan(app):
    initialize()
    app.state.sources = Sources()
    try:
        yield
    finally:
        for task in tasks:
            task.cancel()
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
        await app.state.sources.close()


app = FastAPI(title="Evidence Desk", version="0.1.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_settings().allowed_origins.split(","),
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)


def authorize(authorization: str | None = Header(default=None)):
    expected = get_settings().app_access_token.get_secret_value()
    if expected and (not authorization or not secrets.compare_digest(authorization, "Bearer " + expected)):
        raise HTTPException(
            401, "A local application access token is required. Do not enter OpenAI or NCBI keys here."
        )


@app.get("/api/health")
def health():
    try:
        with engine.connect() as db:
            db.execute(text("SELECT 1"))
    except Exception:
        raise HTTPException(503, "PostgreSQL unavailable") from None
    return {
        "status": "ok",
        "storage": "postgresql",
        "auth_required": bool(get_settings().app_access_token.get_secret_value()),
        "policy_version": POLICY_VERSION,
    }


@app.get("/api/policy", dependencies=[Depends(authorize)])
def policy():
    return {
        "version": POLICY_VERSION,
        "criteria": RANKING_RULES,
        "source_registry": [
            {
                "id": "pubmed",
                "host": "eutils.ncbi.nlm.nih.gov",
                "role": "Published literature; indexing is not endorsement",
            },
            {
                "id": "clinicaltrials",
                "host": "clinicaltrials.gov",
                "role": "Trial development and documented organization roles",
            },
        ],
        "conflict_rule": "Preserve opposing evidence; flag matching intervention/population/outcome, require analyst review, never vote or average.",
        "scope": "US strategy research; no patient data or individualized recommendations.",
        "model": get_settings().model_name(),
        "model_configured": bool(get_settings().openai_api_key.get_secret_value()),
        "ncbi_key_configured": bool(get_settings().ncbi_api_key.get_secret_value()),
    }


async def create_run(payload, request):
    try:
        resolve_scope(payload.condition, payload.population, allow_ambiguous=payload.mode == "fixture")
    except ScopeAmbiguity as exc:
        raise HTTPException(422, str(exc)) from None
    if len(tasks) >= get_settings().max_active_runs:
        raise HTTPException(
            429, "Local worker is busy. Wait for an active run to finish.", headers={"Retry-After": "10"}
        )
    if payload.mode == "fixture" and isinstance(payload, ProcessRequest):
        raise HTTPException(422, "Explicit identifiers require live verification.")
    run_id = str(uuid.uuid4())
    with Session.begin() as db:
        db.add(
            ResearchRun(
                id=run_id,
                condition=payload.condition,
                status="queued",
                mode=payload.mode,
                policy_version=POLICY_VERSION,
                request=payload.model_dump(),
            )
        )
    task = asyncio.create_task(execute(run_id, payload, request.app.state.sources))
    tasks.add(task)
    task.add_done_callback(tasks.discard)
    return {"id": run_id, "status": "queued"}


@app.post("/api/research-runs", status_code=202, dependencies=[Depends(authorize)])
async def research(payload: ResearchRequest, request: Request):
    return await create_run(payload, request)


@app.post("/api/evidence/process", status_code=202, dependencies=[Depends(authorize)])
async def process(payload: ProcessRequest, request: Request):
    """Integration boundary after discovery: re-fetch canonical IDs instead of trusting caller-supplied text."""
    if not payload.pmids and not payload.nct_ids:
        raise HTTPException(422, "Provide discovered pmids or nct_ids.")
    return await create_run(payload, request)


@app.get("/api/research-runs", dependencies=[Depends(authorize)])
def list_runs():
    with Session() as db:
        return [
            {
                "id": r.id,
                "condition": r.condition,
                "status": r.status,
                "mode": r.mode,
                "created_at": r.created_at.isoformat(),
            }
            for r in db.scalars(select(ResearchRun).order_by(ResearchRun.created_at.desc()).limit(25))
        ]


@app.get("/api/research-runs/{run_id}", dependencies=[Depends(authorize)])
def get_run(run_id: str):
    with Session() as db:
        run = db.get(ResearchRun, run_id)
        if not run:
            raise HTTPException(404, "Research run not found")
        events = db.scalars(select(RunEvent).where(RunEvent.run_id == run_id).order_by(RunEvent.id)).all()
        return {
            "id": run.id,
            "condition": run.condition,
            "status": run.status,
            "mode": run.mode,
            "created_at": run.created_at.isoformat(),
            "finished_at": run.finished_at.isoformat() if run.finished_at else None,
            "events": [
                {"stage": e.stage, "message": e.message, "created_at": e.created_at.isoformat()}
                for e in events
            ],
            "result": run.result,
        }


@app.get("/api/citations/{citation_id}", dependencies=[Depends(authorize)])
def get_citation(citation_id: str):
    with Session() as db:
        row = db.get(Citation, citation_id)
        if not row:
            raise HTTPException(404, "Citation not found")
        return {**row.data, "mode": db.get(ResearchRun, row.run_id).mode}


@app.get("/api/citations/{citation_id}/snapshot", dependencies=[Depends(authorize)])
def snapshot(citation_id: str):
    with Session() as db:
        row = db.get(Citation, citation_id)
        if not row:
            raise HTTPException(404, "Citation not found")
        snap = db.get(SourceSnapshot, row.snapshot_id)
        return {"snapshot_id": snap.id, "content_hash": snap.content_hash, "data": snap.data}


@app.get("/api/research-runs/{run_id}/export", dependencies=[Depends(authorize)])
def export(run_id: str, format: str = "markdown"):
    report = get_run(run_id)
    result = report["result"]
    if not result:
        raise HTTPException(409, "A completed evidence bundle is not available yet")
    filename = "evidence-briefing-" + run_id[:8]
    if format == "json":
        return Response(
            json.dumps(report, ensure_ascii=False, indent=2),
            media_type="application/json",
            headers={"Content-Disposition": f'attachment; filename="{filename}.json"'},
        )
    if format != "markdown":
        raise HTTPException(422, "Choose markdown or json")
    lines = [
        f"# {report['condition']} — evidence briefing",
        f"Mode: {result['mode']} | Scope: US | As of: {result['as_of']} | Policy: {result['policy_version']}",
        "Strategy research; automated checks do not establish clinical correctness.",
        "\n## Coverage and limitations",
    ]
    lines.extend("- " + safe_markdown(w) for w in result["warnings"])
    lines.extend(["\n## Standard of care", safe_markdown(result["coverage"]["current_care"]["reason"])])
    citations = {c["id"]: c for c in result["citations"]}
    for section, title in [
        ("care_landscape", "Published care evidence"),
        ("emerging", "Emerging development"),
        ("organizations", "Companies and institutions"),
        ("specific_populations", "Specific populations — separate evidence"),
    ]:
        lines.append("\n## " + title)
        section_claims = [c for c in result["claims"] if c["section"] == section]
        if not section_claims:
            lines.append(
                "No supported generated claim available. Inspect the source evidence and coverage limitations."
            )
        for claim in section_claims:
            lines.append("\n" + safe_markdown(claim["text"]))
            for ref in claim["references"]:
                c = citations[ref["citation_id"]]
                lines.extend(
                    [
                        f"- {source_link(c, c['canonical_id'], synthetic=result['mode'] == 'fixture')} — {ref['locator']}; snapshot SHA-256 `{ref['snapshot_hash']}`",
                        "> " + safe_markdown(ref["quote"]).replace("\n", "\n> "),
                    ]
                )
    lines.append("\n## Conflicting evidence")
    lines.extend(safe_markdown(c["summary"] + " " + c["resolution"]) for c in result["conflicts"])
    if not result["conflicts"]:
        lines.append(
            "No matching opposing finding was detected in this bounded extraction. This does not establish consensus."
        )
    lines.append("\n## Source register")
    for c in result["citations"]:
        lines.append(
            f"- {c['rank']}. {source_link(c, c['title'], synthetic=result['mode'] == 'fixture')} | {c['evidence_class']} | source date: {c['updated_date'] or c['published_date'] or 'unknown'} | retrieved: {c['retrieved_at']} | {', '.join(c['reason_codes'])}"
        )
    return Response(
        "\n\n".join(lines),
        media_type="text/markdown",
        headers={"Content-Disposition": f'attachment; filename="{filename}.md"'},
    )
