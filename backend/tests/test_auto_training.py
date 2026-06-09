import asyncio
from types import SimpleNamespace

from app.config import settings
from app.engines import auto_training


def _run(coro):
    return asyncio.run(coro)


class _FakeDb:
    def __init__(self):
        self.added = []

    def add(self, item):
        self.added.append(item)

    async def flush(self):
        for item in self.added:
            if getattr(item, "id", None) is None and item.__class__.__name__ == "TrainingRun":
                item.id = 1
                item.total_scans = item.total_scans or 0
                item.provider_backed_signals = item.provider_backed_signals or 0
                item.synthetic_skipped = item.synthetic_skipped or 0
                item.unavailable_skipped = item.unavailable_skipped or 0

    async def commit(self):
        return None


def _sample(symbol, direction, *, execution_grade=True, data_mode="provider", demo_only=False):
    return SimpleNamespace(
        symbol=symbol,
        direction=direction,
        execution_grade=execution_grade,
        data_mode=data_mode,
        demo_only=demo_only,
    )


def test_training_config_is_disabled_and_safe_by_default():
    assert settings.AUTO_TRAINING_ENABLED is False
    assert settings.AUTO_TRAINING_INTERVAL_MINUTES == 30
    assert "EUR/USD" in settings.AUTO_TRAINING_SYMBOLS


def test_auto_training_scan_tracks_metadata_and_skips_non_provider(monkeypatch):
    db = _FakeDb()
    monkeypatch.setattr(settings, "AUTO_TRAINING_SYMBOLS", ["EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD"])

    async def no_latest(_db):
        return None

    async def fake_pipeline(_db, pair, source="auto_training", report_unavailable=True):
        if pair == "EUR/USD":
            return {"signal_id": 10, "pair": pair, "direction": "BUY", "data_mode": "provider", "demo_only": False, "execution_grade": True}
        if pair == "GBP/USD":
            return {"signal_id": 11, "pair": pair, "direction": "HOLD", "data_mode": "provider", "demo_only": False, "execution_grade": False}
        if pair == "USD/JPY":
            return {"pair": pair, "direction": "HOLD", "data_mode": "synthetic_demo", "demo_only": True, "execution_grade": False}
        return {"pair": pair, "direction": "UNAVAILABLE", "data_mode": "unavailable", "demo_only": False, "execution_grade": False, "provider_failed": True}

    async def fake_validate(_db):
        return {"validated": 0, "auto_trade": False, "no_execution": True, "advisory_only": True}

    async def fake_status(_db):
        run = next(item for item in db.added if item.__class__.__name__ == "TrainingRun")
        return {
            "run": auto_training._metadata(run),
            "auto_trade": False,
            "no_execution": True,
            "advisory_only": True,
        }

    monkeypatch.setattr(auto_training, "_latest_run", no_latest)
    monkeypatch.setattr(auto_training, "run_signal_pipeline_for_pair", fake_pipeline)
    monkeypatch.setattr(auto_training, "validate_pending_outcomes", fake_validate)
    monkeypatch.setattr(auto_training, "training_status", fake_status)

    payload = _run(auto_training.run_auto_training(db, force=True))

    assert payload["skipped"] is False
    assert payload["run"]["total_scans"] == 1
    assert payload["run"]["provider_backed_signals"] == 2
    assert payload["run"]["synthetic_skipped"] == 1
    assert payload["run"]["unavailable_skipped"] == 1
    assert payload["auto_trade"] is False
    assert payload["no_execution"] is True
    assert payload["advisory_only"] is True


def test_training_accuracy_excludes_hold_demo_unavailable_and_execution_grade_false():
    rows = [
        (_sample("EUR/USD", "BUY"), SimpleNamespace(outcome="win")),
        (_sample("GBP/USD", "SELL"), SimpleNamespace(outcome="loss")),
        (_sample("USD/JPY", "HOLD", execution_grade=False), SimpleNamespace(outcome="neutral")),
        (_sample("AUD/USD", "BUY", execution_grade=False), SimpleNamespace(outcome="win")),
        (_sample("USD/CAD", "BUY", demo_only=True), SimpleNamespace(outcome="win")),
        (_sample("USD/CHF", "BUY", data_mode="unavailable"), SimpleNamespace(outcome="win")),
    ]

    stats = auto_training.training_statistics(rows)

    assert stats["eligible_buy_sell"] == 2
    assert stats["validated_buy_sell"] == 2
    assert stats["wins"] == 1
    assert stats["losses"] == 1
    assert stats["accuracy"] == 50.0
    assert stats["hold_count"] == 1
    assert stats["excluded_non_execution_grade"] == 3
    assert stats["best_pairs"][0]["symbol"] == "EUR/USD"
    assert stats["worst_pairs"][0]["symbol"] == "GBP/USD"
