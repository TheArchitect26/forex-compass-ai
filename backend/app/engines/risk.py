"""Risk Management Engine — SL/TP from ATR, position sizing, sanity checks."""
import pandas as pd
from .technical import enrich


def suggest_levels(df: pd.DataFrame, direction: str, rr: float = 2.5, atr_mult: float = 1.5) -> dict:
    d = enrich(df).iloc[-1]
    price = float(d["close"]); atr = float(d["atr"])
    if direction == "BUY":
        sl = price - atr * atr_mult
        tp = price + (price - sl) * rr
    else:
        sl = price + atr * atr_mult
        tp = price - (sl - price) * rr
    return {"entry": round(price, 5), "sl": round(sl, 5), "tp": round(tp, 5), "rr": rr}


def position_size(account_balance: float, risk_pct: float, entry: float, sl: float,
                  pip_value: float = 10.0) -> dict:
    risk_amount = account_balance * (risk_pct / 100.0)
    stop_pips = abs(entry - sl) * 10000
    if stop_pips == 0: return {"lots": 0.0, "risk_amount": risk_amount}
    lots = risk_amount / (stop_pips * pip_value)
    return {"lots": round(lots, 2), "risk_amount": round(risk_amount, 2), "stop_pips": round(stop_pips, 1)}


def is_dangerous(regime: str, atr_pct: float, near_high_impact_news: bool) -> tuple[bool, str]:
    if near_high_impact_news: return True, "High-impact news within window"
    if atr_pct > 0.02: return True, "Extreme volatility"
    if regime == "ranging" and atr_pct < 0.0003: return True, "Dead liquidity"
    return False, "ok"
