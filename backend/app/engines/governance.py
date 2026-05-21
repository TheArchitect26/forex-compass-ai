from __future__ import annotations
from app.utils_time import utc_now


def regression_severity(baseline: dict, candidate: dict) -> str:
    penalties = 0
    if candidate.get("net_pips", 0) < baseline.get("net_pips", 0): penalties += 1
    if candidate.get("invalidation_rate", 0) > baseline.get("invalidation_rate", 0): penalties += 1
    if candidate.get("calibration_alignment", 0) < baseline.get("calibration_alignment", 0): penalties += 1
    if candidate.get("reliability", 0) < baseline.get("reliability", 0): penalties += 1
    if candidate.get("hold_rate", 0) > baseline.get("hold_rate", 0) * 1.3: penalties += 1
    if candidate.get("aggressiveness", 0) > baseline.get("aggressiveness", 0) * 1.4: penalties += 1
    if penalties <= 1:
        return "acceptable"
    if penalties == 2:
        return "warning"
    if penalties in (3, 4):
        return "regression"
    return "critical regression"


def compare_metrics(baseline: dict, candidate: dict) -> dict:
    sev = regression_severity(baseline, candidate)
    return {"severity": sev, "baseline": baseline, "candidate": candidate, "computed_at": utc_now().isoformat()}
