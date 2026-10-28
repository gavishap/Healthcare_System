from fastapi.testclient import TestClient
from pydantic import SecretStr
from app.main import app
from app.config import get_settings


def test_local_auth_protects_reports_without_exposing_upstream_credentials(monkeypatch):
    monkeypatch.setattr(get_settings(), "app_access_token", SecretStr("local-test-token"))
    client = TestClient(app)  # No lifespan restart or mutation of active worker jobs.
    assert client.get("/api/policy").status_code == 401
    assert client.get("/api/health").json()["storage"] == "postgresql"
    response = client.get("/api/policy", headers={"Authorization": "Bearer local-test-token"})
    assert response.status_code == 200
    assert "OPENAI_API_KEY" not in response.text
    assert "NCBI_API_KEY" not in response.text


def test_discovery_boundary_accepts_identifiers_not_urls_or_caller_authority_flags():
    client = TestClient(app)
    body = {
        "condition": "diabetes",
        "scope_confirmed": True,
        "pmids": ["12345"],
        "url": "http://127.0.0.1/private",
        "verified": True,
    }
    assert client.post("/api/evidence/process", json=body).status_code == 422
    body = {"condition": "diabetes", "scope_confirmed": True, "pmids": ["1234;sql"]}
    assert client.post("/api/evidence/process", json=body).status_code == 422
    assert (
        client.post(
            "/api/evidence/process", json={"condition": "diabetes", "scope_confirmed": True}
        ).status_code
        == 422
    )


def test_no_source_is_fetched_for_an_explicitly_empty_identifier_list():
    import asyncio
    from app.sources import Sources

    async def check():
        sources = Sources()
        try:
            assert (await sources.pubmed("diabetes", 8, []))[1]["status"] == "not_attempted"
            assert (await sources.trials("diabetes", 8, []))[1]["status"] == "not_attempted"
        finally:
            await sources.close()

    asyncio.run(check())
