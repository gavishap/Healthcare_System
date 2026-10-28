"""Uses actual PostgreSQL inside one rolled-back transaction, not SQLite."""

import uuid
from app.database import create_schema, engine, ResearchRun, Citation, SourceSnapshot, EvidencePassage
from sqlalchemy.orm import Session
from app.policy import POLICY_VERSION


def test_postgres_persists_citation_to_snapshot_and_passage_chain():
    create_schema()
    unique = str(uuid.uuid4())
    connection = engine.connect()
    transaction = connection.begin()
    try:
        with Session(bind=connection) as db:
            db.add(
                ResearchRun(
                    id=unique,
                    condition="Synthetic storage test",
                    mode="fixture",
                    policy_version=POLICY_VERSION,
                    request={},
                )
            )
            db.flush()
            db.add(
                SourceSnapshot(
                    id=unique,
                    source="pubmed",
                    canonical_id="12345",
                    content_hash="0" * 64,
                    data={"abstract": "stored exact passage"},
                )
            )
            db.flush()
            db.add(Citation(id=unique, run_id=unique, snapshot_id=unique, data={"provenance": "test"}))
            db.flush()
            db.add(
                EvidencePassage(
                    id=unique,
                    citation_id=unique,
                    snapshot_id=unique,
                    locator="/abstract",
                    text="stored exact passage",
                )
            )
            db.flush()
            passage = db.get(EvidencePassage, unique)
            assert db.get(Citation, passage.citation_id).snapshot_id == passage.snapshot_id
            assert db.get(SourceSnapshot, passage.snapshot_id).data["abstract"] == passage.text
    finally:
        transaction.rollback()
        connection.close()
