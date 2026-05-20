from __future__ import annotations
from datetime import UTC, datetime

SOVEREIGNTY_GUARANTEES = [
    "operator override always available",
    "no hidden adaptation",
    "no silent recommendation escalation",
    "no self-promoting strategic conclusions",
    "no irreversible autonomous changes",
    "human approval required for governance-sensitive operations",
]


def complexity_pressure(payload: dict) -> dict:
    score = 0.0
    score += float(payload.get("dashboard_overload", 0)) * 8
    score += float(payload.get("recommendation_saturation", 0)) * 10
    score += float(payload.get("unresolved_workflow_accumulation", 0)) * 9
    score += float(payload.get("alert_density", 0)) * 7
    score += float(payload.get("governance_burden", 0)) * 8
    score += float(payload.get("contradiction_backlog", 0)) * 9
    score += float(payload.get("investigation_sprawl", 0)) * 8
    score += float(payload.get("replay_backlog_pressure", 0)) * 7
    lvl = "low" if score < 25 else "elevated" if score < 55 else "high"
    return {"complexity_pressure_score": round(min(score, 100), 2), "level": lvl}


def simplification_engine(items: dict) -> dict:
    findings = items.get("findings", [])
    anomalies = items.get("anomalies", [])
    recs = items.get("recommendations", [])
    workflows = items.get("workflows", [])

    dedup_recs = []
    seen = set()
    for r in recs:
        k = str(r.get("recommendation", "")).strip().lower()
        if not k or k in seen:
            continue
        seen.add(k)
        dedup_recs.append(r)

    high_impact = sorted(workflows, key=lambda w: float(w.get("impact", 0)), reverse=True)[:5]
    low_value = [w for w in workflows if float(w.get("impact", 0)) < 0.3]
    return {
        "collapsed_findings": findings[:10],
        "grouped_anomalies": anomalies[:10],
        "merged_recommendations": dedup_recs,
        "low_value_workflows": low_value,
        "highest_impact_investigations": high_impact,
        "noise_suppression_applied": True,
    }


def operator_load(payload: dict) -> dict:
    cognitive = min(100.0, float(payload.get("complexity_pressure", 30)) * 0.6 + float(payload.get("alert_density", 20)) * 0.4)
    fatigue = min(100.0, float(payload.get("unresolved_issues", 10)) * 2 + float(payload.get("critical_alerts", 1)) * 8)
    clarity = max(0.0, 100.0 - float(payload.get("recommendation_saturation", 20)) * 1.2 - float(payload.get("contradictions", 5)) * 2)
    rec_sat = min(100.0, float(payload.get("recommendation_saturation", 20)) * 2)
    gov_burden = min(100.0, float(payload.get("governance_burden", 10)) * 3)
    return {
        "cognitive_load_score": round(cognitive, 2),
        "operational_fatigue_estimate": round(fatigue, 2),
        "strategic_clarity_score": round(clarity, 2),
        "recommendation_saturation_score": round(rec_sat, 2),
        "governance_burden_score": round(gov_burden, 2),
    }


def apply_focus_mode(mode: str, insights: list[dict]) -> list[dict]:
    key = mode.replace("_focus", "")
    if mode == "stability_focus":
        key = "stability"
    return [i for i in insights if key in str(i.get("tags", [])).lower() or key in str(i).lower()]


def explainability_layers(item: dict) -> dict:
    return {
        "executive_summary": item.get("summary", "No summary"),
        "strategic_explanation": item.get("strategy", "No strategic explanation"),
        "technical_detail": item.get("technical", "No technical detail"),
        "full_audit_chain": item.get("audit_chain", []),
        "reproducible": True,
    }


def reset_action(action: str, approved_by_human: bool) -> dict:
    return {
        "action": action,
        "approved_by_human": approved_by_human,
        "reversible": True,
        "auditable": True,
        "applied": bool(approved_by_human),
        "timestamp": datetime.now(UTC).isoformat(),
    }
