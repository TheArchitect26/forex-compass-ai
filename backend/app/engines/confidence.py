"""Confidence Engine — weighted, transparent scoring. No fake certainty."""


WEIGHTS = {
    "trend_alignment": 0.25,
    "structure": 0.15,
    "momentum": 0.10,
    "patterns": 0.10,
    "regime_fit": 0.10,
    "sentiment": 0.10,
    "rsi_position": 0.10,
    "volatility_ok": 0.10,
}


def score_confidence(direction, tech_htf, tech_mtf, tech_ltf, structure, regime, sentiment, patterns) -> dict:
    contrib: dict[str, float] = {}

    aligned = sum(1 for s in (tech_htf, tech_mtf, tech_ltf)
                  if (direction == "BUY" and s["trend"] == "bullish") or
                     (direction == "SELL" and s["trend"] == "bearish"))
    contrib["trend_alignment"] = aligned / 3.0

    contrib["structure"] = 1.0 if (
        (direction == "BUY" and structure["state"] == "bullish_bos") or
        (direction == "SELL" and structure["state"] == "bearish_bos")
    ) else 0.3

    contrib["momentum"] = 1.0 if (
        (direction == "BUY" and tech_ltf["momentum"] == "up") or
        (direction == "SELL" and tech_ltf["momentum"] == "down")
    ) else 0.2

    good = {"BUY": ("bullish_engulfing","bullish_pin"), "SELL": ("bearish_engulfing","bearish_pin")}[direction]
    contrib["patterns"] = 1.0 if any(p in patterns for p in good) else 0.4

    contrib["regime_fit"] = {"trending": 1.0, "volatile": 0.6, "mixed": 0.5, "ranging": 0.3}.get(regime, 0.5)

    s = sentiment["score"]
    contrib["sentiment"] = max(0.0, min(1.0, (s + 1) / 2)) if direction == "BUY" else max(0.0, min(1.0, (-s + 1) / 2))

    rsi = tech_ltf["rsi"]
    if direction == "BUY":
        contrib["rsi_position"] = 1.0 if 35 < rsi < 65 else 0.5 if rsi <= 35 else 0.2
    else:
        contrib["rsi_position"] = 1.0 if 35 < rsi < 65 else 0.5 if rsi >= 65 else 0.2

    atr_pct = tech_ltf["atr"] / tech_ltf["close"]
    contrib["volatility_ok"] = 1.0 if 0.0005 < atr_pct < 0.015 else 0.3

    score = sum(WEIGHTS[k] * v for k, v in contrib.items())
    return {"score": round(score * 100, 1), "breakdown": {k: round(v, 2) for k, v in contrib.items()}}
