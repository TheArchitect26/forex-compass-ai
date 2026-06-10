from __future__ import annotations

from datetime import timedelta

from sqlalchemy import desc, select

from app.config import settings
from app.engines.market_data import market_data
from app.engines.outcome_validation import validate_pending_outcomes
from app.engines.pipeline import run_signal_pipeline_for_pair
from app.models import SignalOutcome, TrainingRun, TrainingSignalSample
from app.utils_time import as_utc, utc_now


TRAINING_DURATION = timedelta(days=7)
PROVIDER_MODES = {"provider", "live", "cached"}
FINAL_TRADE_OUTCOMES = {"win", "loss", "expired", "invalidated"}


async def _latest_run(db) -> TrainingRun | None:
    return (
        await db.execute(select(TrainingRun).order_by(desc(TrainingRun.started_at)).limit(1))
    ).scalars().first()


def _configured_symbols() -> list[str]:
    configured = settings.AUTO_TRAINING_SYMBOLS or settings.PAIRS
    recommended = market_data.recommended_symbols(configured)
    return recommended or configured


def _metadata(run: TrainingRun | None) -> dict | None:
    if not run:
        return None
    return {
        "id": run.id,
        "status": run.status,
        "started_at": run.started_at.isoformat(),
        "completed_at": run.completed_at.isoformat() if run.completed_at else None,
        "last_scan_at": run.last_scan_at.isoformat() if run.last_scan_at else None,
        "interval_minutes": run.interval_minutes,
        "symbols": run.symbols,
        "total_scans": run.total_scans,
        "provider_backed_signals": run.provider_backed_signals,
        "synthetic_skipped": run.synthetic_skipped,
        "unavailable_skipped": run.unavailable_skipped,
        "error_message": run.error_message,
    }


async def run_auto_training(db, *, force: bool = False) -> dict:
    """Run one due provider-backed scan cycle and validate stored outcomes."""
    run = await _latest_run(db)
    if not settings.AUTO_TRAINING_ENABLED and not force:
        return {**await training_status(db), "skipped": True, "reason": "disabled"}

    now = utc_now()
    db_now = now.replace(tzinfo=None)
    if run and run.status == "completed":
        return {**await training_status(db), "skipped": True, "reason": "training_complete"}

    if not run:
        run = TrainingRun(
            started_at=db_now,
            status="running",
            interval_minutes=max(1, settings.AUTO_TRAINING_INTERVAL_MINUTES),
            symbols=_configured_symbols(),
        )
        db.add(run)
        await db.flush()

    if now - as_utc(run.started_at) >= TRAINING_DURATION:
        await validate_pending_outcomes(db)
        run.status = "completed"
        run.completed_at = db_now
        await db.commit()
        return {**await training_status(db), "skipped": True, "reason": "training_complete"}

    interval = timedelta(minutes=max(1, run.interval_minutes))
    if run.last_scan_at and not force and now - as_utc(run.last_scan_at) < interval:
        return {**await training_status(db), "skipped": True, "reason": "interval_not_due"}

    try:
        run.status = "running"
        run.error_message = None
        for symbol in run.symbols:
            signal = await run_signal_pipeline_for_pair(
                db, symbol, source="auto_training", report_unavailable=True
            )
            if not signal:
                continue
            data_mode = signal.get("data_mode") or "unavailable"
            demo_only = bool(signal.get("demo_only"))
            execution_grade = bool(signal.get("execution_grade"))
            if demo_only or data_mode == "synthetic_demo":
                run.synthetic_skipped += 1
                continue
            if data_mode == "unavailable" or signal.get("provider_failed"):
                run.unavailable_skipped += 1
                continue
            if data_mode not in PROVIDER_MODES:
                run.unavailable_skipped += 1
                continue

            run.provider_backed_signals += 1
            signal_id = signal.get("signal_id")
            if signal_id:
                db.add(TrainingSignalSample(
                    training_run_id=run.id,
                    signal_id=signal_id,
                    symbol=signal["pair"],
                    direction=signal["direction"],
                    data_mode=data_mode,
                    demo_only=demo_only,
                    execution_grade=execution_grade,
                ))

        run.total_scans += 1
        run.last_scan_at = db_now
        await db.commit()
        validation = await validate_pending_outcomes(db)
        return {
            **await training_status(db),
            "skipped": False,
            "validation": validation,
        }
    except Exception as exc:
        run.status = "failed"
        run.error_message = str(exc)
        await db.commit()
        return {**await training_status(db), "skipped": False, "error": str(exc)}


async def training_status(db) -> dict:
    run = await _latest_run(db)
    now = utc_now()
    db_now = now.replace(tzinfo=None)
    rows = []
    if run:
        rows = (
            await db.execute(
                select(TrainingSignalSample, SignalOutcome)
                .outerjoin(SignalOutcome, SignalOutcome.signal_id == TrainingSignalSample.signal_id)
                .where(TrainingSignalSample.training_run_id == run.id)
            )
        ).all()
    stats = training_statistics(rows)

    elapsed_seconds = max(0.0, (now - as_utc(run.started_at)).total_seconds()) if run else 0.0
    progress = 100.0 if run and run.status == "completed" else min(100.0, elapsed_seconds / TRAINING_DURATION.total_seconds() * 100)
    return {
        "enabled": settings.AUTO_TRAINING_ENABLED,
        "duration_days": 7,
        "progress_percent": round(progress, 2),
        "run": _metadata(run),
        "statistics": stats,
        "safety_flags": {
            "auto_trade": False,
            "no_execution": True,
            "advisory_only": True,
            "no_broker_execution": True,
            "no_trade_placement": True,
            "provider_backed_accuracy_only": True,
            "synthetic_excluded": True,
            "unavailable_excluded": True,
            "demo_only_excluded": True,
            "execution_grade_false_excluded": True,
            "hold_separate_from_win_rate": True,
        },
        "auto_trade": False,
        "no_execution": True,
        "advisory_only": True,
    }


def training_statistics(rows: list[tuple[TrainingSignalSample, SignalOutcome | None]]) -> dict:
    stats = {
        "eligible_buy_sell": 0,
        "validated_buy_sell": 0,
        "pending_buy_sell": 0,
        "wins": 0,
        "losses": 0,
        "accuracy": 0.0,
        "hold_count": 0,
        "excluded_non_execution_grade": 0,
        "by_pair": [],
        "best_pairs": [],
        "worst_pairs": [],
    }
    pairs: dict[str, dict] = {}
    for sample, outcome in rows:
        if sample.direction == "HOLD":
            stats["hold_count"] += 1
            continue
        if (
            sample.demo_only
            or sample.data_mode not in PROVIDER_MODES
            or not sample.execution_grade
            or sample.direction not in {"BUY", "SELL"}
        ):
            stats["excluded_non_execution_grade"] += 1
            continue
        stats["eligible_buy_sell"] += 1
        result = outcome.outcome if outcome else "pending"
        bucket = pairs.setdefault(sample.symbol, {"symbol": sample.symbol, "validated": 0, "wins": 0, "losses": 0, "accuracy": 0.0})
        if result in FINAL_TRADE_OUTCOMES:
            stats["validated_buy_sell"] += 1
            bucket["validated"] += 1
            if result == "win":
                stats["wins"] += 1
                bucket["wins"] += 1
            else:
                stats["losses"] += 1
                bucket["losses"] += 1
        else:
            stats["pending_buy_sell"] += 1

    if stats["validated_buy_sell"]:
        stats["accuracy"] = round(stats["wins"] / stats["validated_buy_sell"] * 100, 2)
    for bucket in pairs.values():
        if bucket["validated"]:
            bucket["accuracy"] = round(bucket["wins"] / bucket["validated"] * 100, 2)
    ranked = sorted(pairs.values(), key=lambda item: (-item["accuracy"], -item["validated"], item["symbol"]))
    stats["by_pair"] = ranked
    stats["best_pairs"] = ranked[:3]
    stats["worst_pairs"] = sorted(ranked, key=lambda item: (item["accuracy"], -item["validated"], item["symbol"]))[:3]
    return stats
