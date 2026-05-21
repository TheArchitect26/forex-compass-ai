from __future__ import annotations


def match_filters(item: dict, filters: dict) -> bool:
    sev = filters.get("severity")
    regime = filters.get("regime")
    profile = filters.get("profile")
    if sev and item.get("severity") != sev:
        return False
    if regime and regime not in (item.get("regimes") or []):
        return False
    if profile and profile not in (item.get("profiles") or []):
        return False
    return True


def index_search(items: list[dict], q: str = "", filters: dict | None = None) -> list[dict]:
    filters = filters or {}
    qn = q.lower().strip()
    out = []
    for i in items:
        blob = " ".join(str(i.get(k, "")) for k in ["message", "summary", "kind", "id"] ).lower()
        if qn and qn not in blob:
            continue
        if not match_filters(i, filters):
            continue
        out.append(i)
    return out
