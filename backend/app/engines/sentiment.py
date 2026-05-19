"""Sentiment Engine — lightweight lexicon; swap in FinBERT in prod.

The interface stays stable; replace `score_text` with a transformer pipeline
without touching callers.
"""
from __future__ import annotations

_POS = {"surge","gain","rally","beat","strong","bullish","upbeat","optimistic","rise","outperform","record"}
_NEG = {"fall","drop","plunge","miss","weak","bearish","downbeat","pessimistic","slump","underperform","cut"}


def score_text(text: str) -> float:
    t = text.lower()
    p = sum(1 for w in _POS if w in t)
    n = sum(1 for w in _NEG if w in t)
    if p + n == 0: return 0.0
    return (p - n) / (p + n)


def aggregate(headlines: list[dict], currency: str | None = None) -> dict:
    rel = headlines
    if currency:
        rel = [h for h in headlines if currency.upper() in h.get("title", "").upper()]
    scores = [score_text(h.get("title", "")) for h in rel] or [0.0]
    avg = sum(scores) / len(scores)
    return {
        "score": avg,
        "label": "bullish" if avg > 0.15 else "bearish" if avg < -0.15 else "neutral",
        "sample_size": len(rel),
    }
