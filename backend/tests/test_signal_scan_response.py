from app.config import settings


class _FakeDb:
    async def commit(self):
        return None


def test_mixed_scan_response_counts_and_provider_failures(monkeypatch):
    import asyncio
    from app.api import signals as signals_api
    from app.engines.market_data import market_data

    market_data._symbol_results.clear()
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

    payload = asyncio.run(signals_api.scan(db=_FakeDb(), _user="test"))

    assert payload["data_mode"] == "mixed"
    assert payload["real_count"] == 1
    assert payload["cached_count"] == 1
    assert payload["synthetic_demo_count"] == 1
    assert payload["unavailable_count"] == 1
    assert payload["provider_failed_symbols"] == ["AUD/USD"]
    assert payload["auto_trade"] is False
    assert payload["no_execution"] is True

    diagnostics = market_data.provider_diagnostics(settings.PAIRS)
    by_symbol = {item["symbol"]: item for item in diagnostics["symbols"]}
    assert by_symbol["EUR/USD"]["status"] == "supported"
    assert by_symbol["GBP/USD"]["status"] == "cached"
    assert by_symbol["USD/JPY"]["data_mode"] == "synthetic_demo"
    assert by_symbol["AUD/USD"]["status"] == "provider_failed"
    assert by_symbol["AUD/USD"]["data_mode"] == "unavailable"
