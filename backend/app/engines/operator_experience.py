from __future__ import annotations

from app.engines.architectural_coherence import coherence_status
from app.engines.attention_architecture import detect_attention_fatigue
from app.engines.operator_control_plane import control_plane_status
from app.engines.purpose_coherence import purpose_status
from app.engines.refactoring_intelligence import refactoring_status
from app.engines.runtime_observability import observability_status
from app.engines.technical_debt_observatory import debt_status
from app.engines.trust_calibration import trust_status


def _integration_snapshot() -> dict:
    return {
        "control_plane": control_plane_status(),
        "attention": detect_attention_fatigue({"dashboard_fragmentation": 0.74, "context_switch_pressure": 0.7}),
        "technical_debt": debt_status(),
        "refactoring": refactoring_status(),
        "architecture": coherence_status(),
        "observability": observability_status(),
        "trust": trust_status(),
        "purpose": purpose_status(),
    }


def ux_status() -> dict:
    return {
        "operator_experience_score": 0.67,
        "usability_clarity_score": 0.64,
        "navigation_simplicity_score": 0.58,
        "readability_score": 0.62,
        "actionability_score": 0.7,
        "warning_fatigue_score": 0.44,
        "mobile_usability_score": 0.56,
        "interface_coherence_score": 0.61,
        "advisory_only": True,
        "auto_apply": False,
        "human_approval_required": True,
        "never_auto_delete_pages": True,
        "never_auto_change_navigation": True,
        "never_auto_hide_critical_warnings": True,
        "never_auto_rewrite_frontend": True,
    }


def usability_audit(payload: dict) -> dict:
    return {
        "visibility_of_system_status": payload.get("visibility_of_system_status", "mixed across consoles; strongest in control-plane pages"),
        "system_operator_language_match": payload.get("system_operator_language_match", "moderate; technical phrasing sometimes dominates"),
        "consistency_across_consoles": payload.get("consistency_across_consoles", "partial consistency with repeated but non-standard card structures"),
        "information_hierarchy_clarity": payload.get("information_hierarchy_clarity", "improving but crowded on dense console pages"),
        "error_warning_clarity": payload.get("error_warning_clarity", "warnings visible but often repeated with similar wording"),
        "recognition_over_memory": payload.get("recognition_over_memory", "operators still rely on memory across many route names"),
        "minimal_unnecessary_information": payload.get("minimal_unnecessary_information", "noisy in high-console workflows"),
        "human_control_and_freedom": payload.get("human_control_and_freedom", "strong; advisory-only boundaries preserved"),
        "help_documentation_clarity": payload.get("help_documentation_clarity", "available but lengthy; summary-first hints recommended"),
        "advisory_only": True,
        "auto_apply": False,
        "human_approval_required": True,
    }


def navigation_audit(payload: dict) -> dict:
    return {
        "too_many_sidebar_items": payload.get("too_many_sidebar_items", True),
        "duplicated_console_intent": payload.get("duplicated_console_intent", ["release vs observability status cards", "meta vs executive summaries"]),
        "unclear_grouping": payload.get("unclear_grouping", ["governance and strategy pages interleaved"]),
        "confusing_naming": payload.get("confusing_naming", ["adjacent terms (meta/metagovernance/mission) require interpretation"]),
        "buried_critical_pages": payload.get("buried_critical_pages", ["daily-critical pages can be lost in long sidebar"]),
        "excessive_context_switching": payload.get("excessive_context_switching", ["incident review often spans 5+ pages"]),
        "missing_daily_use_pathway": payload.get("missing_daily_use_pathway", ["daily route shortcut not explicit in global nav"]),
        "advisory_only": True,
        "auto_apply": False,
        "human_approval_required": True,
    }


def readability_review(payload: dict) -> dict:
    return {
        "dense_cards": payload.get("dense_cards", ["many cards aggregate several metrics and long inline text"]),
        "too_many_metrics_per_screen": payload.get("too_many_metrics_per_screen", ["multi-console pages show broad score sets without progressive disclosure"]),
        "unclear_score_meanings": payload.get("unclear_score_meanings", ["score interpretation hints are inconsistent"]),
        "weak_section_titles": payload.get("weak_section_titles", ["some headings describe domain but not operator decision intent"]),
        "repeated_safety_text": payload.get("repeated_safety_text", ["same advisory/no-execution copy repeated across many pages"]),
        "lack_summary_first_layout": payload.get("lack_summary_first_layout", ["high-value summary sometimes appears below dense sections"]),
        "small_screen_layout_risk": payload.get("small_screen_layout_risk", ["narrow screens can truncate high-density card content"]),
        "advisory_only": True,
        "auto_apply": False,
        "human_approval_required": True,
    }


def simplification_plan(payload: dict) -> dict:
    return {
        "recommendations": payload.get("recommendations", [
            "group sidebar items by domain and task frequency",
            "promote Control Plane as primary daily page",
            "collapse low-frequency consoles into categorized hubs",
            "standardize card structure (summary, meaning, next action)",
            "standardize score explanation helper text",
            "reduce repeated advisory copy with shared banner component",
            "create Daily View with top priorities and warnings",
            "create Maintenance View for debt/refactoring/ops",
            "create Crisis View for resilience/runtime/release warnings",
        ]),
        "daily_use_pathway": payload.get("daily_use_pathway", ["Open Control Plane", "Review top priorities", "Check critical warnings", "Confirm next human-reviewed action"]),
        "human_review_required": True,
        "advisory_only": True,
        "auto_apply": False,
    }


def ux_memory() -> dict:
    return {
        "ux_audits": ["phase49_operator_experience_baseline"],
        "usability_findings": ["navigation burden and dense layouts flagged"],
        "navigation_reviews": ["grouping recommendations drafted"],
        "readability_reviews": ["summary-first layout opportunity recorded"],
        "simplification_reviews": ["daily/maintenance/crisis views proposed"],
        "integration_snapshot": _integration_snapshot(),
        "safety_principles": [
            "never auto-delete pages",
            "never auto-change navigation",
            "never auto-hide critical warnings",
            "never auto-rewrite frontend",
            "human approval required for UX changes",
        ],
    }
