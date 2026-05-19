"""Market Regime Detection."""
import numpy as np
import pandas as pd
from .technical import enrich


def detect(df: pd.DataFrame) -> str:
    d = enrich(df)
    adx = d["adx"].iloc[-1]
    atr = d["atr"].iloc[-1]
    atr_pct = atr / d["close"].iloc[-1]
    if np.isnan(adx): adx = 0
    if adx > 25 and atr_pct < 0.01: return "trending"
    if adx < 20 and atr_pct < 0.005: return "ranging"
    if atr_pct > 0.012: return "volatile"
    return "mixed"
