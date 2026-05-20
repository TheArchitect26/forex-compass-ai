"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Card, CardTitle } from "@/components/ui";

export default function TemporalConsolePage() {
  const [status, setStatus] = useState<any>(null);
  const [memory, setMemory] = useState<any>(null);
  const [rhythm, setRhythm] = useState<any>(null);
  const [conflicts, setConflicts] = useState<any>(null);

  useEffect(() => {
    api("/api/temporal/timing-status").then(setStatus);
    api("/api/temporal/memory").then(setMemory);
    api("/api/temporal/rhythm-scan", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ volatility: 0.6, operator_workload: 0.7, alert_frequency: 0.75 }) }).then(setRhythm);
    api("/api/temporal/timing-conflicts", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ urgent_low_importance: true, important_not_urgent: true }) }).then(setConflicts);
  }, []);

  return <div className="space-y-4">
    <h1 className="text-xl font-semibold">Temporal Intelligence Console</h1>
    <Card><CardTitle>Timing status</CardTitle><div className="text-xs">Turbulence: {status?.timing_status?.short_term_turbulence ?? "..."} | Sensitivity: {status?.timing_status?.timing_sensitivity ?? "..."}</div></Card>
    <Card><CardTitle>Strategic pacing recommendations</CardTitle><div className="text-xs">{status?.strategic_pacing?.strategic_pacing ?? "..."}</div></Card>
    <Card><CardTitle>Rhythm state</CardTitle><div className="text-xs">{rhythm?.rhythm_state ?? "..."}</div></Card>
    <Card><CardTitle>Urgency vs importance conflicts</CardTitle><div className="text-xs">{conflicts?.conflicts?.join(", ") ?? "none"}</div></Card>
    <Card><CardTitle>Timing memory</CardTitle><div className="text-xs">{memory?.major_timing_corrections?.join(", ") ?? "..."}</div></Card>
    <Card><CardTitle>No-execution safety</CardTitle><p className="text-xs text-muted">Temporal recommendations are advisory-only. Human judgment is final and no trades are executed.</p></Card>
  </div>;
}
