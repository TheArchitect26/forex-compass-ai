from __future__ import annotations
from datetime import UTC, datetime


def estimate_resources(task_type: str, batch_size: int = 1) -> dict:
    cpu = 1.0
    memory_mb = 256
    if "replay" in task_type or "experiment" in task_type:
        cpu = 2.0
        memory_mb = 768
    if "sweep" in task_type:
        cpu += 1.0
        memory_mb += 512
    return {"cpu": cpu, "memory_mb": memory_mb, "batch_size": max(1, int(batch_size))}


def queue_priority(payload: dict) -> int:
    base = int(payload.get("priority", 50))
    if payload.get("integrity_incident"):
        base += 40
    if float(payload.get("drift_score", 0)) > 70:
        base += 25
    if float(payload.get("drawdown", 0)) > 500:
        base += 35
    return min(100, max(1, base))


def workload_status_summary(workloads: list[dict]) -> dict:
    out = {"queued": 0, "running": 0, "failed": 0, "completed": 0, "retrying": 0}
    for w in workloads:
        st = w.get("status", "queued")
        out[st] = out.get(st, 0) + 1
    return out


def replay_checkpoint(cursor: str | None, steps: int, state: dict) -> dict:
    return {
        "cursor": cursor,
        "steps": steps,
        "state": state,
        "checkpointed_at": datetime.now(UTC).isoformat(),
        "resumable": True,
    }


def restore_checkpoint(checkpoint: dict) -> dict:
    return {
        "cursor": checkpoint.get("cursor"),
        "steps": int(checkpoint.get("steps", 0)),
        "state": checkpoint.get("state", {}),
        "resumed": True,
    }
