"""Technical Analysis Engine — indicators + candlestick patterns."""
from __future__ import annotations
import numpy as np
import pandas as pd
import pandas_ta as ta


def enrich(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["ema20"] = ta.ema(out["close"], length=20)
    out["ema50"] = ta.ema(out["close"], length=50)
    out["ema200"] = ta.ema(out["close"], length=200)
    out["rsi"] = ta.rsi(out["close"], length=14)
    macd = ta.macd(out["close"])
    if macd is not None:
        out = pd.concat([out, macd], axis=1)
    out["atr"] = ta.atr(out["high"], out["low"], out["close"], length=14)
    bb = ta.bbands(out["close"], length=20)
    if bb is not None:
        out = pd.concat([out, bb], axis=1)
    out["adx"] = ta.adx(out["high"], out["low"], out["close"], length=14)["ADX_14"]
    out["stoch_rsi"] = ta.stochrsi(out["close"])["STOCHRSIk_14_14_3_3"]
    return out


def summary(df: pd.DataFrame) -> dict:
    d = enrich(df).iloc[-1]
    prev = enrich(df).iloc[-2]
    trend = "bullish" if d["ema20"] > d["ema50"] > d["ema200"] else \
            "bearish" if d["ema20"] < d["ema50"] < d["ema200"] else "neutral"
    rsi_state = "overbought" if d["rsi"] > 70 else "oversold" if d["rsi"] < 30 else "neutral"
    return {
        "trend": trend,
        "rsi": float(d["rsi"]),
        "rsi_state": rsi_state,
        "adx": float(d["adx"]) if not np.isnan(d["adx"]) else 0.0,
        "atr": float(d["atr"]),
        "close": float(d["close"]),
        "momentum": "up" if d["close"] > prev["close"] else "down",
    }


def detect_candlestick(df: pd.DataFrame) -> list[str]:
    """Lightweight pattern detection (no TA-Lib dependency)."""
    patterns: list[str] = []
    if len(df) < 2: return patterns
    a, b = df.iloc[-2], df.iloc[-1]
    body_b = abs(b["close"] - b["open"])
    range_b = b["high"] - b["low"]
    if range_b == 0: return patterns
    upper = b["high"] - max(b["close"], b["open"])
    lower = min(b["close"], b["open"]) - b["low"]
    # Doji
    if body_b <= 0.1 * range_b: patterns.append("doji")
    # Pin bar
    if lower > 2 * body_b and upper < body_b: patterns.append("bullish_pin")
    if upper > 2 * body_b and lower < body_b: patterns.append("bearish_pin")
    # Engulfing
    if b["close"] > b["open"] and a["close"] < a["open"] and b["close"] > a["open"] and b["open"] < a["close"]:
        patterns.append("bullish_engulfing")
    if b["close"] < b["open"] and a["close"] > a["open"] and b["close"] < a["open"] and b["open"] > a["close"]:
        patterns.append("bearish_engulfing")
    return patterns
