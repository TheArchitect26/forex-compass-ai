import asyncio
from datetime import timedelta
from types import SimpleNamespace

from app.api import signals as signals_api
from app.engines import scheduled_validation
from app.utils_time import utc_now


class _ScalarResult:
    def __init__(self, item):
        self.item = item

    def first(self):
        return self.item

    def all(self):
        return [self.item] if self.item else []


class _ExecuteResult:
    def __init__(self, item):
        self.item = item

    def scalars(self):
        return _ScalarResult(self.item)


class _FakeDb:
    def __init__(self, run=None):
        self.run = run

    async def execute(self, _statement):
        return _ExecuteResult(self.run)


def _run_model(*, started_at=None, completed_at=None, checked=3, updated=2):
    now = utc_now()
    return SimpleNamespace(
        id=42,
        started_at=started_at or now,
        completed_at=completed_at or now,
        status="completed",
        signals_checked=checked,
        outcomes_updated=updated,
        error_message=None,
    )


def test_scheduled_validation_respects_safe_interval(monkeypatch):
    db = _FakeDb(_run_model())

    async def fail_if_called(_db):
        raise AssertionError("validation should not run before the safe interval elapses")

    monkeypatch.setattr(scheduled_validation, "validate_pending_outcomes", fail_if_called)

    result = asyncio.run(scheduled_validation.run_scheduled_validation(db))

    assert result["skipped"] is True
    assert result["reason"] == "interval_not_due"
    assert result["last_run"]["signals_checked"] == 3
    assert result["last_run"]["outcomes_updated"] == 2
    assert result["auto_trade"] is False
    assert result["no_execution"] is True
    assert result["advisory_only"] is True


def test_scheduled_validation_runs_when_due_and_keeps_no_execution_flags(monkeypatch):
    old_run = _run_model(started_at=utc_now() - timedelta(minutes=30), completed_at=utc_now() - timedelta(minutes=29))
    db = _FakeDb(old_run)

    async def fake_validate(_db):
        _db.run = _run_model(checked=4, updated=1)
        return {
            "checked": 4,
            "validated": 1,
            "updated": 1,
            "provider_candidates": 1,
            "provider_pending": 0,
            "skipped_demo": 1,
            "skipped_hold": 1,
            "skipped_unavailable": 1,
            "skipped_non_execution": 0,
            "auto_trade": False,
            "no_execution": True,
            "advisory_only": True,
        }

    monkeypatch.setattr(scheduled_validation, "validate_pending_outcomes", fake_validate)

    result = asyncio.run(scheduled_validation.run_scheduled_validation(db))

    assert result["scheduled"] is True
    assert result["skipped"] is False
    assert result["provider_candidates"] == 1
    assert result["skipped_demo"] == 1
    assert result["skipped_hold"] == 1
    assert result["skipped_unavailable"] == 1
    assert result["auto_trade"] is False
    assert result["no_execution"] is True
    assert result["advisory_only"] is True
    assert result["last_run"]["signals_checked"] == 4
    assert result["last_run"]["outcomes_updated"] == 1


def test_signal_status_exposes_last_validation_run_and_pending_count(monkeypatch):
    async def fake_validation_stats(_db):
        return {
            "provider_backed": {"pending": 7, "win_rate": 62.5},
            "synthetic_demo": {"total": 0},
        }

    async def fake_latest_run(_db):
        return {
            "id": 8,
            "started_at": "2026-06-07T00:00:00+00:00",
            "completed_at": "2026-06-07T00:00:10+00:00",
            "status": "completed",
            "signals_checked": 5,
            "outcomes_updated": 2,
            "error_message": None,
        }

    monkeypatch.setattr(signals_api, "_validation_stats", fake_validation_stats)
    monkeypatch.setattr(signals_api, "latest_validation_run", fake_latest_run)

    payload = asyncio.run(signals_api.status(db=object()))

    assert payload["pending_validation_count"] == 7
    assert payload["last_validation_run_at"] == "2026-06-07T00:00:10+00:00"
    assert payload["last_validation_counts"] == {"signals_checked": 5, "outcomes_updated": 2}
    assert payload["auto_trade"] is False
    assert payload["no_execution"] is True
    assert payload["advisory_only"] is True
