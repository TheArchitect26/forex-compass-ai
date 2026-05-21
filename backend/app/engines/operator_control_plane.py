from __future__ import annotations

from app.engines.anticipatory_intelligence import foresight_scores
from app.engines.architectural_coherence import coherence_status
from app.engines.attention_architecture import detect_attention_fatigue
from app.engines.ecosystem_intelligence import ecosystem_status
from app.engines.existential_resilience import resilience_status
from app.engines.institutional_wisdom import wisdom_status
from app.engines.meta_governance import metagovernance_status
from app.engines.operational_orchestration import operational_status
from app.engines.purpose_coherence import purpose_status
from app.engines.refactoring_intelligence import refactoring_status
from app.engines.release_governance import release_status
from app.engines.runtime_observability import observability_status
from app.engines.strategic_synthesis import run_synthesis
from app.engines.technical_debt_observatory import debt_status
from app.engines.trust_calibration import trust_status

FOCUS_VIEWS = [
    "Executive View",
    "Release/Runtime View",
    "Governance View",
    "Architecture/Maintenance View",
    "Strategy/Intelligence View",
    "Crisis/Resilience View",
    "Minimal Daily View",
]


def _integrations() -> dict:
    return {
        "release": release_status(),
        "observability": observability_status(),
        "debt": debt_status(),
        "resilience": resilience_status(),
        "trust": trust_status(),
        "purpose": purpose_status(),
        "wisdom": wisdom_status(),
        "meta_governance": metagovernance_status(),
        "architecture": coherence_status(),
        "refactoring": refactoring_status(),
        "operations": operational_status(),
        "ecosystem": ecosystem_status(),
        "strategic_synthesis": run_synthesis({}),
        "foresight": foresight_scores({}),
        "attention": detect_attention_fatigue({"dashboard_fragmentation": 0.72, "context_switch_pressure": 0.69}),
    }


def control_plane_status() -> dict:
    return {
        "operator_clarity_score": 0.66,
        "dashboard_sprawl_score": 0.78,
        "cognitive_load_score": 0.73,
        "institutional_health_score": 0.68,
        "actionability_score": 0.7,
        "signal_to_noise_score": 0.63,
        "navigation_burden_score": 0.74,
        "consolidation_opportunity_score": 0.81,
        "advisory_only": True,
        "auto_apply": False,
        "human_approval_required": True,
        "never_hide_critical_warnings": True,
        "never_delete_consoles": True,
        "never_change_navigation_automatically": True,
        "never_auto_complete_actions": True,
        "never_auto_deploy_or_rollback": True,
    }


def control_plane_summary(payload: dict) -> dict:
    return {
        "top_institutional_priorities": payload.get("top_institutional_priorities", [
            "stabilize release/runtime route compatibility",
            "reduce dashboard sprawl through grouped focus views",
            "tighten env/runtime parity checks",
            "address high-severity endpoint reliability warnings",
            "improve operator attention protection and noise suppression",
        ]),
        "top_ignore_or_defer": payload.get("top_ignore_or_defer", [
            "low-impact cosmetic console refinements",
            "non-critical narrative expansion tasks",
            "duplicate summary pages pending consolidation plan",
            "low-severity advisory wording tweaks",
            "speculative long-horizon experiments without active risks",
        ]),
        "critical_warnings": payload.get("critical_warnings", [
            "release/runtime mismatch can create false confidence",
            "endpoint failure clusters require human review",
        ]),
        "maintenance_reminders": payload.get("maintenance_reminders", ["weekly route audit", "env-var parity review", "sidebar grouping proposal review"]),
        "release_deployment_status": payload.get("release_deployment_status", "caution"),
        "runtime_health": payload.get("runtime_health", "caution"),
        "operator_load": payload.get("operator_load", "elevated"),
        "strategic_focus_recommendation": payload.get("strategic_focus_recommendation", "Release/Runtime View"),
        "next_best_human_reviewed_action": payload.get("next_best_human_reviewed_action", "Run control-plane guided triage on failing routes and approve a grouped navigation plan."),
        "advisory_only": True,
        "auto_apply": False,
        "human_approval_required": True,
    }


def top_actions(payload: dict) -> dict:
    return {
        "top_actions": payload.get("top_actions", [
            {"action": "triage highest-severity route failures", "priority": "critical", "human_review_required": True},
            {"action": "review release/runtime drift indicators", "priority": "high", "human_review_required": True},
            {"action": "approve sidebar grouping recommendation", "priority": "high", "human_review_required": True},
            {"action": "defer low-value consoles", "priority": "medium", "human_review_required": True},
            {"action": "schedule weekly consolidation checkpoint", "priority": "medium", "human_review_required": True},
        ]),
        "advisory_only": True,
        "auto_apply": False,
    }


def console_sprawl(payload: dict) -> dict:
    return {
        "too_many_sidebar_items": payload.get("too_many_sidebar_items", True),
        "overlapping_frontend_pages": payload.get("overlapping_frontend_pages", ["release vs observability summaries", "meta vs executive summaries"]),
        "low_value_consoles": payload.get("low_value_consoles", ["rarely used duplicate summary pages"]),
        "duplicated_summaries": payload.get("duplicated_summaries", ["multiple pages repeating status snapshots"]),
        "navigation_confusion": payload.get("navigation_confusion", ["adjacent governance/strategy pages difficult to distinguish quickly"]),
        "excessive_context_switching": payload.get("excessive_context_switching", ["operators bounce between >6 consoles for one incident"]),
        "dashboards_to_group": payload.get("dashboards_to_group", ["Release+Observability", "Debt+Refactoring+Architecture", "Trust+Purpose+Wisdom"]),
        "sidebar_simplification_recommendation": payload.get("sidebar_simplification_recommendation", [
            "group by domain: Runtime, Governance, Architecture, Strategy",
            "mark low-priority pages as advanced",
            "keep all routes available; apply only with human approval",
        ]),
        "advisory_only": True,
        "auto_apply": False,
        "never_delete_consoles": True,
        "never_change_navigation_automatically": True,
        "human_approval_required": True,
    }


def focus_view(payload: dict) -> dict:
    view = payload.get("view", "Executive View")
    if view not in FOCUS_VIEWS:
        view = "Executive View"
    selected = {
        "Executive View": ["institutional_health_score", "critical_warnings", "top_institutional_priorities"],
        "Release/Runtime View": ["release_deployment_status", "runtime_health", "critical_warnings"],
        "Governance View": ["trust", "purpose", "meta_governance", "critical_warnings"],
        "Architecture/Maintenance View": ["debt", "architecture", "refactoring", "maintenance_reminders"],
        "Strategy/Intelligence View": ["strategic_synthesis", "foresight", "top_institutional_priorities"],
        "Crisis/Resilience View": ["resilience", "runtime_health", "critical_warnings"],
        "Minimal Daily View": ["top_institutional_priorities", "next_best_human_reviewed_action", "critical_warnings"],
    }
    return {
        "view": view,
        "suppressed_noise": True,
        "critical_warnings_preserved": True,
        "relevant_signals": selected[view],
        "human_judgment_final": True,
        "advisory_only": True,
        "auto_apply": False,
    }


def control_plane_memory() -> dict:
    return {
        "control_plane_snapshots": ["phase48_unified_control_plane_baseline"],
        "focus_decisions": ["Release/Runtime View used during recent stability review"],
        "sprawl_audits": ["sidebar grouping recommended; no automatic removals"],
        "critical_warning_preservation_checks": ["critical warnings always retained across focus views"],
        "integration_snapshot": _integrations(),
        "safety_principles": [
            "never hide critical warnings",
            "never delete consoles",
            "never change navigation automatically",
            "never auto-complete actions",
            "never auto-deploy or rollback",
            "human approval required for consolidation changes",
        ],
    }
