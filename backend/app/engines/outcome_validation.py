from __future__ import annotations
from sqlalchemy import select
from app.models import Signal, SignalOutcome, ValidationRun
from app.utils_time import utc_now
from app.engines.market_data import market_data
from app.engines.outcome_rules import evaluate_outcome, expiry_window_for_timeframe


async def validate_pending_outcomes(db) -> dict:
    run = ValidationRun(status="running", started_at=utc_now())
    db.add(run)
    await db.flush()
    try:
        rows = (await db.execute(select(Signal).order_by(Signal.created_at.desc()).limit(300))).scalars().all()
        validated = 0
        for s in rows:
            outcome_row = (await db.execute(select(SignalOutcome).where(SignalOutcome.signal_id == s.id))).scalar_one_or_none()
            if not outcome_row:
                outcome_row = SignalOutcome(
                    signal_id=s.id, pair=s.pair, timeframe=s.timeframe, direction=s.direction,
                    entry_price=s.entry, stop_loss=s.stop_loss, take_profit=s.take_profit,
                    invalidation_price=s.invalidation_price,
                )
                db.add(outcome_row)

            if outcome_row.outcome in {"win", "loss", "neutral", "expired", "invalidated"}:
                continue

            tf = s.timeframe if s.timeframe in ["1min", "5min", "15min", "30min", "1h", "4h", "1day"] else "15min"
            candles_df = await market_data.ohlcv(s.pair, tf, 300)
            candles = [{"time": r.datetime, "high": float(r.high), "low": float(r.low)} for r in candles_df.itertuples() if r.datetime > s.created_at]
            result = evaluate_outcome(s.direction, s.pair, s.entry, s.stop_loss, s.take_profit, s.invalidation_price, candles, s.created_at + expiry_window_for_timeframe(s.timeframe), s.created_at)
            outcome_row.outcome = result["outcome"]
            outcome_row.result_pips = result["result_pips"]
            outcome_row.gross_result_pips = result["gross_result_pips"]
            outcome_row.estimated_cost_pips = result["estimated_cost_pips"]
            outcome_row.net_result_pips = result["net_result_pips"]
            outcome_row.max_favorable_move = result["max_favorable_move"]
            outcome_row.max_adverse_move = result["max_adverse_move"]
            outcome_row.checked_at = utc_now()
            validated += 1

        run.status = "completed"
        run.signals_checked = len(rows)
        run.outcomes_updated = validated
        run.completed_at = utc_now()
        await db.commit()
        return {"checked": len(rows), "updated": validated, "run_id": run.id}
    except Exception as e:
        run.status = "failed"
        run.error_message = str(e)
        run.completed_at = utc_now()
        await db.commit()
        return {"checked": 0, "updated": 0, "error": str(e), "run_id": run.id}
