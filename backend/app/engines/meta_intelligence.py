from __future__ import annotations


def synthesize_strategic_view(signals: dict) -> dict:
    regime = float(signals.get("regime_instability", 0))
    drift = float(signals.get("drift_pressure", 0))
    integrity = float(signals.get("integrity_degradation", 0))
    reliability_drop = float(signals.get("reliability_drop", 0))
    workload = float(signals.get("workload_pressure", 0))

    summary = []
    if regime > 60 and reliability_drop > 8:
        summary.append("High-volatility regime instability degrading aggressive profile reliability.")
    if integrity > 55:
        summary.append("Replay integrity weakened due to ingestion gap anomalies.")
    if float(signals.get("usd_concentration_risk", 0)) > 65:
        summary.append("Portfolio concentration risk elevated during correlated USD exposure.")

    strategic_stability = max(0.0, 100.0 - (regime * 0.25 + drift * 0.2 + integrity * 0.25 + reliability_drop * 2.0))
    operational_pressure = min(100.0, workload * 0.7 + drift * 0.3)
    intelligence_confidence = max(0.0, 100.0 - abs(drift - regime) * 0.4)
    anomaly_pressure = min(100.0, integrity * 0.5 + regime * 0.3 + drift * 0.2)
    governance_integrity = max(0.0, 100.0 - integrity * 0.8)

    return {
        "summary": summary or ["Strategic posture stable; continue monitored research cadence."],
        "scores": {
            "strategic_stability_score": round(strategic_stability, 2),
            "operational_pressure_score": round(operational_pressure, 2),
            "intelligence_confidence_score": round(intelligence_confidence, 2),
            "anomaly_pressure_score": round(anomaly_pressure, 2),
            "governance_integrity_score": round(governance_integrity, 2),
        },
    }


def detect_anomalies(payload: dict) -> list[dict]:
    anomalies = []
    if float(payload.get("replay_outlier_rate", 0)) > 0.25:
        anomalies.append({
            "type": "unusual_replay_outcomes",
            "confidence": 0.76,
            "likely_causes": ["dataset_gaps", "regime_transition"],
            "impact_scope": ["replay", "calibration"],
            "evidence": payload.get("replay_evidence", []),
            "reproducible": True,
        })
    if float(payload.get("calibration_drift_jump", 0)) > 15:
        anomalies.append({
            "type": "sudden_calibration_drift",
            "confidence": 0.81,
            "likely_causes": ["volatility_shift", "profile_mismatch"],
            "impact_scope": ["signal_quality", "reliability"],
            "evidence": payload.get("drift_evidence", []),
            "reproducible": True,
        })
    if int(payload.get("workload_spike", 0)) > 0:
        anomalies.append({
            "type": "workload_spike",
            "confidence": 0.72,
            "likely_causes": ["batch_fanout", "retry_storm"],
            "impact_scope": ["operator", "throughput"],
            "evidence": payload.get("workload_evidence", []),
            "reproducible": True,
        })
    return anomalies


def detect_recommendation_conflicts(recommendations: list[dict]) -> list[dict]:
    conflicts = []
    texts = [str(r.get("recommendation", "")).lower() for r in recommendations]
    if any("aggressive" in t and "increase" in t for t in texts) and any("reduce exposure" in t or "reduced exposure" in t for t in texts):
        conflicts.append({
            "conflict": "exploration_vs_exposure",
            "description": "One recommendation increases aggressive exploration while another reduces exposure.",
            "reproducible": True,
        })
    return conflicts


def dependency_map_snapshot(payload: dict) -> list[dict]:
    return [
        {"source": "integrity_degradation", "target": "replay_instability", "weight": float(payload.get("integrity_to_replay", 0.7))},
        {"source": "replay_instability", "target": "calibration_drift", "weight": float(payload.get("replay_to_drift", 0.6))},
        {"source": "workload_pressure", "target": "governance_incidents", "weight": float(payload.get("workload_to_governance", 0.4))},
        {"source": "regime_instability", "target": "portfolio_stress", "weight": float(payload.get("regime_to_stress", 0.65))},
    ]
