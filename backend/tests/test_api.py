from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_health_is_small_and_sanitized() -> None:
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "mode": "synthetic-demo"}


def test_workspace_contract_and_security_headers() -> None:
    response = client.get("/api/workspace?scenario=baseline")
    assert response.status_code == 200
    body = response.json()
    assert body["scenario"] == "baseline"
    assert set(body) == {
        "scenario",
        "generated_at",
        "recommendation",
        "alternatives",
        "attention",
        "sources",
    }
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["content-security-policy"].startswith("default-src 'self'")


def test_invalid_scenario_fails_closed_without_internal_details() -> None:
    response = client.get("/api/workspace?scenario=unknown")
    assert response.status_code == 422
    text = response.text.lower()
    assert "traceback" not in text
    assert "invalid scenario" in text


def test_bounded_query_rejects_oversized_input() -> None:
    response = client.get("/api/workspace?scenario=" + "x" * 80)
    assert response.status_code == 422


def test_api_has_no_mutation_or_proxy_surface() -> None:
    schema = client.get("/openapi.json").json()
    paths = schema["paths"]
    assert set(paths) == {"/api/health", "/api/workspace"}
    assert all(set(operations) <= {"get"} for operations in paths.values())
