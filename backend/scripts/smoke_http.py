"""Run the actual Docker/API workflow using the configured backend keys; print sanitized evidence counts."""

import json, time
from pathlib import Path
import httpx
from app.config import get_settings

settings = get_settings()
token = settings.app_access_token.get_secret_value()
headers = {"Authorization": "Bearer " + token} if token else {}
with httpx.Client(base_url="http://localhost:8000", headers=headers, timeout=10) as client:
    response = client.post(
        "/api/research-runs",
        json={
            "condition": "Type 2 diabetes",
            "scope_confirmed": True,
            "mode": "live",
            "use_llm": True,
            "max_records": 8,
        },
    )
    response.raise_for_status()
    run_id = response.json()["id"]
    print("Started live API run " + run_id, flush=True)
    deadline = time.monotonic() + 170
    while time.monotonic() < deadline:
        response = client.get("/api/research-runs/" + run_id)
        response.raise_for_status()
        run = response.json()
        if run["status"] not in {"queued", "running"}:
            break
        time.sleep(1)
    result = run.get("result")
    if not result:
        raise RuntimeError("No completed result before smoke deadline: " + run["status"])
    summary = {
        "run_id": run_id,
        "status": run["status"],
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
    Path("data/smoke-http.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    Path("data/smoke-result.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
