from __future__ import annotations

from app.engines.change_impact_analysis import change_control_status
from app.engines.controlled_evolution import evolution_control_status
from app.engines.feature_flag_governance import feature_flags_status
from app.engines.golden_path_workflows import golden_paths_status
from app.engines.institutional_evaluation import evaluation_status
from app.engines.meta_governance import metagovernance_status
from app.engines.platform_catalog import platform_catalog_status
from app.engines.post_implementation_review import post_implementation_status
from app.engines.purpose_coherence import purpose_status
from app.engines.release_governance import release_status
from app.engines.runtime_observability import observability_status
from app.engines.scorecard_governance import scorecard_status
from app.engines.existential_resilience import resilience_status

POLICY_CATEGORIES = [
    "constitutional_policy", "governance_policy", "operational_policy", "release_policy", "observability_policy",
    "change_control_policy", "safety_policy", "review_policy", "memory_retention_policy", "anti_automation_policy",
    "resilience_policy", "human_sovereignty_policy",
]


def _integration_snapshot() -> dict:
    return {
        "post_implementation": post_implementation_status(),
        "change_control": change_control_status(),
        "golden_paths": golden_paths_status(),
        "scorecards": scorecard_status(),
        "platform_catalog": platform_catalog_status(),
        "release": release_status(),
        "observability": observability_status(),
        "feature_flags": feature_flags_status(),
        "controlled_evolution": evolution_control_status(),
        "evaluation": evaluation_status(),
        "resilience": resilience_status(),
        "purpose": purpose_status(),
        "meta_governance": metagovernance_status(),
    }


def policy_status() -> dict:
    return {
        "policy_categories": POLICY_CATEGORIES,
        "constitutional_rules": [
            "advisory_only=true by default",
            "auto_apply=false by default",
            "human approval required for operational changes",
            "no autonomous deployment",
            "no autonomous rollback",
            "no autonomous governance mutation",
            "no hidden operator-impacting behavior",
            "rollback/recovery planning required",
            "observability required for operational systems",
            "migrations required for persistence changes",
            "tests required for operational capabilities",
            "README updates required for governance-impacting changes",
        ],
        "policy_coverage_score": 0.79,
        "enforcement_clarity_score": 0.76,
        "doctrine_consistency_score": 0.78,
        "institutional_protection_score": 0.82,
        "review_discipline_score": 0.77,
        "operational_resilience_score": 0.75,
        "constitutional_alignment_score": 0.81,
        "governance_completeness_score": 0.78,
        "advisory_only": True,
        "auto_apply": False,
        "human_approval_required": True,
        "never_auto_enforce_destructive_actions": True,
        "never_auto_delete_capabilities": True,
        "never_auto_change_governance_states": True,
        "never_auto_approve_compliance": True,
        "never_auto_rewrite_doctrine": True,
    }


def policies_list(payload: dict) -> dict:
    return {
        "policies": payload.get("policies", [
            {"name": "constitutional_core", "category": "constitutional_policy", "owner": "governance", "non_negotiable": True},
            {"name": "anti_automation_guardrails", "category": "anti_automation_policy", "owner": "governance", "non_negotiable": True},
        ]),
        "advisory_only": True, "auto_apply": False, "human_approval_required": True,
    }


def evaluate_compliance(payload: dict) -> dict:
    return {
        "violates_institutional_doctrine": payload.get("violates_institutional_doctrine", False),
        "bypasses_safeguards": payload.get("bypasses_safeguards", False),
        "lacks_review_requirements": payload.get("lacks_review_requirements", False),
        "weakens_observability": payload.get("weakens_observability", False),
        "weakens_rollback_readiness": payload.get("weakens_rollback_readiness", False),
        "weakens_operator_sovereignty": payload.get("weakens_operator_sovereignty", False),
        "weakens_documentation_discipline": payload.get("weakens_documentation_discipline", False),
        "introduces_governance_contradiction": payload.get("introduces_governance_contradiction", False),
        "advisory_only": True, "auto_apply": False, "human_approval_required": True,
    }


def conflict_review(payload: dict) -> dict:
    return {
        "conflict_summary": payload.get("conflict_summary", "Potential mismatch between workflow checklist and scorecard gate strictness"),
        "affected_systems": payload.get("affected_systems", ["golden_paths", "scorecards", "release_governance"]),
        "doctrine_violated": payload.get("doctrine_violated", ["review obligation consistency"]),
        "risk_severity": payload.get("risk_severity", "moderate"),
        "human_review_required": True,
        "recommended_resolution_path": payload.get("recommended_resolution_path", ["align checklist gate with scorecard policy", "add explicit doctrine note in README"]),
        "advisory_only": True, "auto_apply": False, "human_approval_required": True,
    }


def doctrine_summary(payload: dict) -> dict:
    return {
        "institutional_operating_principles": payload.get("institutional_operating_principles", ["human-reviewed governance", "safety-first operational discipline"]),
        "governance_philosophy": payload.get("governance_philosophy", ["stable constitutional constraints over phase-level variance"]),
        "review_obligations": payload.get("review_obligations", ["release, architecture, and rollback reviews where applicable"]),
        "operational_safety_principles": payload.get("operational_safety_principles", ["no hidden operator-impacting behavior", "explicit rollback planning"]),
        "anti_automation_protections": payload.get("anti_automation_protections", ["no autonomous deploy/rollback/governance mutation"]),
        "long_term_continuity_doctrine": payload.get("long_term_continuity_doctrine", ["institutional rules outlive individual phases"]),
        "human_sovereignty_guarantees": payload.get("human_sovereignty_guarantees", ["human approval required for doctrine and operational changes"]),
        "advisory_only": True, "auto_apply": False, "human_approval_required": True,
    }


def policy_memory() -> dict:
    return {
        "policy_snapshots": ["phase60_institutional_policy_baseline"],
        "compliance_reviews": ["doctrine compliance checks recorded"],
        "conflict_reviews": ["policy/workflow/scorecard conflicts tracked"],
        "doctrine_summaries": ["constitutional doctrine summaries retained"],
        "integration_snapshot": _integration_snapshot(),
        "safety_principles": [
            "never auto-enforce destructive actions",
            "never auto-delete capabilities",
            "never auto-change governance states",
            "never auto-approve compliance",
            "never auto-rewrite doctrine",
            "human approval required for doctrine changes",
        ],
    }
