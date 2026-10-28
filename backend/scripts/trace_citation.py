"""Read-only policy replay of stored source versions; no discovery/model calls or report mutation.

Run from backend: python -m scripts.trace_citation --run-id <id> --nct-id NCT01954147
"""

import argparse
from datetime import date
import json
from pathlib import Path

from sqlalchemy import select
from app.database import Session, ResearchRun, Citation, SourceSnapshot
from app.schemas import SourceDocument
from app.sources import parse_trial
from app.policy import rank_documents, validate_claim, POLICY_VERSION
from app.workflow import structured_claims


def trace(run_id, nct_id):
    with Session() as db:
        run = db.get(ResearchRun, run_id)
        if not run or not run.result:
            raise ValueError("Saved completed run required")
        before = run.result
        rows = list(db.scalars(select(Citation).where(Citation.run_id == run_id)))
        documents = []
        for row in rows:
            snapshot = db.get(SourceSnapshot, row.snapshot_id).data
            if row.data["source"] == "clinicaltrials":
                documents.append(parse_trial(snapshot, row.data["retrieved_at"]))
            else:
                fields = {k: v for k, v in row.data.items() if k in SourceDocument.model_fields}
                documents.append(
                    SourceDocument(
                        **fields,
                        snapshot=snapshot,
                        passages=[{"locator": e["locator"], "text": e["text"]} for e in row.data["evidence"]],
                    )
                )
        after = rank_documents(
            documents,
            run.condition,
            run_id,
            run.request.get("population", "general"),
            as_of=date.fromisoformat(before["as_of"][:10]),
        )
        accepted = structured_claims(after)
        withheld = []
        # Revalidate the original model claims against the same immutable source versions.
        for claim in before["claims"]:
            if claim["origin"] == "structured_source_fields":
                continue
            ok, reasons, _ = validate_claim(claim, after)
            (accepted if ok else withheld).append(
                claim if ok else {"text": claim["text"], "reason_codes": reasons}
            )
        old = next(c for c in before["citations"] if c["canonical_id"] == nct_id)
        new = next(c for c in after if c["canonical_id"] == nct_id)
        old_claims = [
            c for c in before["claims"] if any(r["citation_id"] == old["id"] for r in c["references"])
        ]
        new_claims = [
            c
            for c in accepted
            if any(r["evidence_id"] in {e["id"] for e in new["evidence"]} for r in c["references"])
        ]
        return {
            "mode": "saved_snapshot_policy_replay",
            "original_run_id": run_id,
            "request": run.request,
            "source_attempts": before["source_attempts"],
            "source_as_of": before["as_of"],
            "original_policy": before["policy_version"],
            "replay_policy": POLICY_VERSION,
            "new_source_or_model_calls": 0,
            "original_results_modified": False,
            "target": {
                "canonical_id": nct_id,
                "snapshot_hash": old["snapshot_hash"],
                "before": old,
                "after": {k: v for k, v in new.items() if k != "snapshot"},
                "before_claims": old_claims,
                "after_claims": new_claims,
                "selected_by_original_model": any(
                    old["id"] in t.get("citation_ids", []) for t in before["usage"]["tool_calls"]
                ),
            },
            "before_claim_count": len(before["claims"]),
            "after_claim_count": len(accepted),
            "replay_claims": accepted,
            "withheld_original_model_claims": withheld,
            "limitation": "This isolates changed parser/policy behavior on the original saved sources. It revalidates original model text; it is not a new live search or a new semantic review.",
        }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--nct-id", default="NCT01954147")
    args = parser.parse_args()
    result = trace(args.run_id, args.nct_id)
    output = Path("data") / f"trace-{args.nct_id.lower()}.json"
    output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(
        json.dumps(
            {
                "output": str(output),
                "policy": result["replay_policy"],
                "before_claims_for_target": len(result["target"]["before_claims"]),
                "after_claims_for_target": len(result["target"]["after_claims"]),
                "reasons": result["target"]["after"]["reason_codes"],
                "population": result["target"]["after"]["population"],
            },
            indent=2,
        )
    )
