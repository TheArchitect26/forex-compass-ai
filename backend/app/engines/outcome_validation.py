from __future__ import annotations

from datetime import timedelta

from sqlalchemy import select

from app.config import settings
from app.engines.market_data import market_data
from app.engines.pips import pips_from_price_move
from app.models import HistoricalCandle, Signal, SignalOutcome, SignalScanContext, ValidationRun
from app.utils_time import as_utc, utc_now


FINAL_OUTCOMES = {"win", "loss", "neutral", "expired", "invalidated"}
VALIDATION_TIMEFRAMES = {"1min", "5min", "15min", "30min", "1h", "4h", "1day"}
TF_MINUTES = {"1min": 1, "5min": 5, "15min": 15, "30min": 30, "1h": 60, "4h": 240, "1day": 1440}


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
    run = ValidationRun(status="running", started_at=utc_now())
    db.add(run)
    await db.flush()
    counts = {
        "checked": 0,
        "validated": 0,
        "pending": 0,
        "skipped_demo": 0,
        "missing_data": 0,
        "wins": 0,
        "losses": 0,
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
                outcome_row.checked_at = utc_now()
                counts["skipped_demo"] += 1
                counts["pending"] += 1
                continue

            future_candles = await _future_candles(db, signal, context)
            if not future_candles:
                outcome_row.checked_at = utc_now()
                counts["missing_data"] += 1
                counts["pending"] += 1
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
            outcome_row.checked_at = utc_now()
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
                counts["pending"] += 1

        run.status = "completed"
        run.signals_checked = counts["checked"]
        run.outcomes_updated = counts["validated"]
        run.completed_at = utc_now()
        await db.commit()
        return {**counts, "updated": counts["validated"], "run_id": run.id, "auto_trade": False, "no_execution": True}
    except Exception as exc:
        run.status = "failed"
        run.error_message = str(exc)
        run.completed_at = utc_now()
        await db.commit()
        return {**counts, "updated": counts["validated"], "error": str(exc), "run_id": run.id, "auto_trade": False, "no_execution": True}


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
    start = as_utc(signal.created_at)
    end = start + timedelta(minutes=TF_MINUTES[timeframe] * max(1, horizon + 1))
    stored = (await db.execute(
        select(HistoricalCandle)
        .where(
            HistoricalCandle.pair == signal.pair,
            HistoricalCandle.timeframe == timeframe,
            HistoricalCandle.timestamp > start,
            HistoricalCandle.timestamp <= end,
        )
        .order_by(HistoricalCandle.timestamp.asc())
        .limit(horizon)
    )).scalars().all()
    if stored:
        return [{"time": c.timestamp, "high": c.high, "low": c.low} for c in stored]

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
        if start < as_utc(ts) <= end:
            candles.append({"time": ts, "high": float(row.high), "low": float(row.low)})
            db.add(HistoricalCandle(
                pair=signal.pair,
                timeframe=timeframe,
                timestamp=ts,
                open=float(row.open),
                high=float(row.high),
                low=float(row.low),
                close=float(row.close),
                volume=float(getattr(row, "volume", 0.0) or 0.0),
                source=info.get("source") or provider_name,
                integrity_flags={"validation_fetch": True},
            ))
    return candles[:horizon]
