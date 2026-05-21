from __future__ import annotations

from app.engines.change_impact_analysis import change_control_status
from app.engines.feature_flag_governance import feature_flags_status
from app.engines.golden_path_workflows import golden_paths_status
from app.engines.institutional_evaluation import evaluation_status
from app.engines.knowledge_compression import compression_status
from app.engines.memory_retrieval import memory_status
from app.engines.operator_experience import ux_status
from app.engines.platform_catalog import platform_catalog_status
from app.engines.release_governance import release_status
from app.engines.runtime_observability import observability_status
from app.engines.scorecard_governance import scorecard_status
from app.engines.technical_debt_observatory import debt_status

PIR_TYPES = [
    "successful_change", "failed_change", "partial_success", "unexpected_impact", "rollback_required",
    "emergency_fix_review", "governance_gap_review", "release_regression_review", "operator_experience_review",
]


def _integration_snapshot() -> dict:
    return {
        "change_control": change_control_status(),
        "golden_paths": golden_paths_status(),
        "scorecards": scorecard_status(),
        "platform_catalog": platform_catalog_status(),
        "release": release_status(),
        "observability": observability_status(),
        "technical_debt": debt_status(),
        "feature_flags": feature_flags_status(),
        "memory": memory_status(),
        "compression": compression_status(),
        "evaluation": evaluation_status(),
        "ux": ux_status(),
    }


def post_implementation_status() -> dict:
    return {
        "pir_types": PIR_TYPES,
        "implementation_success_score": 0.73,
        "expected_vs_actual_alignment_score": 0.68,
        "incident_severity_score": 0.34,
        "rollback_effectiveness_score": 0.71,
        "operator_impact_score": 0.49,
        "lesson_value_score": 0.76,
        "process_improvement_priority_score": 0.72,
        "future_risk_reduction_score": 0.70,
        "advisory_only": True,
        "auto_apply": False,
        "human_approval_required": True,
        "never_rewrite_history": True,
        "never_auto_close_improvement_actions": True,
        "never_auto_change_scorecards": True,
        "never_auto_update_golden_paths": True,
        "never_auto_run_commands": True,
        "never_deploy": True,
        "never_rollback": True,
    }


def review(payload: dict) -> dict:
    return {
        "change_summary": payload.get("change_summary", "Completed change reviewed after production rollout"),
        "planned_outcome": payload.get("planned_outcome", "Improve governance visibility with minimal operator disruption"),
        "actual_outcome": payload.get("actual_outcome", "Visibility improved; minor onboarding friction detected"),
        "deviations": payload.get("deviations", ["additional review cycle needed", "runtime metric naming differed from plan"]),
        "what_worked": payload.get("what_worked", ["clear rollback notes", "tests caught integration mismatch"]),
        "what_failed": payload.get("what_failed", ["documentation update lagged deployment"]),
        "unexpected_impacts": payload.get("unexpected_impacts", ["temporary operator confusion in console labeling"]),
        "affected_systems": payload.get("affected_systems", ["api", "engine", "frontend", "docs"]),
        "incident_links_references": payload.get("incident_links_references", ["INC-2026-05-59-A"]),
        "rollback_status": payload.get("rollback_status", "not_required"),
        "operator_impact": payload.get("operator_impact", "low_to_moderate"),
        "lessons_learned": payload.get("lessons_learned", ["align docs and runtime labels before release"]),
        "recommended_improvements": payload.get("recommended_improvements", ["update checklist for docs/runtime naming parity"]),
        "human_review_required": True,
        "advisory_only": True,
        "auto_apply": False,
        "human_approval_required": True,
    }


def expected_vs_actual(payload: dict) -> dict:
    return {
        "predicted_vs_actual_affected_systems": payload.get("predicted_vs_actual_affected_systems", "mostly_aligned"),
        "expected_vs_actual_risk": payload.get("expected_vs_actual_risk", "actual_slightly_higher"),
        "expected_vs_actual_operator_impact": payload.get("expected_vs_actual_operator_impact", "actual_higher_for_onboarding"),
        "planned_vs_actual_validation": payload.get("planned_vs_actual_validation", "aligned_with_extra_regression"),
        "planned_vs_actual_rollback": payload.get("planned_vs_actual_rollback", "rollback_not_used_but_ready"),
        "expected_vs_actual_benefit": payload.get("expected_vs_actual_benefit", "benefit_realized_with_minor_delay"),
        "advisory_only": True,
        "auto_apply": False,
        "human_approval_required": True,
    }


def lessons_learned(payload: dict) -> dict:
    return {
        "golden_paths_lessons": payload.get("golden_paths_lessons", ["add explicit docs-runtime parity check"]),
        "scorecards_lessons": payload.get("scorecards_lessons", ["raise documentation readiness gate for operator-facing changes"]),
        "release_governance_lessons": payload.get("release_governance_lessons", ["add post-deploy verification for labels/alerts"]),
        "change_control_lessons": payload.get("change_control_lessons", ["tighten predicted operator impact criteria"]),
        "runtime_observability_lessons": payload.get("runtime_observability_lessons", ["add metric alias warnings"]),
        "feature_flags_lessons": payload.get("feature_flags_lessons", ["bind rollout docs to flag state transitions"]),
        "platform_catalog_lessons": payload.get("platform_catalog_lessons", ["mark docs ownership for every operator console"]),
        "ux_quality_lessons": payload.get("ux_quality_lessons", ["pre-release terminology review for new pages"]),
        "technical_debt_lessons": payload.get("technical_debt_lessons", ["remove duplicate labels introduced by rapid patch"]),
        "memory_retrieval_lessons": payload.get("memory_retrieval_lessons", ["store PIR summaries with searchable tags"]),
        "knowledge_compression_lessons": payload.get("knowledge_compression_lessons", ["compress repeated incident patterns into heuristics"]),
        "advisory_only": True,
        "auto_apply": False,
        "human_approval_required": True,
    }


def improvement_actions(payload: dict) -> dict:
    return {
        "actions": payload.get("actions", [
            "update golden path checklist",
            "adjust scorecard readiness gate",
            "improve change-control impact analysis",
            "strengthen release validation",
            "add missing test coverage",
            "document runtime issue",
            "add observability check",
            "update rollback playbook",
            "clarify owner/lifecycle",
            "compress repeated lesson into heuristic",
        ]),
        "priority_order": payload.get("priority_order", [
            "strengthen release validation",
            "add missing test coverage",
            "update golden path checklist",
            "improve change-control impact analysis",
            "add observability check",
        ]),
        "human_review_required": True,
        "advisory_only": True,
        "auto_apply": False,
        "human_approval_required": True,
    }


def post_implementation_memory() -> dict:
    return {
        "pir_snapshots": ["phase59_post_implementation_baseline"],
        "expected_vs_actual_reviews": ["predicted-vs-actual comparisons recorded"],
        "lesson_snapshots": ["cross-system lessons captured"],
        "improvement_action_snapshots": ["human-reviewed action backlog maintained"],
        "integration_snapshot": _integration_snapshot(),
        "safety_principles": [
            "never rewrite history",
            "never auto-close improvement actions",
            "never auto-change scorecards",
            "never auto-update golden paths",
            "never auto-run commands",
            "never deploy",
            "never rollback",
            "human approval required for improvement actions",
        ],
    }
