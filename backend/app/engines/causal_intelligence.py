from __future__ import annotations


def causal_status() -> dict:
    return {
        "domains": [
            "reliability_drops",
            "governance_fragmentation",
            "operator_overload",
            "replay_debt",
            "data_integrity_degradation",
            "attention_fatigue",
            "mission_drift",
            "confidence_inflation",
            "pathway_failures",
            "scenario_regressions",
        ],
        "advisory_only": True,
        "auto_apply": False,
    }


def causal_graph(payload: dict) -> dict:
    nodes = payload.get("nodes", [
        "data_integrity", "replay_confidence", "calibration_quality", "signal_reliability",
        "governance_pressure", "operator_load", "attention_fatigue", "strategic_clarity",
        "scenario_outcomes", "pathway_recommendations",
    ])
    edges = payload.get("edges", [
        ["data_integrity", "replay_confidence"],
        ["replay_confidence", "calibration_quality"],
        ["calibration_quality", "signal_reliability"],
        ["signal_reliability", "governance_pressure"],
        ["governance_pressure", "operator_load"],
        ["operator_load", "attention_fatigue"],
        ["attention_fatigue", "strategic_clarity"],
    ])
    return {"nodes": nodes, "edges": edges, "note": "graph encodes hypotheses, not proof"}


def analyze_root_cause(payload: dict) -> dict:
    root_causes = payload.get("root_causes", [
        {"cause": "data_integrity_degradation", "score": 0.81},
        {"cause": "replay_debt", "score": 0.69},
        {"cause": "operator_overload", "score": 0.63},
    ])
    root_causes = sorted(root_causes, key=lambda x: float(x.get("score", 0)), reverse=True)
    return {
        "likely_root_causes": root_causes,
        "contributing_factors": payload.get("contributing_factors", ["governance backlog", "calibration drift"]),
        "amplifiers": payload.get("amplifiers", ["attention fragmentation", "confidence inflation"]),
        "downstream_effects": payload.get("downstream_effects", ["reliability decline", "strategy hesitation"]),
        "confidence_level": float(payload.get("confidence_level", 0.62)),
        "evidence_references": payload.get("evidence_references", ["reliability_history", "replay_validation_runs"]),
        "uncertainty_notes": payload.get("uncertainty_notes", ["causal links inferred from partial telemetry", "correlation does not imply causation"]),
        "advisory_only": True,
    }


def propagation_estimate(payload: dict) -> dict:
    chain = payload.get("chain", [
        "data_integrity_degradation",
        "replay_confidence_drop",
        "calibration_uncertainty",
        "reliability_decline",
        "governance_pressure_increase",
    ])
    return {
        "propagation_chain": chain,
        "estimated_pressure_gain": float(payload.get("estimated_pressure_gain", 0.37)),
        "uncertainty_notes": ["propagation magnitude is estimate, not deterministic"],
        "advisory_only": True,
    }


def intervention_effect(payload: dict) -> dict:
    return {
        "intervention": payload.get("intervention", "run_data_integrity_repair_pathway"),
        "likely_benefit": float(payload.get("likely_benefit", 0.71)),
        "affected_systems": payload.get("affected_systems", ["data_integrity", "replay_confidence", "signal_reliability"]),
        "second_order_risks": payload.get("second_order_risks", ["temporary research slowdown"]),
        "reversibility": payload.get("reversibility", "high"),
        "confidence": float(payload.get("confidence", 0.6)),
        "time_horizon": payload.get("time_horizon", "1-3 weeks"),
        "human_review_required": True,
        "uncertainty_notes": ["effect size depends on execution quality"],
        "advisory_only": True,
        "auto_apply": False,
    }


def causal_memory() -> dict:
    return {
        "analyses": ["reliability_drop_rca_2026w20"],
        "graph_snapshots": ["causal_graph_baseline_v1"],
        "intervention_estimates": ["data_integrity_repair_effect_estimate"],
        "resolved_incidents": ["replay debt stabilized"],
        "false_links": ["headline-noise falsely linked to calibration drift"],
    }
