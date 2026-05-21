from __future__ import annotations

from app.engines.architectural_coherence import coherence_status
from app.engines.knowledge_compression import compression_status
from app.engines.memory_retrieval import memory_status
from app.engines.meta_governance import metagovernance_status
from app.engines.operator_control_plane import control_plane_status
from app.engines.operator_experience import ux_status
from app.engines.operational_orchestration import operational_status
from app.engines.purpose_coherence import purpose_status
from app.engines.refactoring_intelligence import refactoring_status
from app.engines.release_governance import release_status
from app.engines.runtime_observability import observability_status
from app.engines.technical_debt_observatory import debt_status
from app.engines.trust_calibration import trust_status
from app.engines.existential_resilience import resilience_status

BENCHMARK_CATEGORIES = [
    "daily_usability", "release_safety", "runtime_reliability", "memory_recall", "dashboard_clarity",
    "governance_coherence", "debt_control", "operator_cognitive_load", "strategic_actionability", "resilience_readiness",
]


def _integration_snapshot() -> dict:
    return {
        "control_plane": control_plane_status(), "ux": ux_status(), "memory": memory_status(), "compression": compression_status(),
        "release": release_status(), "observability": observability_status(), "debt": debt_status(), "architecture": coherence_status(),
        "refactoring": refactoring_status(), "meta_governance": metagovernance_status(), "trust": trust_status(), "purpose": purpose_status(),
        "operations": operational_status(), "resilience": resilience_status(),
    }


def evaluation_status() -> dict:
    return {
        "institutional_maturity_score": 0.71,
        "usability_maturity_score": 0.66,
        "release_maturity_score": 0.69,
        "runtime_maturity_score": 0.68,
        "governance_maturity_score": 0.72,
        "memory_maturity_score": 0.67,
        "strategic_usefulness_score": 0.7,
        "maintainability_maturity_score": 0.63,
        "operator_clarity_score": 0.65,
        "advisory_only": True,
        "auto_apply": False,
        "human_review_required": True,
        "never_auto_change_scores_without_evidence": True,
        "never_auto_approve_maturity_claims": True,
        "never_auto_rewrite_strategy": True,
        "never_hide_regressions": True,
    }


def maturity_assessment(payload: dict) -> dict:
    return {
        "scores": payload.get("scores", evaluation_status()),
        "evidence_summary": payload.get("evidence_summary", ["phase tests passing", "advisory safeguards preserved", "consolidation layers added"]),
        "maturity_confidence": payload.get("maturity_confidence", "moderate"),
        "human_review_required": True,
        "advisory_only": True,
        "auto_apply": False,
    }


def benchmark(payload: dict) -> dict:
    categories = []
    for c in BENCHMARK_CATEGORIES:
        categories.append({
            "category": c,
            "current_score": float(payload.get(f"{c}_current", 0.65)),
            "target_score": float(payload.get(f"{c}_target", 0.8)),
            "evidence": payload.get(f"{c}_evidence", ["operator telemetry + engine audits"]),
            "trend": payload.get(f"{c}_trend", "improving"),
            "maturity_level": payload.get(f"{c}_maturity_level", "developing"),
            "recommended_improvement": payload.get(f"{c}_recommended_improvement", "tighten feedback loops and reduce sprawl"),
            "human_review_required": True,
        })
    return {"benchmarks": categories, "advisory_only": True, "auto_apply": False}


def improvement_plan(payload: dict) -> dict:
    return {
        "plan_items": payload.get("plan_items", [
            "consolidate pages", "improve daily control plane", "strengthen tests", "reduce sidebar overload",
            "improve release validation", "clean old assumptions", "improve memory relevance", "reduce repeated safety copy",
            "split oversized files", "improve API consistency",
        ]),
        "priority_order": payload.get("priority_order", ["release/runtime clarity", "operator burden", "maintainability", "memory quality"]),
        "human_review_required": True,
        "advisory_only": True,
        "auto_apply": False,
    }


def regression_review(payload: dict) -> dict:
    return {
        "more_navigation_burden": payload.get("more_navigation_burden", True),
        "more_duplicated_logic": payload.get("more_duplicated_logic", True),
        "weaker_release_safety": payload.get("weaker_release_safety", False),
        "weaker_runtime_clarity": payload.get("weaker_runtime_clarity", False),
        "weaker_operator_experience": payload.get("weaker_operator_experience", True),
        "more_governance_contradiction": payload.get("more_governance_contradiction", True),
        "more_memory_clutter": payload.get("more_memory_clutter", True),
        "more_technical_debt": payload.get("more_technical_debt", True),
        "regression_warnings": payload.get("regression_warnings", ["sidebar growth increased cognitive switching pressure"]),
        "evidence_required": True,
        "advisory_only": True,
        "auto_apply": False,
        "human_review_required": True,
    }


def evaluation_memory() -> dict:
    return {
        "evaluation_snapshots": ["phase52_baseline_maturity_assessment"],
        "benchmark_history": ["initial benchmark matrix recorded"],
        "regression_reviews": ["navigation burden flagged"],
        "improvement_plan_history": ["human-reviewed plan drafted"],
        "integration_snapshot": _integration_snapshot(),
        "safety_principles": [
            "never auto-change scores without evidence", "never auto-approve maturity claims", "never auto-rewrite strategy",
            "never hide regressions", "human review required for improvement plans",
        ],
    }
