from __future__ import annotations


def evaluate_signal_components(tech_htf: dict, tech_mtf: dict, tech_ltf: dict, structure: dict, patterns: list[str]) -> dict:
    confirms: list[str] = []
    contradicts: list[str] = []
    bull = 0
    bear = 0

    trends = [tech_htf["trend"], tech_mtf["trend"], tech_ltf["trend"]]
    if trends.count("bullish") >= 2:
        bull += 2
        confirms.append("Trend is bullish across timeframes")
    elif trends.count("bearish") >= 2:
        bear += 2
        confirms.append("Trend is bearish across timeframes")
    else:
        contradicts.append("Trend alignment is mixed")

    rsi = tech_ltf["rsi"]
    if rsi < 35:
        bull += 1
        confirms.append("RSI is near oversold and supports upside reversion")
    elif rsi > 65:
        bear += 1
        confirms.append("RSI is near overbought and supports downside reversion")
    else:
        contradicts.append("RSI is neutral")

    if tech_ltf.get("momentum") == "up":
        bull += 1
        confirms.append("Recent candle momentum is up")
    else:
        bear += 1
        confirms.append("Recent candle momentum is down")

    if structure.get("state") == "bullish_bos":
        bull += 2
        confirms.append("Support/resistance structure shows bullish BOS")
    elif structure.get("state") == "bearish_bos":
        bear += 2
        confirms.append("Support/resistance structure shows bearish BOS")
    else:
        contradicts.append("No clean structure break")

    if any(p in patterns for p in ("bullish_engulfing", "bullish_pin")):
        bull += 1
        confirms.append("Bullish candle pattern confirmation")
    if any(p in patterns for p in ("bearish_engulfing", "bearish_pin")):
        bear += 1
        confirms.append("Bearish candle pattern confirmation")

    if bull >= bear + 2 and bull >= 5:
        direction = "BUY"
    elif bear >= bull + 2 and bear >= 5:
        direction = "SELL"
    else:
        direction = "HOLD"
        contradicts.append("Indicator confluence is conflicting")

    lead = abs(bull - bear)
    raw_score = min(100, 45 + lead * 10)
    if direction == "HOLD":
        raw_score = min(raw_score, 45)

    return {
        "direction": direction,
        "confidence": float(raw_score),
        "confirmations": confirms,
        "contradictions": contradicts,
        "bull_score": bull,
        "bear_score": bear,
    }


def assess_risk_and_strength(direction: str, confidence: float, close: float, atr: float, stop_loss: float) -> tuple[str, str, list[str]]:
    warnings: list[str] = []
    atr_pct = atr / close if close else 0
    stop_distance_pct = abs(close - stop_loss) / close if close else 0

    risk_level = "medium"
    if atr_pct < 0.0005:
        warnings.append("Very low volatility can produce weak follow-through")
    if atr_pct > 0.02:
        warnings.append("Extreme ATR volatility detected")
        risk_level = "high"
    if stop_distance_pct > 0.02:
        warnings.append("Stop-loss distance is wide relative to price")
        risk_level = "high"

    if direction == "HOLD" or confidence < 55 or atr_pct < 0.0005:
        strength = "weak"
    elif confidence >= 75 and risk_level != "high":
        strength = "strong"
    else:
        strength = "medium"

    return risk_level, strength, warnings
