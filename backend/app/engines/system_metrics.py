from __future__ import annotations


def aggregate_metrics(workloads: list[dict], incidents: list[dict]) -> dict:
    queued = len([w for w in workloads if w.get("status") == "queued"])
    failed = len([w for w in workloads if w.get("status") == "failed"])
    running = len([w for w in workloads if w.get("status") == "running"])
    replay_tp = sum(float(w.get("throughput", 0)) for w in workloads if "replay" in w.get("type", ""))
    ingestion_tp = sum(float(w.get("throughput", 0)) for w in workloads if "ingestion" in w.get("type", ""))
    latency = round(sum(float(w.get("latency_ms", 0)) for w in workloads) / max(1, len(workloads)), 2)
    return {
        "scheduler_health": "ok" if failed < 5 else "degraded",
        "worker_health": "ok" if running > 0 else "idle",
        "queue_backlog": queued,
        "failed_tasks": failed,
        "replay_throughput": replay_tp,
        "ingestion_throughput": ingestion_tp,
        "replay_latency_ms": latency,
        "integrity_incidents": len(incidents),
        "database_health": "ok",
    }
