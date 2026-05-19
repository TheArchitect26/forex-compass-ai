"""AI Explanation Engine — produces analyst-grade natural language."""


def explain(pair: str, direction: str, reasoning: dict, levels: dict, confidence: float) -> str:
    t = reasoning["technical"]
    parts = []
    parts.append(
        f"{direction} setup on {pair} with {confidence:.0f}% confidence. "
        f"Higher timeframe (4H) is {t['htf']['trend']}, intermediate (1H) is {t['mtf']['trend']}, "
        f"and entry timeframe (15M) shows {t['ltf']['momentum']} momentum with RSI at {t['ltf']['rsi']:.1f}."
    )
    if reasoning["structure"]["state"] != "neutral":
        parts.append(f"Market structure: {reasoning['structure']['state'].replace('_', ' ')}.")
    if reasoning["patterns"]:
        parts.append(f"Price action: {', '.join(reasoning['patterns'])}.")
    s = reasoning["sentiment"]
    parts.append(f"News sentiment ({s['sample_size']} headlines) is {s['label']} ({s['score']:+.2f}).")
    parts.append(f"Regime: {reasoning['regime']}.")
    parts.append(
        f"Suggested entry {levels['entry']}, stop {levels['sl']}, target {levels['tp']} (R:R 1:{levels['rr']})."
    )
    parts.append("This is analysis only — execute manually after your own verification.")
    return " ".join(parts)
