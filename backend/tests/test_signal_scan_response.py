from app.config import settings
from app.main import app


def test_mixed_scan_response_counts_and_provider_failures(monkeypatch):
    from app.api import signals as signals_api
    from fastapi.testclient import TestClient

    monkeypatch.setattr(settings, "ALLOW_ANONYMOUS_AUTH", True)
    monkeypatch.setattr(settings, "PAIRS", ["EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD"])

    async def fake_pipeline(_db, pair, source="api_scan", report_unavailable=False):
        if pair == "EUR/USD":
            return {"pair": pair, "direction": "BUY", "data_source": "real", "data_mode": "provider", "provider_name": "twelve_data", "demo_only": False}
        if pair == "GBP/USD":
            return {"pair": pair, "direction": "SELL", "data_source": "real", "data_mode": "cached", "provider_name": "cached_provider", "demo_only": False}
        if pair == "USD/JPY":
            return {"pair": pair, "direction": "HOLD", "data_source": "synthetic", "data_mode": "synthetic_demo", "provider_name": "synthetic", "demo_only": True, "execution_grade": False}
        return {"pair": pair, "direction": "UNAVAILABLE", "data_source": "unavailable", "data_mode": "unavailable", "provider_name": "twelve_data", "provider_failed": True, "demo_only": False, "execution_grade": False}

    monkeypatch.setattr(signals_api, "run_signal_pipeline_for_pair", fake_pipeline)

    payload = TestClient(app).post("/api/signals/scan").json()

    assert payload["data_mode"] == "mixed"
    assert payload["real_count"] == 1
    assert payload["cached_count"] == 1
    assert payload["synthetic_demo_count"] == 1
    assert payload["unavailable_count"] == 1
    assert payload["provider_failed_symbols"] == ["AUD/USD"]
    assert payload["auto_trade"] is False
    assert payload["no_execution"] is True
