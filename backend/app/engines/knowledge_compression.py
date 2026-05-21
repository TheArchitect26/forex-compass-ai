from __future__ import annotations

from app.engines.architectural_coherence import coherence_status
from app.engines.institutional_learning import learning_memory
from app.engines.institutional_wisdom import wisdom_status
from app.engines.memory_retrieval import memory_index
from app.engines.operator_control_plane import control_plane_status
from app.engines.operator_experience import ux_status
from app.engines.purpose_coherence import purpose_status
from app.engines.refactoring_intelligence import refactoring_status
from app.engines.release_governance import release_status
from app.engines.runtime_observability import observability_status
from app.engines.technical_debt_observatory import debt_status
from app.engines.existential_resilience import resilience_status


def _integration_snapshot() -> dict:
    return {
        "memory_retrieval": memory_index(),
        "control_plane": control_plane_status(),
        "operator_experience": ux_status(),
        "technical_debt": debt_status(),
        "release": release_status(),
        "runtime_observability": observability_status(),
        "purpose": purpose_status(),
        "wisdom": wisdom_status(),
        "architecture": coherence_status(),
        "resilience": resilience_status(),
        "institutional_learning": learning_memory(),
        "refactoring": refactoring_status(),
    }


def compression_status() -> dict:
    return {
        "compression_efficiency_score": 0.74,
        "insight_density_score": 0.71,
        "recall_usefulness_score": 0.73,
        "cognitive_reduction_score": 0.69,
        "repetition_reduction_score": 0.76,
        "strategic_retention_score": 0.72,
        "knowledge_durability_score": 0.7,
        "clutter_reduction_score": 0.75,
        "advisory_only": True,
        "auto_apply": False,
        "human_approval_required": True,
        "never_auto_delete_historical_records": True,
        "never_rewrite_institutional_history": True,
        "never_hide_critical_warnings": True,
        "never_collapse_nuance_into_false_certainty": True,
    }


def distill(payload: dict) -> dict:
    return {
        "durable_principles": payload.get("durable_principles", [
            "Prefer reversibility over cleverness.",
            "Consolidate before expanding.",
            "Protect operator cognition before adding features.",
        ]),
        "strategic_heuristics": payload.get("strategic_heuristics", [
            "Warnings lose value when overproduced.",
            "Institutional memory must remain searchable and compressible.",
            "Group insights by operator task, not subsystem novelty.",
        ]),
        "operational_lessons": payload.get("operational_lessons", ["route/env parity checks prevent recurring deployment confusion"]),
        "governance_doctrines": payload.get("governance_doctrines", ["human judgment remains final for release/rollback actions"]),
        "deployment_lessons": payload.get("deployment_lessons", ["phase-based rollout must include runtime regression checks"]),
        "architectural_patterns": payload.get("architectural_patterns", ["central summary console reduces multi-page triage cost"]),
        "recurring_anti_patterns": payload.get("recurring_anti_patterns", ["dashboard sprawl", "recommendation overload", "stale assumptions"]),
        "crisis_response_lessons": payload.get("crisis_response_lessons", ["preserve critical warnings while suppressing low-value noise"]),
        "trusted_institutional_practices": payload.get("trusted_institutional_practices", ["advisory-only defaults", "explicit human approval gates"]),
        "advisory_only": True,
        "auto_apply": False,
    }


def strategic_lessons(payload: dict) -> dict:
    return {
        "what_repeatedly_worked": payload.get("what_repeatedly_worked", ["summary-first operator views", "human-reviewed release checklists"]),
        "what_repeatedly_failed": payload.get("what_repeatedly_failed", ["fragmented route-by-route incident triage"]),
        "what_created_unnecessary_complexity": payload.get("what_created_unnecessary_complexity", ["duplicated cross-console summaries"]),
        "what_reduced_operator_burden": payload.get("what_reduced_operator_burden", ["control-plane consolidation", "focus views"]),
        "what_improved_survivability": payload.get("what_improved_survivability", ["rollback readiness and runtime checks"]),
        "what_improved_clarity": payload.get("what_improved_clarity", ["standardized score + warning framing"]),
        "what_caused_recurring_deployment_runtime_issues": payload.get("what_caused_recurring_deployment_runtime_issues", ["env mismatch", "route compatibility drift"]),
        "what_governance_patterns_proved_useful": payload.get("what_governance_patterns_proved_useful", ["advisory-only safety boundaries", "human-approval escalation"]),
        "clutter_reduction_opportunities": payload.get("clutter_reduction_opportunities", ["collapse low-frequency consoles into grouped categories"]),
        "advisory_only": True,
        "auto_apply": False,
    }


def anti_patterns(payload: dict) -> dict:
    return {
        "recurring_anti_patterns": payload.get("recurring_anti_patterns", [
            "dashboard sprawl",
            "governance inflation",
            "repeated dependency fragility",
            "architectural duplication",
            "recommendation overload",
            "alert fatigue",
            "symbolic complexity",
            "stale assumptions",
            "over-engineering",
            "operator confusion loops",
        ]),
        "advisory_only": True,
        "auto_apply": False,
        "human_approval_required": True,
    }


def heuristics(payload: dict) -> dict:
    return {
        "institutional_heuristics": payload.get("institutional_heuristics", [
            "Prefer reversibility over cleverness.",
            "Protect operator cognition before adding features.",
            "Consolidate before expanding.",
            "Warnings lose value when overproduced.",
            "Institutional memory must remain searchable and compressible.",
        ]),
        "advisory_only": True,
        "auto_apply": False,
    }


def compression_memory() -> dict:
    return {
        "distilled_insights": ["phase51_initial_distillation"],
        "strategic_heuristics": ["consolidate before expanding"],
        "anti_pattern_library": ["dashboard sprawl", "operator confusion loops"],
        "retention_checks": ["critical warning nuance preserved in compressed outputs"],
        "integration_snapshot": _integration_snapshot(),
        "safety_principles": [
            "never auto-delete historical records",
            "never rewrite institutional history",
            "never hide critical warnings",
            "never collapse nuanced information into false certainty",
            "human approval required for archival/compression actions",
        ],
    }
