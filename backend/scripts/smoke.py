"""Explicit live smoke run; prints no keys, URLs with keys, or upstream exception bodies."""

import asyncio, json, uuid
from pathlib import Path
from app.database import create_schema, Session, ResearchRun
from app.policy import POLICY_VERSION
from app.schemas import ResearchRequest
from app.sources import Sources
from app.workflow import execute


async def main():
    create_schema()
    payload = ResearchRequest(condition="Type 2 diabetes", scope_confirmed=True, max_records=8)
    run_id = str(uuid.uuid4())
    with Session.begin() as db:
        db.add(
            ResearchRun(
                id=run_id,
                condition=payload.condition,
                status="queued",
                mode="live",
                policy_version=POLICY_VERSION,
                request=payload.model_dump(),
            )
        )
    sources = Sources()
    try:
        result = await execute(run_id, payload, sources)
    finally:
        await sources.close()
    summary = {
        "run_id": run_id,
        "status": result["status"],
        "citations": len(result["citations"]),
        "claims": len(result["claims"]),
        "conflicts": len(result["conflicts"]),
        "excluded_claims": len(result["excluded_claims"]),
        "source_attempts": result["source_attempts"],
        "usage": result["usage"],
        "model": result["model"],
        "warnings": result["warnings"],
    }
    Path("data").mkdir(exist_ok=True)
    Path("data/smoke-result.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


asyncio.run(main())
