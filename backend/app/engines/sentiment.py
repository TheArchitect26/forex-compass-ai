"""Sentiment Engine — provider scores when available, lexicon fallback otherwise."""
from __future__ import annotations

_POS = {
    "surge", "gain", "rally", "beat", "strong", "bullish", "upbeat",
    "optimistic", "rise", "outperform", "record", "rebound", "growth",
}
_NEG = {
    "fall", "drop", "plunge", "miss", "weak", "bearish", "downbeat",
    "pessimistic", "slump", "underperform", "cut", "recession", "risk",
}


def score_text(text: str) -> float:
    value = text.lower()
    positive = sum(1 for word in _POS if word in value)
    negative = sum(1 for word in _NEG if word in value)
    if positive + negative == 0:
        return 0.0
    return (positive - negative) / (positive + negative)


def _provider_score(headline: dict) -> float | None:
    value = headline.get("sentiment_score")
    if value is None:
        return None
    try:
        score = float(value)
    except (TypeError, ValueError):
        return None
    return max(-1.0, min(1.0, score))


def aggregate(headlines: list[dict], currency: str | None = None) -> dict:
    relevant = headlines
    if currency:
        needle = currency.upper()
        relevant = [
            headline
            for headline in headlines
            if needle in (
                f"{headline.get('title', '')} {headline.get('summary', '')}"
            ).upper()
        ]

    scores: list[float] = []
    provider_score_count = 0
    for headline in relevant:
        provider_score = _provider_score(headline)
        if provider_score is not None:
            scores.append(provider_score)
            provider_score_count += 1
        else:
            scores.append(
                score_text(
                    f"{headline.get('title', '')} {headline.get('summary', '')}"
                )
            )

    if not scores:
        scores = [0.0]

    average = sum(scores) / len(scores)
    return {
        "score": average,
        "label": (
            "bullish"
            if average > 0.15
            else "bearish"
            if average < -0.15
            else "neutral"
        ),
        "sample_size": len(relevant),
        "provider_score_count": provider_score_count,
        "lexicon_score_count": max(0, len(relevant) - provider_score_count),
    }
