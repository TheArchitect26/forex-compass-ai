"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Card, CardTitle } from "@/components/ui";

export default function MetaOperationsConsolePage() {
  const [status, setStatus] = useState<any>(null);
  const [resilience, setResilience] = useState<any>(null);
  const [timeline, setTimeline] = useState<any[]>([]);
  const [sync, setSync] = useState<any>(null);

  useEffect(() => {
    api("/api/meta/coordination-status").then(setStatus);
    api("/api/meta/resilience").then((r) => setResilience(r.resilience));
    api("/api/meta/timeline").then((r) => setTimeline(r.timeline || []));
  }, []);

  const runSyncCheck = async () => {
    const out = await api("/api/meta/synchronization-check", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ unsynchronized_eras: true, replay_governance_drift: true })
    });
    setSync(out);
  };

  return <div className="space-y-4">
    <h1 className="text-xl font-semibold">Meta-Operations Console</h1>
    <Card><CardTitle>Coordination pressure</CardTitle><div className="text-xs">Pressure: {status?.coordination_pressure ?? "..."} | Level: {status?.level ?? "..."}</div></Card>
    <Card><CardTitle>Institutional cohesion scores</CardTitle><div className="text-xs">Coordination resilience: {resilience?.coordination_resilience ?? "..."} | Synchronization integrity: {resilience?.synchronization_integrity ?? "..."} | Cohesion: {resilience?.institutional_cohesion ?? "..."}</div></Card>
    <Card><CardTitle>Synchronization status</CardTitle><button className="px-2 py-1 rounded bg-accent text-bg text-xs" onClick={runSyncCheck}>Run sync check</button><div className="text-xs mt-2">Flags: {(sync?.flags || []).join(", ") || "none"}</div></Card>
    <Card><CardTitle>Unified institutional timeline</CardTitle><div className="text-xs">Events tracked: {timeline.length}</div></Card>
    <Card><CardTitle>Safety</CardTitle><p className="text-xs text-muted">Meta-layer only coordinates and explains. No autonomous irreversible actions.</p></Card>
  </div>;
}
