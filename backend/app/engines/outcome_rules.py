from __future__ import annotations
from datetime import datetime, timedelta, timezone
from app.config import settings
from app.engines.pips import pips_from_price_move
from app.utils_time import as_utc


def expiry_window_for_timeframe(tf: str) -> timedelta:
    if tf in {"1min", "5min", "15min", "30min"}:
        return timedelta(minutes=60)
    if tf in {"1h", "4h"}:
        return timedelta(hours=8)
    return timedelta(days=3)


def _cost_pips(pair: str) -> float:
    return float(settings.DEFAULT_SPREAD_PIPS.get(pair, 1.5)) + float(settings.DEFAULT_SLIPPAGE_PIPS) + float(settings.COMMISSION_PER_TRADE)


def _pack(outcome: str, pair: str, gross: float, max_fav: float, max_adv: float) -> dict:
    cost = _cost_pips(pair)
    net = gross - cost
    return {"outcome": outcome, "result_pips": round(net, 1), "gross_result_pips": round(gross, 1), "estimated_cost_pips": round(cost, 1), "net_result_pips": round(net, 1), "max_favorable_move": round(max_fav, 1), "max_adverse_move": round(max_adv, 1)}


def evaluate_outcome(direction: str, pair: str, entry: float, sl: float, tp: float, invalidation: float, candles: list[dict], expires_at: datetime, created_at: datetime) -> dict:
    now = datetime.now(timezone.utc)
    expires_at = as_utc(expires_at)
    if direction == "HOLD":
        if now >= expires_at:
            return _pack("neutral", pair, 0.0, 0.0, 0.0)
        return _pack("pending", pair, 0.0, 0.0, 0.0)

    max_fav = 0.0
    max_adv = 0.0
    for c in candles:
        high, low = c["high"], c["low"]
        if direction == "BUY":
            max_fav = max(max_fav, pips_from_price_move(pair, high - entry))
            max_adv = min(max_adv, pips_from_price_move(pair, low - entry))
            if low <= invalidation:
                return _pack("invalidated", pair, pips_from_price_move(pair, invalidation - entry), max_fav, max_adv)
            if low <= sl:
                return _pack("loss", pair, pips_from_price_move(pair, sl - entry), max_fav, max_adv)
            if high >= tp:
                return _pack("win", pair, pips_from_price_move(pair, tp - entry), max_fav, max_adv)
        if direction == "SELL":
            max_fav = max(max_fav, pips_from_price_move(pair, entry - low))
            max_adv = min(max_adv, pips_from_price_move(pair, entry - high))
            if high >= invalidation:
                return _pack("invalidated", pair, pips_from_price_move(pair, entry - invalidation), max_fav, max_adv)
            if high >= sl:
                return _pack("loss", pair, pips_from_price_move(pair, entry - sl), max_fav, max_adv)
            if low <= tp:
                return _pack("win", pair, pips_from_price_move(pair, entry - tp), max_fav, max_adv)

    if now >= expires_at:
        return _pack("expired", pair, 0.0, max_fav, max_adv)
    return _pack("pending", pair, 0.0, max_fav, max_adv)
