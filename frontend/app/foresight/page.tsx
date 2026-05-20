"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Card, CardTitle } from "@/components/ui";

export default function ForesightConsolePage() {
  const [status, setStatus] = useState<any>(null);
  const [warnings, setWarnings] = useState<any>(null);
  const [plan, setPlan] = useState<any>(null);
  const [memory, setMemory] = useState<any>(null);

  useEffect(() => {
    api("/api/foresight/status").then(setStatus);
    api("/api/foresight/early-warnings", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ operator_overload: 0.75, replay_debt: 0.6 }) }).then(setWarnings);
    api("/api/foresight/intervention-plan", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ intervention_urgency: 0.72 }) }).then(setPlan);
    api("/api/foresight/memory").then(setMemory);
  }, []);

  return <div className="space-y-4">
    <h1 className="text-xl font-semibold">Foresight Console</h1>
    <Card><CardTitle>Trajectory status & scores</CardTitle><div className="text-xs">Trajectory: {status?.trajectory_status?.trajectory ?? "..."} | Instability: {status?.foresight_scores?.instability_probability ?? "..."}</div></Card>
    <Card><CardTitle>Active early warnings</CardTitle><div className="text-xs">{warnings?.warnings?.map((w:any)=>`${w.warning}:${w.classification}`).join(", ") ?? "none"}</div></Card>
    <Card><CardTitle>Intervention suggestions</CardTitle><div className="text-xs">{plan?.intervention_plan?.join(", ") ?? "..."}</div></Card>
    <Card><CardTitle>Warning horizons</CardTitle><div className="text-xs">{warnings?.warnings?.map((w:any)=>w.estimated_time_horizon).join(", ") ?? "..."}</div></Card>
    <Card><CardTitle>False-alarms / missed-warnings memory</CardTitle><div className="text-xs">False alarms: {memory?.false_alarms?.join(", ") ?? "..."} | Missed: {memory?.missed_warnings?.join(", ") ?? "..."}</div></Card>
    <Card><CardTitle>No-execution safety</CardTitle><p className="text-xs text-muted">Foresight is advisory only and never auto-applies strategy changes.</p></Card>
  </div>;
}
