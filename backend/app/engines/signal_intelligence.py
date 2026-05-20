"""Signal Intelligence Engine — confluence, confidence, and explainable trust signals."""
from __future__ import annotations
from app.utils_time import utc_now
from .market_data import market_data
from . import technical, market_structure, regime, sentiment as sent, news as news_mod
from .risk import suggest_levels
from .signal_rules import evaluate_signal_components, assess_risk_and_strength



def regime_weight_adjustments(regime_name: str) -> dict:
    base = {"rsi": 1.0, "trend": 1.0, "momentum": 1.0, "volatility_breakout": 1.0}
    reasons = []
    if regime_name in {"trending", "breakout"}:
        base["rsi"] = 0.8; base["trend"] = 1.2; reasons.append("Trend-following weighted up; RSI mean-reversion weighted down")
    if regime_name in {"ranging", "low volatility"}:
        base["trend"] = 0.8; base["rsi"] = 1.2; reasons.append("Range regime increases RSI relevance and reduces trend-following")
    if regime_name in {"high volatility", "unstable"}:
        base["momentum"] = 0.9; base["volatility_breakout"] = 1.3; reasons.append("Volatility breakout weight increased under unstable conditions")
    return {"weights": base, "reasons": reasons}

INDICATORS_USED = [
    "trend_direction", "rsi", "macd", "moving_averages", "support_resistance", "atr_volatility", "candle_momentum"
]


async def analyze_pair(pair: str) -> dict:
    htf = await market_data.ohlcv(pair, "4h", 200)
    mtf = await market_data.ohlcv(pair, "1h", 200)
    ltf = await market_data.ohlcv(pair, "15min", 200)

    source_info = market_data.source_info(pair, "15min", 200)
    data_source = "real" if source_info.get("source") == "twelve_data" else "synthetic"

    tech_htf = technical.summary(htf)
    tech_mtf = technical.summary(mtf)
    tech_ltf = technical.summary(ltf)
    structure = market_structure.bos_choch(mtf)
    regime_details = regime.detect_details(mtf)
    market_regime = regime_details["regime"]
    patterns = technical.detect_candlestick(ltf)

    headlines = await news_mod.headlines()
    base, _ = pair.split("/")
    senti = sent.aggregate(headlines, currency=base)

    adaptive = regime_weight_adjustments(market_regime)
    confluence = evaluate_signal_components(tech_htf, tech_mtf, tech_ltf, structure, patterns)
    # gradual adaptive scaling (bounded, explainable)
    trend_adj = adaptive["weights"]["trend"]
    rsi_adj = adaptive["weights"]["rsi"]
    raw_conf = confluence["confidence"]
    confluence["confidence"] = max(5.0, min(100.0, raw_conf * ((trend_adj + rsi_adj) / 2)))
    direction = confluence["direction"]

    levels = suggest_levels(ltf, "BUY" if direction == "HOLD" else direction)
    invalidation_price = levels["sl"]
    risk_level, strength, risk_warnings = assess_risk_and_strength(
        direction=direction,
        confidence=confluence["confidence"],
        close=tech_ltf["close"],
        atr=tech_ltf["atr"],
        stop_loss=levels["sl"],
    )

    if data_source == "synthetic":
        risk_warnings.append(source_info.get("warning") or "Synthetic/demo market data is active")

    reason_summary = f"{direction} based on confluence: {confluence['bull_score']} bullish vs {confluence['bear_score']} bearish factors."

    reasoning = {
        "technical": {"htf": tech_htf, "mtf": tech_mtf, "ltf": tech_ltf},
        "structure": structure,
        "regime": market_regime,
        "regime_details": regime_details,
        "adaptive_weighting": adaptive,
        "patterns": patterns,
        "sentiment": senti,
        "confirmations": confluence["confirmations"],
        "contradictions": confluence["contradictions"],
        "risk_warnings": risk_warnings,
        "future_validation": {
            "outcome_window_bars": 24,
            "hit_take_profit": None,
            "hit_stop_loss": None,
            "resolved_at": None,
        },
    }

    explanation = (
        f"{direction} selected for {pair}. Confirms: {', '.join(confluence['confirmations']) or 'none'}. "
        f"Contradictions: {', '.join(confluence['contradictions']) or 'none'}. "
        f"Invalidation at {invalidation_price}. Risk={risk_level}."
    )

    signal = {
        "pair": pair,
        "timeframe": "15min",
        "direction": direction,
        "confidence": round(confluence["confidence"], 1),
        "strength": strength,
        "reason_summary": reason_summary,
        "indicators_used": INDICATORS_USED,
        "risk_level": risk_level,
        "invalidation_price": invalidation_price,
        "suggested_stop_loss_area": levels["sl"],
        "suggested_take_profit_area": levels["tp"],
        "timestamp": utc_now().isoformat(),
        "data_source": data_source,
        "entry": levels["entry"],
        "stop_loss": levels["sl"],
        "take_profit": levels["tp"],
        "risk_reward": levels["rr"],
        "market_regime": market_regime,
        "reasoning": reasoning,
        "explanation": explanation,
        "created_at": utc_now().isoformat(),
    }
    return {"pair": pair, "signal": signal, "regime": market_regime}
