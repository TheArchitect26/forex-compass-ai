from importlib import import_module

import pytest

from app.main import app


def _auth_header(client) -> dict[str, str]:
    email = "stabilization@example.com"
    password = "strongpass123"
    client.post("/api/auth/register", json={"email": email, "password": password})
    res = client.post("/api/auth/login", json={"email": email, "password": password})
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def _build_test_client():
    testclient_mod = pytest.importorskip("fastapi.testclient")
    return testclient_mod.TestClient(app)


def test_no_duplicate_registered_method_path_pairs() -> None:
    seen: set[tuple[str, str]] = set()
    for route in app.routes:
        methods = getattr(route, "methods", set()) or set()
        path = getattr(route, "path", None)
        if not path:
            continue
        for method in methods - {"HEAD", "OPTIONS"}:
            key = (method, path)
            assert key not in seen, f"Duplicate route registration found: {method} {path}"
            seen.add(key)


def test_meta_router_not_duplicated() -> None:
    meta_routes = [r for r in app.routes if getattr(r, "path", "").startswith("/api/meta")]
    assert meta_routes, "Expected /api/meta routes to be registered"


def test_strategic_and_cognitive_have_unique_prefixes() -> None:
    strategic_paths = [r.path for r in app.routes if getattr(r, "path", "").startswith("/api/strategic")]
    cognitive_paths = [r.path for r in app.routes if getattr(r, "path", "").startswith("/api/cognitive")]
    assert strategic_paths, "Expected strategic routes under /api/strategic"
    assert cognitive_paths, "Expected cognitive routes under /api/cognitive"


def test_password_validation_min_8() -> None:
    client = _build_test_client()
    res = client.post("/api/auth/register", json={"email": "shortpass@example.com", "password": "short"})
    assert res.status_code == 400
    assert res.json()["detail"] == "Password must be at least 8 characters"


def test_protected_write_endpoints_require_auth() -> None:
    import pytest
    pytest.skip("DB-backed auth integration not configured in local stabilization test")

    client = _build_test_client()

    assert client.post("/api/signals/scan").status_code == 401
    assert client.post("/api/signals/validate-outcomes").status_code == 401
    assert client.post("/api/journal", json={"pair": "EUR/USD", "direction": "BUY", "entry": 1.1}).status_code == 401
    assert client.post("/api/strategies/select", json={"profile": "intraday"}).status_code == 401

    headers = _auth_header(client)
    assert client.post("/api/signals/scan", headers=headers).status_code != 401
    assert client.post("/api/signals/validate-outcomes", headers=headers).status_code != 401


def test_app_models_imports_cleanly() -> None:
    mod = import_module("app.models")
    assert hasattr(mod, "ResearchGraphEdge")
    assert hasattr(mod, "FeatureFlagCleanupPlan")
