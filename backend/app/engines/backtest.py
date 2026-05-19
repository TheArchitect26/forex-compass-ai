"""Backtesting Engine — vectorbt-powered EMA-cross baseline strategy.

Returns: equity curve, Sharpe, win rate, max drawdown, expectancy.
"""
from __future__ import annotations
import numpy as np
import pandas as pd


async def run_ema_cross(pair: str, timeframe: str = "1h", fast: int = 20, slow: int = 50) -> dict:
    from .market_data import market_data
    df = await market_data.ohlcv(pair, timeframe, 1000)
    close = df["close"].values
    ema_f = pd.Series(close).ewm(span=fast).mean().values
    ema_s = pd.Series(close).ewm(span=slow).mean().values

    pos = np.zeros(len(close))
    pos[ema_f > ema_s] = 1
    pos[ema_f < ema_s] = -1
    rets = np.diff(close) / close[:-1]
    strat = pos[:-1] * rets
    equity = np.cumprod(1 + strat)
    sharpe = float(strat.mean() / (strat.std() + 1e-9) * np.sqrt(252))
    wins = strat[strat > 0]; losses = strat[strat < 0]
    win_rate = float(len(wins) / max(len(wins) + len(losses), 1))
    avg_win = float(wins.mean()) if len(wins) else 0.0
    avg_loss = float(losses.mean()) if len(losses) else 0.0
    expectancy = win_rate * avg_win + (1 - win_rate) * avg_loss
    peak = np.maximum.accumulate(equity); dd = (equity - peak) / peak
    max_dd = float(dd.min())

    return {
        "strategy": "ema_cross", "pair": pair, "timeframe": timeframe,
        "params": {"fast": fast, "slow": slow},
        "metrics": {
            "sharpe": round(sharpe, 3),
            "win_rate": round(win_rate * 100, 2),
            "expectancy": round(expectancy * 10000, 4),
            "max_drawdown_pct": round(max_dd * 100, 2),
            "final_equity": round(float(equity[-1]), 4),
            "n_bars": int(len(close)),
        },
        "equity_curve": [
            {"t": str(t), "v": float(v)} for t, v in zip(df["datetime"].iloc[1:], equity)
        ][::max(1, len(equity)//200)],  # downsample
    }
