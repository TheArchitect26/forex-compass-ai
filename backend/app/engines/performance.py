"""Performance Analytics Engine — aggregates journal + signal outcomes."""
from __future__ import annotations
from collections import defaultdict


def summarize(signals: list[dict]) -> dict:
    closed = [s for s in signals if s.get("status") in ("win", "loss")]
    n = len(closed); wins = sum(1 for s in closed if s["status"] == "win")
    by_pair: dict[str, dict] = defaultdict(lambda: {"n": 0, "wins": 0, "pnl": 0.0})
    by_regime: dict[str, dict] = defaultdict(lambda: {"n": 0, "wins": 0})
    for s in closed:
        by_pair[s["pair"]]["n"] += 1
        by_pair[s["pair"]]["wins"] += 1 if s["status"] == "win" else 0
        by_pair[s["pair"]]["pnl"] += s.get("pnl_pips") or 0.0
        by_regime[s["market_regime"]]["n"] += 1
        by_regime[s["market_regime"]]["wins"] += 1 if s["status"] == "win" else 0
    return {
        "total": n,
        "win_rate": round(wins / n * 100, 2) if n else 0.0,
        "by_pair": dict(by_pair),
        "by_regime": dict(by_regime),
    }
