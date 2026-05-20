from __future__ import annotations

PROFILES = {
    "scalping": {"min_confidence": 64, "risk_tolerance": "medium", "cooldown_minutes": 20},
    "intraday": {"min_confidence": 62, "risk_tolerance": "medium", "cooldown_minutes": 30},
    "swing": {"min_confidence": 60, "risk_tolerance": "medium", "cooldown_minutes": 90},
    "conservative": {"min_confidence": 72, "risk_tolerance": "low", "cooldown_minutes": 120},
    "aggressive": {"min_confidence": 55, "risk_tolerance": "high", "cooldown_minutes": 15},
}

def profile_or_default(name: str | None) -> dict:
    n = name if name in PROFILES else "intraday"
    return {"name": n, **PROFILES[n]}
