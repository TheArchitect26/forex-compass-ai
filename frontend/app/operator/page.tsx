"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Card, CardTitle } from "@/components/ui";

export default function OperatorCenterPage() {
  const [metrics, setMetrics] = useState<any>(null);

  useEffect(() => {
    api("/api/system/metrics").then((r) => setMetrics(r.metrics));
  }, []);

  return <div className="space-y-4">
    <h1 className="text-xl font-semibold">Operator Center</h1>
    <Card><CardTitle>Live workloads</CardTitle><div className="text-xs">Running workers: {metrics?.worker_health ?? "..."}</div></Card>
    <Card><CardTitle>Queue and failures</CardTitle><div className="text-xs">Backlog: {metrics?.queue_backlog ?? 0} | Failed: {metrics?.failed_tasks ?? 0}</div></Card>
    <Card><CardTitle>Throughput & latency</CardTitle><div className="text-xs">Replay throughput: {metrics?.replay_throughput ?? 0} | Ingestion throughput: {metrics?.ingestion_throughput ?? 0} | Replay latency ms: {metrics?.replay_latency_ms ?? 0}</div></Card>
    <Card><CardTitle>Safety</CardTitle><p className="text-xs text-muted">Operator tooling only. Advisory workflows only. No trade execution.</p></Card>
  </div>;
}
