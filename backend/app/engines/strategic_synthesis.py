from __future__ import annotations


def _top_three(items: list[dict], key: str = "score") -> list[dict]:
    return sorted(items, key=lambda x: float(x.get(key, 0)), reverse=True)[:3]


def detect_cross_layer_conflicts(payload: dict) -> list[str]:
    conflicts = []
    if payload.get("attention_urgent") and payload.get("wisdom_wait"):
        conflicts.append("attention says urgent, wisdom says wait")
    if payload.get("temporal_defer") and payload.get("governance_critical"):
        conflicts.append("temporal says defer, governance says critical")
    if payload.get("mission_simplify") and payload.get("research_expand"):
        conflicts.append("mission says simplify, research says expand")
    if payload.get("reality_low_usefulness") and payload.get("meta_high_complexity"):
        conflicts.append("reality says low usefulness, meta says high complexity")
    if payload.get("operator_reduce") and payload.get("system_investigate"):
        conflicts.append("operator load says reduce, system pressure says investigate")
    return conflicts


def condensed_brief(payload: dict) -> dict:
    priorities = _top_three(payload.get("priorities", []))
    ignore_now = _top_three(payload.get("noise", []), key="noise_score")
    risks = _top_three(payload.get("risks", []))
    return {
        "top_priorities": priorities,
        "ignore_for_now": ignore_now,
        "risks_to_monitor": risks,
        "recommended_focus_mode": payload.get("recommended_focus_mode", "executive_overview"),
        "recommended_next_review_window": payload.get("recommended_next_review_window", "within 24 hours"),
    }


def run_synthesis(payload: dict) -> dict:
    conflicts = detect_cross_layer_conflicts(payload)
    brief = condensed_brief(payload)
    return {
        "top_strategic_priorities": brief["top_priorities"],
        "suppressed_noise": brief["ignore_for_now"],
        "conflicting_layer_signals": conflicts,
        "recommended_focus": brief["recommended_focus_mode"],
        "timing_guidance": brief["recommended_next_review_window"],
        "operator_safe_next_actions": payload.get("operator_safe_next_actions", ["review top priority", "confirm with human judgment", "defer low-value work"]),
        "facts": payload.get("facts", []),
        "estimates": payload.get("estimates", []),
        "recommendations": payload.get("recommendations", []),
        "advisory_only": True,
        "human_judgment_final": True,
        "auto_apply": False,
    }


def synthesis_memory() -> dict:
    return {
        "recent_snapshots": ["focus-shift-to-risk-control"],
        "recent_conflicts": ["attention-vs-wisdom urgency disagreement"],
        "focus_decisions": ["executive_overview for next cycle"],
        "preserved_safety_warnings": ["never execute trades automatically"],
    }
