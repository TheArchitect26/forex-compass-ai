import asyncio

import pytest

from app.config import settings
from app.main import app


def _client():
    testclient_mod = pytest.importorskip("fastapi.testclient")
    return testclient_mod.TestClient(app)


def test_production_no_provider_status_clarity(monkeypatch) -> None:
    monkeypatch.setattr(settings, "APP_ENV", "production")
    monkeypatch.setattr(settings, "TWELVE_DATA_API_KEY", "")
    monkeypatch.setattr(settings, "ALLOW_SYNTHETIC_SIGNALS", False)

    res = _client().get("/api/signals/status")

    assert res.status_code == 200
    payload = res.json()
    assert payload["scanner_ready"] is False
    assert payload["live_data_ready"] is False
    assert payload["execution_ready"] is False
    assert payload["demo_only"] is True
    assert payload["data_mode"] == "synthetic_demo"
    assert payload["market_data"]["mode"] == "synthetic_demo"
    assert payload["synthetic_buy_sell_blocked"] is True
    assert payload["auto_trade"] is False
    assert payload["no_execution"] is True
    assert payload["advisory_only"] is True


def test_local_synthetic_fallback_is_demo_labelled(monkeypatch) -> None:
    monkeypatch.setattr(settings, "APP_ENV", "test")
    monkeypatch.setattr(settings, "TWELVE_DATA_API_KEY", "")

    payload = _client().get("/api/signals/status").json()

    assert payload["scanner_ready"] is True
    assert payload["live_data_ready"] is False
    assert payload["execution_ready"] is False
    assert payload["demo_only"] is True
    assert payload["data_mode"] == "synthetic_demo"
    assert payload["advisory_only"] is True


def test_scan_requires_auth_in_production_without_provider(monkeypatch) -> None:
    monkeypatch.setattr(settings, "APP_ENV", "production")
    monkeypatch.setattr(settings, "TWELVE_DATA_API_KEY", "")
    monkeypatch.setattr(settings, "ALLOW_ANONYMOUS_AUTH", False)

    res = _client().post("/api/signals/scan")

    assert res.status_code in {401, 403}


def test_validate_outcomes_requires_auth_in_production(monkeypatch) -> None:
    monkeypatch.setattr(settings, "APP_ENV", "production")
    monkeypatch.setattr(settings, "ALLOW_ANONYMOUS_AUTH", False)

    res = _client().post("/api/signals/validate-outcomes")

    assert res.status_code in {401, 403}


def test_synthetic_buy_sell_blocked_in_production_without_provider(monkeypatch) -> None:
    from app.engines import pipeline

    monkeypatch.setattr(settings, "APP_ENV", "production")
    monkeypatch.setattr(settings, "TWELVE_DATA_API_KEY", "")
    monkeypatch.setattr(settings, "ALLOW_SYNTHETIC_SIGNALS", True)

    async def fake_profile(_db):
        return {"name": "intraday", "min_confidence": 60, "cooldown_minutes": 30}

    async def fake_analyze_pair(_pair):
        return {
            "signal": {
                "pair": "EUR/USD",
                "direction": "BUY",
                "timeframe": "15min",
                "confidence": 85,
                "strength": "strong",
                "risk_level": "low",
                "reason_summary": "synthetic test signal",
                "data_source": "synthetic",
            }
        }

    monkeypatch.setattr(pipeline, "get_active_profile", fake_profile)
    monkeypatch.setattr(pipeline, "analyze_pair", fake_analyze_pair)

    assert asyncio.run(pipeline.run_signal_pipeline_for_pair(object(), "EUR/USD")) is None
