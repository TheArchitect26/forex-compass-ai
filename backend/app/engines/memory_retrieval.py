from __future__ import annotations

from app.engines.architectural_coherence import architecture_memory
from app.engines.institutional_learning import learning_memory
from app.engines.meta_governance import metagovernance_memory
from app.engines.operator_control_plane import control_plane_memory
from app.engines.operational_orchestration import operations_memory
from app.engines.purpose_coherence import purpose_memory
from app.engines.refactoring_intelligence import refactoring_memory
from app.engines.release_governance import release_memory
from app.engines.runtime_observability import observability_memory
from app.engines.technical_debt_observatory import debt_memory
from app.engines.trust_calibration import trust_memory
from app.engines.existential_resilience import resilience_memory

INDEX_CATEGORIES = [
    "phase_history",
    "decisions",
    "lessons",
    "warnings",
    "assumptions",
    "incidents",
    "migrations",
    "recommendations",
    "governance_rationale",
    "operator_context",
    "unresolved_issues",
]


def _integration_snapshot() -> dict:
    return {
        "control_plane": control_plane_memory(),
        "institutional_learning": learning_memory(),
        "technical_debt": debt_memory(),
        "release": release_memory(),
        "runtime_observability": observability_memory(),
        "architecture": architecture_memory(),
        "refactoring": refactoring_memory(),
        "meta_governance": metagovernance_memory(),
        "purpose": purpose_memory(),
        "trust": trust_memory(),
        "operations": operations_memory(),
        "resilience": resilience_memory(),
    }


def memory_status() -> dict:
    return {
        "retrieval_health": "ready",
        "indexed_categories": INDEX_CATEGORIES,
        "memory_coverage_score": 0.73,
        "retrieval_accuracy_estimate": 0.69,
        "staleness_exposure_score": 0.38,
        "advisory_only": True,
        "auto_apply": False,
        "human_approval_required": True,
        "never_auto_delete_memory": True,
        "never_auto_rewrite_history": True,
        "never_auto_resolve_assumptions": True,
        "never_hide_critical_historical_warnings": True,
    }


def _scoring(payload: dict) -> dict:
    return {
        "relevance_score": float(payload.get("relevance_score", 0.78)),
        "recency_score": float(payload.get("recency_score", 0.61)),
        "strategic_importance_score": float(payload.get("strategic_importance_score", 0.74)),
        "confidence_score": float(payload.get("confidence_score", 0.67)),
        "source_clarity_score": float(payload.get("source_clarity_score", 0.71)),
        "usefulness_score": float(payload.get("usefulness_score", 0.72)),
        "actionability_score": float(payload.get("actionability_score", 0.69)),
        "staleness_risk_score": float(payload.get("staleness_risk_score", 0.36)),
    }


def memory_search(payload: dict) -> dict:
    return {
        "query": payload.get("query", "latest release/runtime lessons"),
        "matches": payload.get("matches", [
            {"title": "Phase 47 runtime observability baseline", "category": "lessons", "source": "runtime_observability", "snippet": "Route mismatch and env parity are recurring risks."},
            {"title": "Phase 46 release governance checklist", "category": "decisions", "source": "release_governance", "snippet": "Require explicit rollback planning and human review."},
        ]),
        "retrieval_scoring": _scoring(payload),
        "advisory_only": True,
        "auto_apply": False,
        "human_approval_required": True,
    }


def contextual_recall(payload: dict) -> dict:
    return {
        "context": payload.get("context", "operator triaging release/runtime instability"),
        "most_relevant_prior_lessons": payload.get("most_relevant_prior_lessons", ["env parity checks prevent post-release confusion", "route compatibility drift requires early detection"]),
        "related_decisions": payload.get("related_decisions", ["prioritize release/runtime view for incidents", "defer low-value console changes during stabilization"]),
        "related_incidents": payload.get("related_incidents", ["phase47 route mismatch warning cluster"]),
        "related_assumptions": payload.get("related_assumptions", ["all deploy targets expose identical API prefixes"]),
        "related_warnings": payload.get("related_warnings", ["repeated 404 bursts after phased rollout"]),
        "related_phases": payload.get("related_phases", ["phase46", "phase47", "phase48", "phase49"]),
        "stale_or_outdated_knowledge_risks": payload.get("stale_or_outdated_knowledge_risks", ["older migration notes may not reflect latest phase ordering"]),
        "recommended_human_review": payload.get("recommended_human_review", "validate assumptions and confirm current deployment topology before action"),
        "retrieval_scoring": _scoring(payload),
        "advisory_only": True,
        "auto_apply": False,
    }


def related_items(payload: dict) -> dict:
    return {
        "item": payload.get("item", "phase47_runtime_observability_baseline"),
        "related_phase_history": payload.get("related_phase_history", ["phase46_release_governance_baseline", "phase48_unified_control_plane_baseline"]),
        "related_recommendations": payload.get("related_recommendations", ["group runtime + release summaries", "tighten env parity checklist"]),
        "related_governance_rationale": payload.get("related_governance_rationale", ["human approval precedes deployment/rollback choices"]),
        "related_unresolved_issues": payload.get("related_unresolved_issues", ["stale assumptions about route parity"]),
        "retrieval_scoring": _scoring(payload),
        "advisory_only": True,
        "auto_apply": False,
    }


def staleness_review(payload: dict) -> dict:
    return {
        "old_assumptions_no_longer_reliable": payload.get("old_assumptions_no_longer_reliable", ["single deployment profile assumption"]),
        "outdated_recommendations": payload.get("outdated_recommendations", ["legacy console-first workflow before control-plane rollout"]),
        "superseded_phase_decisions": payload.get("superseded_phase_decisions", ["older navigation priority before phase48 consolidation guidance"]),
        "stale_migration_notes": payload.get("stale_migration_notes", ["older phase ordering comments lacking phase50 context"]),
        "old_warnings_no_longer_material": payload.get("old_warnings_no_longer_material", ["resolved temporary provider warning"]),
        "old_lessons_needing_revalidation": payload.get("old_lessons_needing_revalidation", ["pre-control-plane cognitive load assumptions"]),
        "recommended_human_review": payload.get("recommended_human_review", "review stale entries and annotate validity windows"),
        "advisory_only": True,
        "auto_apply": False,
        "human_approval_required": True,
    }


def memory_index() -> dict:
    return {
        "categories": INDEX_CATEGORIES,
        "example_entries": [
            {"id": "phase47_runtime_observability_baseline", "category": "phase_history", "tags": ["runtime", "regression", "warnings"]},
            {"id": "phase48_unified_control_plane_baseline", "category": "decisions", "tags": ["consolidation", "operator_clarity"]},
            {"id": "phase49_operator_experience_baseline", "category": "lessons", "tags": ["ux", "navigation", "readability"]},
        ],
        "advisory_only": True,
        "auto_apply": False,
    }
