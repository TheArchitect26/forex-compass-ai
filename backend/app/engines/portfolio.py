from __future__ import annotations
from dataclasses import dataclass, asdict
from app.engines.assets import get_asset_meta


def correlation_bucket(a: str, b: str) -> str:
    if a == b:
        return "positive"
    majors = {"EUR/USD", "GBP/USD", "AUD/USD", "NZD/USD"}
    inv_usd = {"USD/JPY", "USD/CAD", "USD/CHF"}
    if a in majors and b in majors:
        return "positive"
    if (a in majors and b in inv_usd) or (a in inv_usd and b in majors):
        return "inverse"
    return "uncertain"


def estimate_position_size(mode: str, balance: float, confidence: float, atr_pct: float, fixed_lot: float = 0.1) -> float:
    if mode == "fixed_lot":
        return fixed_lot
    if mode == "fixed_risk":
        return max(0.01, min(2.0, balance * 0.01 / 1000))
    if mode == "volatility_adjusted":
        return max(0.01, min(2.0, 0.2 / max(0.001, atr_pct)))
    if mode == "confidence_adjusted":
        return max(0.01, min(2.0, confidence / 100))
    if mode == "capped_exposure":
        return max(0.01, min(0.5, balance * 0.005 / 1000))
    return 0.1


def compute_metrics(equity_curve: list[float]) -> dict:
    if not equity_curve:
        return {"max_drawdown": 0, "recovery_factor": 0, "expectancy": 0, "sharpe_like": 0}
    peak = equity_curve[0]
    max_dd = 0
    rets = []
    for i, e in enumerate(equity_curve):
        peak = max(peak, e)
        dd = (peak - e)
        max_dd = max(max_dd, dd)
        if i > 0:
            rets.append(equity_curve[i] - equity_curve[i-1])
    profit = equity_curve[-1] - equity_curve[0]
    recovery = profit / max(1e-9, max_dd)
    exp = profit / max(1, len(rets))
    mean = (sum(rets) / max(1, len(rets))) if rets else 0
    var = (sum((r - mean) ** 2 for r in rets) / max(1, len(rets))) if rets else 0
    sharpe = mean / (var ** 0.5 + 1e-9)
    return {"max_drawdown": round(max_dd, 2), "recovery_factor": round(recovery, 3), "expectancy": round(exp, 3), "sharpe_like": round(sharpe, 3)}
