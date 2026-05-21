from __future__ import annotations

from app.engines.architectural_coherence import coherence_status
from app.engines.institutional_evaluation import evaluation_status
from app.engines.knowledge_compression import compression_status
from app.engines.memory_retrieval import memory_status
from app.engines.operator_control_plane import control_plane_status
from app.engines.operator_experience import ux_status
from app.engines.purpose_coherence import purpose_status
from app.engines.refactoring_intelligence import refactoring_status
from app.engines.release_governance import release_status
from app.engines.runtime_observability import observability_status
from app.engines.technical_debt_observatory import debt_status
from app.engines.trust_calibration import trust_status

LIFECYCLE_STATES = [
    "experimental", "active", "stable", "frozen", "deprecated", "retired_candidate", "consolidation_candidate", "needs_review",
]


def _integration_snapshot() -> dict:
    return {
        "evaluation": evaluation_status(), "compression": compression_status(), "memory": memory_status(), "ux": ux_status(),
        "control_plane": control_plane_status(), "debt": debt_status(), "refactoring": refactoring_status(), "architecture": coherence_status(),
        "purpose": purpose_status(), "trust": trust_status(), "release": release_status(), "observability": observability_status(),
    }


def evolution_control_status() -> dict:
    return {
        "lifecycle_states": LIFECYCLE_STATES,
        "capability_maturity_score": 0.69,
        "operator_value_score": 0.71,
        "evidence_strength_score": 0.67,
        "maintenance_burden_score": 0.58,
        "retirement_readiness_score": 0.55,
        "consolidation_readiness_score": 0.74,
        "freeze_suitability_score": 0.66,
        "evolution_priority_score": 0.72,
        "advisory_only": True,
        "auto_apply": False,
        "human_approval_required": True,
        "never_auto_delete_features": True,
        "never_auto_remove_routes": True,
        "never_auto_freeze_capabilities": True,
        "never_auto_retire_consoles": True,
        "never_auto_change_navigation": True,
    }


def capability_audit(payload: dict) -> dict:
    capabilities = payload.get("capabilities", [
        {"capability": "frontend_consoles", "lifecycle_state": "consolidation_candidate", "value_evidence": "high operator visibility but high sprawl", "maintenance_burden": "high", "overlap_risk": "high", "maturity_level": "active", "recommendation": "group under control-plane domains", "human_approval_required": True},
        {"capability": "release_observability_stack", "lifecycle_state": "stable", "value_evidence": "improved runtime/release visibility", "maintenance_burden": "medium", "overlap_risk": "medium", "maturity_level": "stable", "recommendation": "freeze core interfaces and refine incrementally", "human_approval_required": True},
    ])
    return {"capability_audit": capabilities, "advisory_only": True, "auto_apply": False}


def lifecycle_review(payload: dict) -> dict:
    return {
        "candidate_graduations": payload.get("candidate_graduations", ["release_governance", "runtime_observability"]),
        "candidate_freezes": payload.get("candidate_freezes", ["core control-plane score schema", "release checklist contract"]),
        "candidate_deprecations": payload.get("candidate_deprecations", ["duplicate summary-only consoles"]),
        "candidate_consolidations": payload.get("candidate_consolidations", ["memory + compression insight surfaces", "debt + refactoring + architecture summaries"]),
        "needs_review": payload.get("needs_review", ["long-tail experimental advisory pages"]),
        "advisory_only": True,
        "auto_apply": False,
        "human_approval_required": True,
    }


def retirement_candidates(payload: dict) -> dict:
    return {
        "unused_or_low_value_consoles": payload.get("unused_or_low_value_consoles", ["niche duplicate summary views"]),
        "duplicated_advisory_systems": payload.get("duplicated_advisory_systems", ["overlapping status pages with similar metrics"]),
        "old_experimental_routes": payload.get("old_experimental_routes", ["legacy experimental compare routes"]),
        "repeated_summaries": payload.get("repeated_summaries", ["same risk summary repeated across many consoles"]),
        "burden_without_clarity": payload.get("burden_without_clarity", ["high-maintenance pages with low decision value"]),
        "better_grouped_under_control_plane": payload.get("better_grouped_under_control_plane", ["release + observability + evaluation daily checks"]),
        "engines_better_merged_or_frozen": payload.get("engines_better_merged_or_frozen", ["adjacent advisory synthesis helpers"]),
        "advisory_only": True,
        "auto_apply": False,
        "human_approval_required": True,
    }


def evolution_plan(payload: dict) -> dict:
    return {
        "what_to_evolve_next": payload.get("what_to_evolve_next", ["daily control-plane pathways", "evidence-linked benchmark quality"]),
        "what_to_freeze": payload.get("what_to_freeze", ["stable release/runtime safety contracts"]),
        "what_to_consolidate": payload.get("what_to_consolidate", ["duplicated summaries and low-frequency consoles"]),
        "what_to_monitor": payload.get("what_to_monitor", ["navigation burden", "warning fatigue", "memory staleness"]),
        "what_to_retire_later": payload.get("what_to_retire_later", ["legacy experimental routes with low usage"]),
        "what_not_to_touch": payload.get("what_not_to_touch", ["core advisory safety guarantees"]),
        "risk_notes": payload.get("risk_notes", ["over-consolidation can hide nuance if not reviewed carefully"]),
        "reversibility_notes": payload.get("reversibility_notes", ["prefer feature-flagged deprecation and phased rollbacks"]),
        "advisory_only": True,
        "auto_apply": False,
        "human_approval_required": True,
    }


def evolution_control_memory() -> dict:
    return {
        "lifecycle_snapshots": ["phase53_controlled_evolution_baseline"],
        "retirement_watchlist": ["duplicate summary consoles"],
        "freeze_decisions": ["core release/runtime contracts flagged for freeze review"],
        "consolidation_reviews": ["control-plane centered grouping proposal logged"],
        "integration_snapshot": _integration_snapshot(),
        "safety_principles": [
            "never auto-delete features", "never auto-remove routes", "never auto-freeze capabilities",
            "never auto-retire consoles", "never auto-change navigation", "human approval required for lifecycle changes",
        ],
    }
