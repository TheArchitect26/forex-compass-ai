from __future__ import annotations
from datetime import datetime, timedelta
from app.utils_time import utc_now


def apply_quality_gates(signal: dict, min_confidence: float) -> dict:
    s = dict(signal)
    if s.get("direction") in {"BUY", "SELL"} and s.get("confidence", 0) < min_confidence:
        s["direction"] = "HOLD"
        s["strength"] = "weak"
        s["reason_summary"] = f"{s.get('reason_summary','')} Downgraded: low confidence.".strip()
    if s.get("risk_level") == "high" and s.get("strength") == "strong":
        s["strength"] = "medium"
    return s


def blocked_by_synthetic_policy(signal: dict, allow_synthetic: bool) -> bool:
    return signal.get("data_source") == "synthetic" and not allow_synthetic and signal.get("direction") in {"BUY", "SELL"}


def is_duplicate_recent(existing_created_at: datetime | None, cooldown_minutes: int) -> bool:
    if not existing_created_at:
        return False
    return existing_created_at >= utc_now() - timedelta(minutes=cooldown_minutes)
