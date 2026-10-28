import uuid
from app.database import (
    create_schema,
    Session,
    ResearchRun,
    ClaimEvidence,
    EvidencePassage,
    SourceSnapshot,
    Citation,
)
from app.policy import POLICY_VERSION
from app.schemas import ResearchRequest
from app.sources import Sources
from app.workflow import execute
from sqlalchemy import select


async def test_fixture_conflict_round_trip_uses_real_postgres_and_preserves_quotes():
    create_schema()
    payload = ResearchRequest(condition="Type 2 diabetes", scope_confirmed=True, mode="fixture")
    run_id = str(uuid.uuid4())
    with Session.begin() as db:
        db.add(
            ResearchRun(
                id=run_id,
                condition=payload.condition,
                mode="fixture",
                policy_version=POLICY_VERSION,
                request=payload.model_dump(),
            )
        )
    sources = Sources()
    try:
        result = await execute(run_id, payload, sources)
    finally:
        await sources.close()
    assert result["mode"] == "fixture"
    assert len(result["claims"]) == 2 and len(result["conflicts"]) == 1
    assert result["coverage"]["current_care"]["status"] == "unavailable"
    assert result["usage"]["model_requests"] == 0
    with Session() as db:
        for claim in result["claims"]:
            for ref in db.scalars(select(ClaimEvidence).where(ClaimEvidence.claim_id == claim["id"])):
                passage = db.get(EvidencePassage, ref.evidence_id)
                assert ref.quote in passage.text
                assert db.get(Citation, passage.citation_id).run_id == run_id
                assert db.get(SourceSnapshot, passage.snapshot_id).content_hash == ref.check["snapshot_hash"]
        assert db.get(ResearchRun, run_id).status == "partial"
    with Session.begin() as db:
        db.delete(db.get(ResearchRun, run_id))
