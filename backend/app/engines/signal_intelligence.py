"""Signal Intelligence Engine — fuses technical, structure, regime, news, sentiment.

Outputs structured Signal dicts with confidence + full reasoning.
"""
from __future__ import annotations
from datetime import datetime
from .market_data import market_data
from . import technical, market_structure, regime, sentiment as sent, news as news_mod
from .confidence import score_confidence
from .risk import suggest_levels
from .explanation import explain


async def analyze_pair(pair: str) -> dict:
    htf = await market_data.ohlcv(pair, "4h", 200)
    mtf = await market_data.ohlcv(pair, "1h", 200)
    ltf = await market_data.ohlcv(pair, "15min", 200)

    tech_htf = technical.summary(htf)
    tech_mtf = technical.summary(mtf)
    tech_ltf = technical.summary(ltf)
    structure = market_structure.bos_choch(mtf)
    market_regime = regime.detect(mtf)
    patterns = technical.detect_candlestick(ltf)

    headlines = await news_mod.headlines()
    base, quote = pair.split("/")
    senti = sent.aggregate(headlines, currency=base)

    direction = _decide_direction(tech_htf, tech_mtf, tech_ltf, structure, patterns)
    if direction is None:
        return {"pair": pair, "signal": None, "regime": market_regime, "reason": "no confluence"}

    levels = suggest_levels(ltf, direction)
    conf_breakdown = score_confidence(
        direction=direction,
        tech_htf=tech_htf, tech_mtf=tech_mtf, tech_ltf=tech_ltf,
        structure=structure, regime=market_regime,
        sentiment=senti, patterns=patterns,
    )
    reasoning = {
        "technical": {"htf": tech_htf, "mtf": tech_mtf, "ltf": tech_ltf},
        "structure": structure,
        "regime": market_regime,
        "patterns": patterns,
        "sentiment": senti,
        "confidence_breakdown": conf_breakdown,
    }
    explanation = explain(pair, direction, reasoning, levels, conf_breakdown["score"])
    return {
        "pair": pair,
        "signal": {
            "pair": pair, "direction": direction,
            "entry": levels["entry"], "stop_loss": levels["sl"], "take_profit": levels["tp"],
            "risk_reward": levels["rr"], "confidence": conf_breakdown["score"],
            "market_regime": market_regime, "timeframe": "15min",
            "reasoning": reasoning, "explanation": explanation,
            "created_at": datetime.utcnow().isoformat(),
        },
    }


def _decide_direction(htf, mtf, ltf, structure, patterns) -> str | None:
    bull_score = 0; bear_score = 0
    for s in (htf, mtf, ltf):
        if s["trend"] == "bullish": bull_score += 1
        elif s["trend"] == "bearish": bear_score += 1
    if structure["state"] == "bullish_bos": bull_score += 1
    if structure["state"] == "bearish_bos": bear_score += 1
    if "bullish_engulfing" in patterns or "bullish_pin" in patterns: bull_score += 1
    if "bearish_engulfing" in patterns or "bearish_pin" in patterns: bear_score += 1
    if bull_score >= 3 and bull_score - bear_score >= 2: return "BUY"
    if bear_score >= 3 and bear_score - bull_score >= 2: return "SELL"
    return None
