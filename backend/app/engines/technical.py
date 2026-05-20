"""Technical Analysis Engine — indicators + candlestick patterns."""
from __future__ import annotations
import numpy as np
import pandas as pd


def _ema(series: pd.Series, length: int) -> pd.Series:
    return series.ewm(span=length, adjust=False).mean()


def _rsi(series: pd.Series, length: int = 14) -> pd.Series:
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(alpha=1 / length, adjust=False, min_periods=length).mean()
    avg_loss = loss.ewm(alpha=1 / length, adjust=False, min_periods=length).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    return 100 - (100 / (1 + rs))


def _atr(high: pd.Series, low: pd.Series, close: pd.Series, length: int = 14) -> pd.Series:
    prev_close = close.shift(1)
    tr = pd.concat([(high - low), (high - prev_close).abs(), (low - prev_close).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / length, adjust=False, min_periods=length).mean()


def _adx(high: pd.Series, low: pd.Series, close: pd.Series, length: int = 14) -> pd.Series:
    up_move = high.diff()
    down_move = -low.diff()
    plus_dm = pd.Series(np.where((up_move > down_move) & (up_move > 0), up_move, 0.0), index=high.index)
    minus_dm = pd.Series(np.where((down_move > up_move) & (down_move > 0), down_move, 0.0), index=high.index)

    atr = _atr(high, low, close, length)
    plus_di = 100 * plus_dm.ewm(alpha=1 / length, adjust=False, min_periods=length).mean() / atr
    minus_di = 100 * minus_dm.ewm(alpha=1 / length, adjust=False, min_periods=length).mean() / atr

    di_sum = (plus_di + minus_di).replace(0, np.nan)
    dx = (100 * (plus_di - minus_di).abs() / di_sum).replace([np.inf, -np.inf], np.nan)
    return dx.ewm(alpha=1 / length, adjust=False, min_periods=length).mean()


def _stoch_rsi(series: pd.Series, rsi_length: int = 14, stoch_length: int = 14, k: int = 3) -> pd.Series:
    rsi = _rsi(series, rsi_length)
    min_rsi = rsi.rolling(stoch_length).min()
    max_rsi = rsi.rolling(stoch_length).max()
    stoch = (rsi - min_rsi) / (max_rsi - min_rsi).replace(0, np.nan)
    return (100 * stoch).rolling(k).mean()


def enrich(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["ema20"] = _ema(out["close"], 20)
    out["ema50"] = _ema(out["close"], 50)
    out["ema200"] = _ema(out["close"], 200)
    out["rsi"] = _rsi(out["close"], 14)

    macd_line = _ema(out["close"], 12) - _ema(out["close"], 26)
    macd_signal = macd_line.ewm(span=9, adjust=False).mean()
    out["MACD_12_26_9"] = macd_line
    out["MACDs_12_26_9"] = macd_signal
    out["MACDh_12_26_9"] = macd_line - macd_signal

    out["atr"] = _atr(out["high"], out["low"], out["close"], 14)

    bb_mid = out["close"].rolling(20).mean()
    bb_std = out["close"].rolling(20).std(ddof=0)
    out["BBL_20_2.0"] = bb_mid - (2 * bb_std)
    out["BBM_20_2.0"] = bb_mid
    out["BBU_20_2.0"] = bb_mid + (2 * bb_std)

    out["adx"] = _adx(out["high"], out["low"], out["close"], 14)
    out["stoch_rsi"] = _stoch_rsi(out["close"])
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
