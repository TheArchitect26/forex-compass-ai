from __future__ import annotations
from datetime import timedelta
from sqlalchemy import select, desc
from app.config import settings
from app.config import has_real_market_provider, is_production_like, synthetic_buy_sell_blocked
from app.models import Signal, ExplainabilityAudit, HistoricalCandle, SignalScanContext, StrategyState, LearningRecord
from app.engines.market_data import market_data
from app.engines.signal_intelligence import analyze_pair
from app.engines.signal_discipline import apply_quality_gates, blocked_by_synthetic_policy, is_duplicate_recent
from app.engines.adaptive import pattern_key, pattern_key_for_direction
from app.engines.strategy_profiles import profile_or_default
from app.utils_time import utc_now

from app.engines.pipeline_meta import config_snapshot

async def get_active_profile(db) -> dict:
    state = (await db.execute(select(StrategyState).order_by(StrategyState.id.asc()))).scalars().first()
    return profile_or_default(state.active_profile if state else "intraday")


def _apply_training_direction(signal: dict, direction: str) -> None:
    previous = signal.get("direction")
    if previous == direction:
        return

    entry = float(signal["entry"])
    current_sl = float(signal["stop_loss"])
    distance = abs(entry - current_sl)

    if distance <= 0:
        distance = max(abs(entry) * 0.0005, 0.00001)

    rr = float(signal.get("risk_reward") or 2.5)
    precision = 3 if signal.get("pair", "").endswith("/JPY") else 5

    if direction == "BUY":
        stop_loss = entry - distance
        take_profit = entry + distance * rr
    else:
        stop_loss = entry + distance
        take_profit = entry - distance * rr

    signal["direction"] = direction
    signal["stop_loss"] = round(stop_loss, precision)
    signal["take_profit"] = round(take_profit, precision)
    signal["invalidation_price"] = signal["stop_loss"]
    signal["reason_summary"] = (
        f"{signal.get('reason_summary', '')} "
        f"Adaptive learning changed {previous} to {direction}."
    ).strip()
    signal["explanation"] = (
        f"{signal.get('explanation', '')} "
        f"Training memory selected {direction}; paper trade only."
    ).strip()


async def run_signal_pipeline_for_pair(db, pair: str, source: str = "api_scan", report_unavailable: bool = False) -> dict | None:
    profile = await get_active_profile(db)
    training_mode = source == "auto_training"
    if training_mode:
        res = await analyze_pair(
            pair,
            force_trade=True,
        )
    else:
        res = await analyze_pair(pair)
    if not res.get("signal"):
        return None
    s = res["signal"]
    source_info = market_data.source_info(s["pair"], s["timeframe"], 200)
    provider_name = source_info.get("source") or s["data_source"]
    provider_failed = (
        has_real_market_provider()
        and provider_name == "synthetic"
        and "Twelve Data request failed" in (source_info.get("warning") or "")
    )
    if provider_failed and is_production_like():
        if report_unavailable:
            return {
                "pair": pair,
                "direction": "UNAVAILABLE",
                "timeframe": s["timeframe"],
                "data_source": "unavailable",
                "data_mode": "unavailable",
                "provider_name": "twelve_data",
                "provider_failed": True,
                "demo_only": False,
                "execution_grade": False,
                "warning": source_info.get("warning") or "Twelve Data request failed.",
            }
        return None
    allow_synthetic_signals = (
        settings.ALLOW_SYNTHETIC_SIGNALS
        and not synthetic_buy_sell_blocked()
    )

    if blocked_by_synthetic_policy(
        s,
        allow_synthetic_signals,
    ):
        return None

    before = s["confidence"]

    reasoning = s.setdefault("reasoning", {})

    if training_mode:
        buy_key = pattern_key_for_direction(s, "BUY")
        sell_key = pattern_key_for_direction(s, "SELL")

        learning_rows = (
            await db.execute(
                select(LearningRecord).where(
                    LearningRecord.pattern_key.in_(
                        [buy_key, sell_key]
                    )
                )
            )
        ).scalars().all()

        learning_by_key = {
            row.pattern_key: row for row in learning_rows
        }
        buy_row = learning_by_key.get(buy_key)
        sell_row = learning_by_key.get(sell_key)

        buy_weight = buy_row.weight if buy_row else 1.0
        sell_weight = sell_row.weight if sell_row else 1.0

        scores = reasoning.get("confluence_scores") or {}
        bull_score = float(scores.get("bull", 0))
        bear_score = float(scores.get("bear", 0))

        adjusted_buy_score = (
            bull_score + 1.0
        ) * buy_weight
        adjusted_sell_score = (
            bear_score + 1.0
        ) * sell_weight

        if adjusted_buy_score > adjusted_sell_score:
            selected_direction = "BUY"
        elif adjusted_sell_score > adjusted_buy_score:
            selected_direction = "SELL"
        else:
            selected_direction = (
                s["direction"]
                if s["direction"] in {"BUY", "SELL"}
                else "BUY"
            )

        direction_before_learning = s["direction"]
        _apply_training_direction(
            s,
            selected_direction,
        )

        selected_row = (
            buy_row
            if selected_direction == "BUY"
            else sell_row
        )
        selected_weight = (
            selected_row.weight if selected_row else 1.0
        )
        confidence_before_learning = s["confidence"]
        s["confidence"] = round(
            max(
                5.0,
                min(
                    100.0,
                    s["confidence"] * selected_weight,
                ),
            ),
            1,
        )

        reasoning["learning_decision"] = {
            "direction_before_learning": direction_before_learning,
            "selected_direction": selected_direction,
            "bull_score": bull_score,
            "bear_score": bear_score,
            "buy_weight": buy_weight,
            "sell_weight": sell_weight,
            "adjusted_buy_score": round(
                adjusted_buy_score,
                4,
            ),
            "adjusted_sell_score": round(
                adjusted_sell_score,
                4,
            ),
            "buy_results": {
                "wins": buy_row.wins if buy_row else 0,
                "losses": buy_row.losses if buy_row else 0,
            },
            "sell_results": {
                "wins": sell_row.wins if sell_row else 0,
                "losses": sell_row.losses if sell_row else 0,
            },
        }
        reasoning["learning_adjustment"] = {
            "pattern_key": (
                buy_key
                if selected_direction == "BUY"
                else sell_key
            ),
            "weight": selected_weight,
            "confidence_before": confidence_before_learning,
            "confidence_after": s["confidence"],
        }
        reasoning["training_mode"] = {
            "forced_paper_trade": True,
            "quality_gate_bypassed": True,
            "cooldown_bypassed": True,
            "improves_after_each_resolved_trade": True,
            "no_broker_execution": True,
        }
    else:
        learning_key = pattern_key(s)
        learning_row = (
            await db.execute(
                select(LearningRecord).where(
                    LearningRecord.pattern_key == learning_key
                )
            )
        ).scalar_one_or_none()

        if learning_row:
            confidence_before_learning = s["confidence"]
            s["confidence"] = round(
                max(
                    5.0,
                    min(
                        100.0,
                        s["confidence"]
                        * learning_row.weight,
                    ),
                ),
                1,
            )
            reasoning["learning_adjustment"] = {
                "pattern_key": learning_key,
                "weight": learning_row.weight,
                "confidence_before": confidence_before_learning,
                "confidence_after": s["confidence"],
                "wins": learning_row.wins,
                "losses": learning_row.losses,
            }

        s = apply_quality_gates(
            s,
            profile["min_confidence"],
        )
    demo_only = s["data_source"] == "synthetic" or provider_name == "synthetic"
    data_mode = "synthetic_demo" if demo_only else "provider"

    if not training_mode:
        cooldown_since = (
            utc_now() - timedelta(minutes=profile["cooldown_minutes"])
        ).replace(tzinfo=None)
        existing = (
            await db.execute(
                select(Signal)
                .where(
                    Signal.pair == s["pair"],
                    Signal.timeframe == s["timeframe"],
                    Signal.created_at >= cooldown_since,
                )
                .order_by(desc(Signal.created_at))
            )
        ).scalars().first()
        if existing and is_duplicate_recent(
            existing.created_at,
            profile["cooldown_minutes"],
        ):
            return None

    snap = config_snapshot(
        profile,
        runtime={
            "allow_synthetic_signals": allow_synthetic_signals,
            "default_slippage_pips": settings.DEFAULT_SLIPPAGE_PIPS,
            "default_spread_pips": settings.DEFAULT_SPREAD_PIPS,
            "training_mode": training_mode,
            "forced_paper_trade": training_mode,
        },
    )
    s.setdefault("reasoning", {})["profile"] = profile["name"]
    s["reasoning"]["config_snapshot"] = snap
    s["reasoning"]["source_path"] = source
    s["data_mode"] = data_mode
    s["provider_name"] = provider_name
    s["demo_only"] = demo_only
    s["execution_grade"] = not demo_only

    row = Signal(
        pair=s["pair"], direction=s["direction"], timeframe=s["timeframe"],
        entry=s["entry"], stop_loss=s["stop_loss"], take_profit=s["take_profit"],
        risk_reward=s["risk_reward"], confidence=s["confidence"], strength=s["strength"],
        risk_level=s["risk_level"], reason_summary=s["reason_summary"], indicators_used=s["indicators_used"],
        invalidation_price=s["invalidation_price"], data_source=s["data_source"], market_regime=s["market_regime"],
        reasoning=s["reasoning"], explanation=s["explanation"], status="open",
    )
    db.add(row)
    await db.flush()
    s["signal_id"] = row.id

    snapshot = await _persist_signal_candle_snapshot(db, s["pair"], s["timeframe"], provider_name, demo_only)
    db.add(SignalScanContext(
        signal_id=row.id,
        symbol=s["pair"],
        interval=s["timeframe"],
        signal_timestamp=row.created_at,
        direction=s["direction"],
        confidence=s["confidence"],
        entry_price=s["entry"],
        data_mode=data_mode,
        provider_name=provider_name,
        demo_only=demo_only,
        candle_snapshot=snapshot,
    ))
    db.add(ExplainabilityAudit(
        pair=s["pair"], timeframe=s["timeframe"], regime=s["market_regime"], strategy_profile=profile["name"],
        signal_decision=s["direction"], confidence_before=before, confidence_after=s["confidence"],
        adaptive_changes=s.get("reasoning", {}).get("adaptive_weighting", {}), drift_warnings=s.get("reasoning", {}).get("risk_warnings", []),
        reasons=f"{s.get('reason_summary','')} | src={source} | versions={snap}",
    ))
    return s


async def _persist_signal_candle_snapshot(
    db,
    pair: str,
    timeframe: str,
    provider_name: str,
    demo_only: bool,
) -> dict:
    limit = 200

    frame = await market_data.ohlcv(
        pair,
        timeframe,
        limit,
    )

    candles_by_timestamp = {}

    for item in frame.itertuples():
        timestamp = (
            item.datetime.to_pydatetime()
            if hasattr(
                item.datetime,
                "to_pydatetime",
            )
            else item.datetime
        )

        if getattr(timestamp, "tzinfo", None):
            timestamp = timestamp.replace(
                tzinfo=None
            )

        candles_by_timestamp[timestamp] = {
            "timestamp": timestamp,
            "open": float(item.open),
            "high": float(item.high),
            "low": float(item.low),
            "close": float(item.close),
            "volume": float(
                getattr(item, "volume", 0.0)
                or 0.0
            ),
        }

    rows = list(
        candles_by_timestamp.values()
    )

    persisted_rows = 0

    if not demo_only and rows:
        timestamps = [
            candle["timestamp"]
            for candle in rows
        ]

        existing_timestamps = set(
            (
                await db.execute(
                    select(
                        HistoricalCandle.timestamp
                    ).where(
                        HistoricalCandle.pair
                        == pair,
                        HistoricalCandle.timeframe
                        == timeframe,
                        HistoricalCandle.source
                        == provider_name,
                        HistoricalCandle.timestamp.in_(
                            timestamps
                        ),
                    )
                )
            ).scalars().all()
        )

        for candle in rows:
            if (
                candle["timestamp"]
                in existing_timestamps
            ):
                continue

            db.add(
                HistoricalCandle(
                    pair=pair,
                    timeframe=timeframe,
                    timestamp=(
                        candle["timestamp"]
                    ),
                    open=candle["open"],
                    high=candle["high"],
                    low=candle["low"],
                    close=candle["close"],
                    volume=candle["volume"],
                    source=provider_name,
                    integrity_flags={
                        "scan_context": True,
                    },
                    dataset_version=(
                        "signal-snapshot-v1"
                    ),
                )
            )

            persisted_rows += 1

    return {
        "rows": len(rows),
        "persisted_rows": persisted_rows,
        "duplicate_rows": (
            len(rows) - persisted_rows
            if not demo_only
            else 0
        ),
        "first_timestamp": (
            rows[0]["timestamp"].isoformat()
            if rows
            else None
        ),
        "last_timestamp": (
            rows[-1]["timestamp"].isoformat()
            if rows
            else None
        ),
        "source": provider_name,
        "demo_only": demo_only,
    }
