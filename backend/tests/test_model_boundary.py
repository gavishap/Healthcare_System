import uuid
from app import workflow
from app.database import Session, ResearchRun, create_schema
from app.fixtures import fixture_documents
from app.policy import POLICY_VERSION
from app.schemas import ResearchRequest, Extraction


async def test_uncited_model_limitations_do_not_bypass_the_claim_evidence_gate(monkeypatch):
    class FakeModel:
        usage = []
        tool_calls = []

        async def extract(self, *args):
            return Extraction(
                claims=[], limitations=["Uncited clinical conclusion that must not appear as a report fact."]
            )

        async def review(self, *args):
            return {}

    class FakeSources:
        async def collect(self, *args, **kwargs):
            return fixture_documents("Type 2 diabetes"), [{"source": "test", "status": "success"}]

    monkeypatch.setattr(workflow, "EvidenceModel", FakeModel)
    create_schema()
    run_id = str(uuid.uuid4())
    payload = ResearchRequest(condition="Type 2 diabetes", scope_confirmed=True, use_llm=True)
    with Session.begin() as db:
        db.add(
            ResearchRun(
                id=run_id,
                condition="diabetes",
                mode="live",
                policy_version=POLICY_VERSION,
                request=payload.model_dump(),
            )
        )
    try:
        result = await workflow.execute(run_id, payload, FakeSources())
        assert not result["claims"]
        assert all("Uncited clinical conclusion" not in w for w in result["warnings"])
        assert any("uncited model limitation notes were withheld" in w for w in result["warnings"])
    finally:
        with Session.begin() as db:
            db.delete(db.get(ResearchRun, run_id))
