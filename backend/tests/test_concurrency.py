"""Concurrent runs must reuse immutable snapshots without losing either report."""

from concurrent.futures import ThreadPoolExecutor
import uuid
from app.database import create_schema, Session, ResearchRun, Citation, SourceSnapshot
from app.fixtures import fixture_documents
from app.policy import rank_documents, POLICY_VERSION
from app.workflow import store_result


def test_concurrent_snapshot_admission_is_atomic():
    create_schema()
    run_ids = [str(uuid.uuid4()), str(uuid.uuid4())]
    doc = fixture_documents("diabetes")[0]
    doc.snapshot["test_nonce"] = str(uuid.uuid4())
    bundles = [rank_documents([doc], "diabetes", r) for r in run_ids]
    with Session.begin() as db:
        for r in run_ids:
            db.add(
                ResearchRun(
                    id=r, condition="diabetes", mode="fixture", policy_version=POLICY_VERSION, request={}
                )
            )
    try:
        with ThreadPoolExecutor(max_workers=2) as pool:
            futures = [
                pool.submit(store_result, r, {"claims": [], "conflicts": [], "status": "partial"}, b)
                for r, b in zip(run_ids, bundles)
            ]
            for f in futures:
                f.result()
        with Session() as db:
            assert all(db.get(Citation, b[0]["id"]) for b in bundles)
            assert db.get(SourceSnapshot, bundles[0][0]["snapshot_id"])
            assert bundles[0][0]["snapshot_id"] == bundles[1][0]["snapshot_id"]
    finally:
        with Session.begin() as db:
            for r in run_ids:
                row = db.get(ResearchRun, r)
                if row:
                    db.delete(row)
            db.flush()
            snapshot = db.get(SourceSnapshot, bundles[0][0]["snapshot_id"])
            if snapshot:
                db.delete(snapshot)
