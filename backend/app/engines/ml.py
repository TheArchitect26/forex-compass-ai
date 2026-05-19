"""Machine Learning Engine — XGBoost win-probability model.

Trains on Signal outcomes stored in DB. LSTM/RL stubs in separate modules.
"""
from __future__ import annotations
import os, joblib, numpy as np
from pathlib import Path

MODEL_DIR = Path(os.getenv("MODEL_DIR", "/app/models"))
MODEL_DIR.mkdir(exist_ok=True, parents=True)
MODEL_PATH = MODEL_DIR / "xgb_winprob.pkl"


def _features(signal: dict) -> np.ndarray:
    r = signal["reasoning"]
    t = r["technical"]
    return np.array([
        signal["confidence"],
        signal["risk_reward"],
        t["htf"]["rsi"], t["mtf"]["rsi"], t["ltf"]["rsi"],
        t["ltf"]["atr"] / max(t["ltf"]["close"], 1e-9),
        r["sentiment"]["score"],
        1 if r["structure"]["state"].endswith("bos") else 0,
        len(r["patterns"]),
    ], dtype=float)


def train(signals: list[dict]) -> dict:
    try:
        from xgboost import XGBClassifier
    except ImportError:
        return {"status": "xgboost not installed"}
    closed = [s for s in signals if s.get("status") in ("win", "loss")]
    if len(closed) < 30:
        return {"status": f"need >=30 closed signals, have {len(closed)}"}
    X = np.stack([_features(s) for s in closed])
    y = np.array([1 if s["status"] == "win" else 0 for s in closed])
    model = XGBClassifier(n_estimators=200, max_depth=4, learning_rate=0.05, eval_metric="logloss")
    model.fit(X, y)
    joblib.dump(model, MODEL_PATH)
    acc = float((model.predict(X) == y).mean())
    return {"status": "trained", "samples": len(closed), "train_accuracy": acc}


def predict_win_prob(signal: dict) -> float | None:
    if not MODEL_PATH.exists(): return None
    model = joblib.load(MODEL_PATH)
    return float(model.predict_proba(_features(signal).reshape(1, -1))[0][1])
