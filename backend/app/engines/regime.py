"""Explainable market regime detection."""
from __future__ import annotations
import numpy as np
import pandas as pd
from .technical import enrich


def detect_details(df: pd.DataFrame) -> dict:
    d = enrich(df)
    last = d.iloc[-1]
    prev = d.iloc[-6] if len(d) > 6 else d.iloc[0]
    adx = float(0 if np.isnan(last.get("adx", 0)) else last.get("adx", 0))
    atr = float(last.get("atr", 0))
    close = float(last.get("close", 1))
    atr_pct = atr / close if close else 0
    ma_slope = float((last.get("ema50", close) - prev.get("ema50", close)) / close)
    momentum_consistency = float((d["close"].diff().tail(10) > 0).sum() / max(1, len(d.tail(10))))
    compression = float(d["atr"].tail(20).std() / max(1e-9, d["atr"].tail(20).mean())) if "atr" in d else 0.0

    warnings = []
    if atr_pct > 0.02:
        regime = "high volatility"; confidence = 82
    elif atr_pct < 0.0007:
        regime = "low volatility"; confidence = 76
    elif adx > 28 and abs(ma_slope) > 0.001:
        regime = "trending"; confidence = 78
    elif adx < 18 and atr_pct < 0.006:
        regime = "ranging"; confidence = 72
    elif compression < 0.12 and adx > 20:
        regime = "breakout"; confidence = 68
    elif momentum_consistency < 0.45:
        regime = "unstable"; confidence = 62
    else:
        regime = "news-sensitive"; confidence = 55; warnings.append("Mixed conditions; treat signals cautiously")

    return {
        "regime": regime,
        "confidence": confidence,
        "metrics": {
            "adx": round(adx, 2), "atr_pct": round(atr_pct, 5), "ma_slope": round(ma_slope, 5),
            "momentum_consistency": round(momentum_consistency, 2), "compression": round(compression, 3),
        },
        "warnings": warnings,
    }


def detect(df: pd.DataFrame) -> str:
    return detect_details(df)["regime"]
