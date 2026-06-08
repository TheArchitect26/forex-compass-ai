from __future__ import annotations

from datetime import timedelta

from sqlalchemy import select

from app.engines.outcome_validation import validate_pending_outcomes
from app.models import ValidationRun
from app.utils_time import as_utc, utc_now


VALIDATION_INTERVAL = timedelta(minutes=10)


async def _latest_validation_run_model(db) -> ValidationRun | None:
    return (await db.execute(select(ValidationRun).order_by(ValidationRun.started_at.desc()).limit(1))).scalars().first()


def _serialize_validation_run(run: ValidationRun | None) -> dict | None:
    if not run:
        return None
    return {
        "id": run.id,
        "started_at": run.started_at.isoformat(),
        "completed_at": run.completed_at.isoformat() if run.completed_at else None,
        "status": run.status,
        "signals_checked": run.signals_checked,
        "outcomes_updated": run.outcomes_updated,
        "error_message": run.error_message,
    }


async def latest_validation_run(db) -> dict | None:
    try:
        return _serialize_validation_run(await _latest_validation_run_model(db))
    except Exception:
        return None


async def run_scheduled_validation(db, *, force: bool = False) -> dict:
    latest_model = await _latest_validation_run_model(db)
    latest = _serialize_validation_run(latest_model)
    if latest_model and not force:
        last_started = as_utc(latest_model.started_at)
        if utc_now() - last_started < VALIDATION_INTERVAL:
            return {
                "skipped": True,
                "reason": "interval_not_due",
                "last_run": latest,
                "auto_trade": False,
                "no_execution": True,
                "advisory_only": True,
            }
    result = await validate_pending_outcomes(db)
    return {
        **result,
        "skipped": False,
        "scheduled": True,
        "last_run": await latest_validation_run(db),
        "auto_trade": False,
        "no_execution": True,
        "advisory_only": True,
    }
