from __future__ import annotations

from datetime import timedelta

from sqlalchemy import func, select

from app.config import settings
from app.engines.market_data import market_data
from app.engines.pips import pips_from_price_move
from app.engines.adaptive import record_outcome
from app.models import HistoricalCandle, Signal, SignalOutcome, SignalScanContext, ValidationRun
from app.utils_time import as_utc, utc_now


FINAL_OUTCOMES = {"win", "loss", "neutral", "expired", "invalidated"}
VALIDATION_TIMEFRAMES = {"1min", "5min", "15min", "30min", "1h", "4h", "1day"}
TF_MINUTES = {"1min": 1, "5min": 5, "15min": 15, "30min": 30, "1h": 60, "4h": 240, "1day": 1440}
PROVIDER_VALIDATION_MODES = {"provider", "live", "cached"}


def classify_threshold_outcome(
    direction: str,
    pair: str,
    entry: float,
    candles: list[dict],
    *,
    horizon_candles: int | None = None,
    take_profit_pips: float | None = None,
    stop_loss_pips: float | None = None,
) -> dict:
    horizon = horizon_candles or settings.OUTCOME_VALIDATION_HORIZON_CANDLES
    take_profit = take_profit_pips or settings.OUTCOME_TAKE_PROFIT_PIPS
    stop_loss = stop_loss_pips or settings.OUTCOME_STOP_LOSS_PIPS
    usable = candles[:horizon]

    if direction not in {"BUY", "SELL"}:
        return {"outcome": "neutral", "max_favorable_move": 0.0, "max_adverse_move": 0.0}
    if not usable:
        return {"outcome": "pending", "max_favorable_move": 0.0, "max_adverse_move": 0.0}

    max_fav = 0.0
    max_adv = 0.0
    for candle in usable:
        high = float(candle["high"])
        low = float(candle["low"])
        if direction == "BUY":
            fav = pips_from_price_move(pair, high - entry)
            adv = pips_from_price_move(pair, entry - low)
        else:
            fav = pips_from_price_move(pair, entry - low)
            adv = pips_from_price_move(pair, high - entry)
        max_fav = max(max_fav, fav)
        max_adv = max(max_adv, adv)
        hit_tp = fav >= take_profit
        hit_sl = adv >= stop_loss
        if hit_tp and not hit_sl:
            return {"outcome": "win", "max_favorable_move": round(max_fav, 1), "max_adverse_move": round(max_adv, 1)}
        if hit_sl:
            return {"outcome": "loss", "max_favorable_move": round(max_fav, 1), "max_adverse_move": round(max_adv, 1)}

    if len(usable) < horizon:
        return {"outcome": "pending", "max_favorable_move": round(max_fav, 1), "max_adverse_move": round(max_adv, 1)}
    return {"outcome": "loss", "max_favorable_move": round(max_fav, 1), "max_adverse_move": round(max_adv, 1)}


async def validate_pending_outcomes(db) -> dict:
    run = ValidationRun(status="running", started_at=utc_now().replace(tzinfo=None))
    db.add(run)
    await db.flush()
    counts = {
        "checked": 0,
        "provider_candidates": 0,
        "provider_pending": 0,
        "validated": 0,
        "pending": 0,
        "skipped_demo": 0,
        "skipped_hold": 0,
        "skipped_unavailable": 0,
        "skipped_non_execution": 0,
        "missing_data": 0,
        "wins": 0,
        "losses": 0,
        "learning_updates": 0,
    }
    try:
        rows = (await db.execute(select(Signal).order_by(Signal.created_at.desc()).limit(300))).scalars().all()
        contexts = (await db.execute(select(SignalScanContext))).scalars().all()
        by_signal = {c.signal_id: c for c in contexts}

        for signal in rows:
            counts["checked"] += 1
            outcome_row = await _ensure_outcome_row(db, signal)
            if outcome_row.outcome in FINAL_OUTCOMES:
                if outcome_row.outcome == "win":
                    counts["wins"] += 1
                elif outcome_row.outcome == "loss":
                    counts["losses"] += 1
                continue

            context = by_signal.get(signal.id)
            demo_only = (context.demo_only if context else signal.data_source == "synthetic")
            if demo_only:
                outcome_row.outcome = "pending"
                outcome_row.checked_at = utc_now().replace(tzinfo=None)
                counts["skipped_demo"] += 1
                continue
            data_mode = context.data_mode if context else ("provider" if signal.data_source == "real" else "synthetic_demo")
            if data_mode == "unavailable":
                outcome_row.outcome = "pending"
                outcome_row.checked_at = utc_now().replace(tzinfo=None)
                counts["skipped_unavailable"] += 1
                continue
            if signal.direction == "HOLD":
                outcome_row.outcome = "neutral"
                outcome_row.checked_at = utc_now().replace(tzinfo=None)
                counts["skipped_hold"] += 1
                continue
            if signal.direction not in {"BUY", "SELL"}:
                outcome_row.checked_at = utc_now().replace(tzinfo=None)
                counts["skipped_hold"] += 1
                continue
            if data_mode not in PROVIDER_VALIDATION_MODES:
                outcome_row.outcome = "pending"
                outcome_row.checked_at = utc_now().replace(tzinfo=None)
                counts["skipped_non_execution"] += 1
                continue

            counts["provider_candidates"] += 1

            future_candles = await _future_candles(db, signal, context)
            if not future_candles:
                outcome_row.checked_at = utc_now().replace(tzinfo=None)
                counts["missing_data"] += 1
                counts["provider_pending"] += 1
                continue

            result = classify_threshold_outcome(
                signal.direction,
                signal.pair,
                signal.entry,
                future_candles,
            )
            outcome_row.outcome = result["outcome"]
            outcome_row.max_favorable_move = result["max_favorable_move"]
            outcome_row.max_adverse_move = result["max_adverse_move"]
            outcome_row.checked_at = utc_now().replace(tzinfo=None)
            if result["outcome"] == "win":
                outcome_row.result_pips = settings.OUTCOME_TAKE_PROFIT_PIPS
                outcome_row.gross_result_pips = settings.OUTCOME_TAKE_PROFIT_PIPS
                outcome_row.net_result_pips = settings.OUTCOME_TAKE_PROFIT_PIPS
                signal.status = "win"
                counts["wins"] += 1
                counts["validated"] += 1
            elif result["outcome"] == "loss":
                loss = -settings.OUTCOME_STOP_LOSS_PIPS
                outcome_row.result_pips = loss
                outcome_row.gross_result_pips = loss
                outcome_row.net_result_pips = loss
                signal.status = "loss"
                counts["losses"] += 1
                counts["validated"] += 1
            else:
                counts["provider_pending"] += 1

            if result["outcome"] in {"win", "loss"}:
                signal.closed_at = utc_now().replace(tzinfo=None)
                signal.pnl_pips = outcome_row.net_result_pips
                learning_result = await record_outcome(
                    db,
                    signal,
                    commit=False,
                )
                if not learning_result.get("skipped"):
                    counts["learning_updates"] += 1

        run.status = "completed"
        run.signals_checked = counts["checked"]
        run.outcomes_updated = counts["validated"]
        run.completed_at = utc_now().replace(tzinfo=None)
        await db.commit()
        counts["pending"] = counts["provider_pending"]
        return {**counts, "updated": counts["validated"], "run_id": run.id, "auto_trade": False, "no_execution": True, "advisory_only": True}
    except Exception as exc:
        run.status = "failed"
        run.error_message = str(exc)
        run.completed_at = utc_now().replace(tzinfo=None)
        await db.commit()
        counts["pending"] = counts["provider_pending"]
        return {**counts, "updated": counts["validated"], "error": str(exc), "run_id": run.id, "auto_trade": False, "no_execution": True, "advisory_only": True}


async def _ensure_outcome_row(db, signal: Signal) -> SignalOutcome:
    outcome_row = (await db.execute(select(SignalOutcome).where(SignalOutcome.signal_id == signal.id))).scalar_one_or_none()
    if outcome_row:
        return outcome_row
    outcome_row = SignalOutcome(
        signal_id=signal.id,
        pair=signal.pair,
        timeframe=signal.timeframe,
        direction=signal.direction,
        entry_price=signal.entry,
        stop_loss=signal.stop_loss,
        take_profit=signal.take_profit,
        invalidation_price=signal.invalidation_price,
    )
    db.add(outcome_row)
    await db.flush()
    return outcome_row


async def _future_candles(db, signal: Signal, context: SignalScanContext | None) -> list[dict]:
    timeframe = signal.timeframe if signal.timeframe in VALIDATION_TIMEFRAMES else "15min"
    horizon = settings.OUTCOME_VALIDATION_HORIZON_CANDLES
    start_utc = as_utc(signal.created_at)
    end_utc = start_utc + timedelta(
        minutes=TF_MINUTES[timeframe] * max(1, horizon + 1)
    )
    validation_end_utc = min(end_utc, utc_now())
    start_db = start_utc.replace(tzinfo=None)
    validation_end_db = validation_end_utc.replace(tzinfo=None)
    stored = (await db.execute(
        select(
            HistoricalCandle.timestamp,
            func.max(HistoricalCandle.high).label("high"),
            func.min(HistoricalCandle.low).label("low"),
        )
        .where(
            HistoricalCandle.pair == signal.pair,
            HistoricalCandle.timeframe == timeframe,
            HistoricalCandle.timestamp > start_db,
            HistoricalCandle.timestamp <= validation_end_db,
        )
        .group_by(HistoricalCandle.timestamp)
        .order_by(HistoricalCandle.timestamp.asc())
        .limit(horizon)
    )).all()
    if stored:
        return [
            {
                "time": row.timestamp,
                "high": float(row.high),
                "low": float(row.low),
            }
            for row in stored
        ]

    provider_name = context.provider_name if context else ""
    if provider_name not in {"twelve_data", "cached_provider"}:
        return []
    df = await market_data.ohlcv(signal.pair, timeframe, max(300, horizon + 5))
    info = market_data.source_info(signal.pair, timeframe, max(300, horizon + 5))
    if info.get("source") == "synthetic":
        return []
    candles = []
    for row in df.itertuples():
        ts = row.datetime.to_pydatetime() if hasattr(row.datetime, "to_pydatetime") else row.datetime
        if start_utc < as_utc(ts) <= validation_end_utc:
            candles.append({"time": ts, "high": float(row.high), "low": float(row.low)})
            db.add(HistoricalCandle(
                pair=signal.pair,
                timeframe=timeframe,
                timestamp=as_utc(ts).replace(tzinfo=None),
                open=float(row.open),
                high=float(row.high),
                low=float(row.low),
                close=float(row.close),
                volume=float(getattr(row, "volume", 0.0) or 0.0),
                source=info.get("source") or provider_name,
                integrity_flags={"validation_fetch": True},
            ))
    return candles[:horizon]
