"""Market Structure Engine — swing highs/lows, BOS, CHOCH, FVG, order blocks."""
from __future__ import annotations
import pandas as pd


def swings(df: pd.DataFrame, lookback: int = 3) -> dict:
    highs, lows = [], []
    for i in range(lookback, len(df) - lookback):
        win = df.iloc[i - lookback:i + lookback + 1]
        if df.iloc[i]["high"] == win["high"].max(): highs.append((i, float(df.iloc[i]["high"])))
        if df.iloc[i]["low"] == win["low"].min(): lows.append((i, float(df.iloc[i]["low"])))
    return {"highs": highs[-5:], "lows": lows[-5:]}


def bos_choch(df: pd.DataFrame) -> dict:
    s = swings(df)
    last_high = s["highs"][-1][1] if s["highs"] else None
    last_low = s["lows"][-1][1] if s["lows"] else None
    close = float(df.iloc[-1]["close"])
    state = "neutral"
    if last_high and close > last_high: state = "bullish_bos"
    elif last_low and close < last_low: state = "bearish_bos"
    return {"state": state, "last_high": last_high, "last_low": last_low}


def fair_value_gaps(df: pd.DataFrame) -> list[dict]:
    gaps = []
    for i in range(2, len(df)):
        a, b, c = df.iloc[i-2], df.iloc[i-1], df.iloc[i]
        if a["high"] < c["low"]:
            gaps.append({"type": "bullish", "low": float(a["high"]), "high": float(c["low"]), "index": i})
        if a["low"] > c["high"]:
            gaps.append({"type": "bearish", "low": float(c["high"]), "high": float(a["low"]), "index": i})
    return gaps[-10:]
