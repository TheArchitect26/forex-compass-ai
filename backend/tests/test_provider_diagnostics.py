import asyncio

from app.api.signals import provider_diagnostics
from app.config import settings
from app.engines.market_data import market_data
from app.utils_time import utc_now


def _run(coro):
    return asyncio.run(coro)


def _reset_diagnostics():
    market_data._symbol_results.clear()
    market_data._provider_last_success = None
    market_data._provider_last_error = None
    market_data._provider_last_error_message = None


def test_provider_diagnostics_endpoint_works(monkeypatch):
    _reset_diagnostics()
    monkeypatch.setattr(settings, "PAIRS", ["EUR/USD", "GBP/USD"])
    monkeypatch.setattr(settings, "TWELVE_DATA_API_KEY", "")

    payload = _run(provider_diagnostics())

    assert payload["provider_name"] == "twelve_data"
    assert payload["provider_configured"] is False
    assert len(payload["symbols"]) == 2
    assert payload["symbols"][0]["status"] == "unknown"
    assert payload["auto_trade"] is False
    assert payload["no_execution"] is True


def test_provider_diagnostics_reports_failed_symbols(monkeypatch):
    _reset_diagnostics()
    monkeypatch.setattr(settings, "PAIRS", ["AUD/USD"])
    monkeypatch.setattr(settings, "TWELVE_DATA_API_KEY", "secret-key")
    market_data.record_symbol_result(
        "AUD/USD",
        status="provider_failed",
        data_mode="unavailable",
        provider_name="twelve_data",
        last_error=utc_now(),
        last_error_message="Twelve Data rejected secret-key for AUD/USD",
    )

    item = _run(provider_diagnostics())["symbols"][0]

    assert item["symbol"] == "AUD/USD"
    assert item["status"] == "provider_failed"
    assert item["data_mode"] == "unavailable"
    assert item["last_error"] is not None
    assert "secret-key" not in item["last_error_message"]


def test_provider_diagnostics_reports_successful_symbols(monkeypatch):
    _reset_diagnostics()
    monkeypatch.setattr(settings, "PAIRS", ["EUR/USD"])
    monkeypatch.setattr(settings, "TWELVE_DATA_API_KEY", "configured")
    market_data.record_symbol_result(
        "EUR/USD",
        status="supported",
        data_mode="provider",
        provider_name="twelve_data",
        last_success=utc_now(),
    )

    payload = _run(provider_diagnostics())
    item = payload["symbols"][0]

    assert payload["provider_configured"] is True
    assert payload["last_success"] is not None
    assert item["symbol"] == "EUR/USD"
    assert item["status"] == "supported"
    assert item["data_mode"] == "provider"
    assert item["last_success"] is not None


def test_provider_diagnostics_exposes_no_trading_behavior(monkeypatch):
    _reset_diagnostics()
    monkeypatch.setattr(settings, "PAIRS", ["EUR/USD"])

    payload = _run(provider_diagnostics())
    forbidden = {"execute", "trade", "order", "broker", "position_size", "close_url"}

    assert payload["auto_trade"] is False
    assert payload["no_execution"] is True
    assert forbidden.isdisjoint(payload.keys())
    for item in payload["symbols"]:
        assert forbidden.isdisjoint(item.keys())


def test_provider_diagnostics_no_auto_trading_introduced(monkeypatch):
    _reset_diagnostics()
    monkeypatch.setattr(settings, "PAIRS", ["EUR/USD"])

    payload = _run(provider_diagnostics())

    assert payload["auto_trade"] is False
    assert payload["no_execution"] is True
