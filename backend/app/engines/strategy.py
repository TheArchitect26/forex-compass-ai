"""Strategy Evolution Engine — grid-search baseline; swap in Optuna/genetic later."""
from __future__ import annotations
from itertools import product
from .backtest import run_ema_cross


async def evolve_ema(pair: str, timeframe: str = "1h") -> dict:
    grid = list(product([10, 20, 30], [50, 100, 200]))
    results = []
    for f, s in grid:
        if f >= s: continue
        r = await run_ema_cross(pair, timeframe, f, s)
        results.append({"fast": f, "slow": s, "sharpe": r["metrics"]["sharpe"], "wr": r["metrics"]["win_rate"]})
    results.sort(key=lambda x: x["sharpe"], reverse=True)
    return {"pair": pair, "tested": len(results), "top": results[:5]}
