"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Card, CardTitle } from "@/components/ui";

export default function PathwaysConsolePage() {
  const [rec, setRec] = useState<any>(null);
  const [evals, setEvals] = useState<any>(null);

  useEffect(() => {
    api("/api/pathways/recommend", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ pressure: 0.82, operator_capacity: 0.32, replay_confidence: 0.5, data_integrity: 0.7 }) }).then(setRec);
    api("/api/pathways/evaluate", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ pressure: 0.82, operator_capacity: 0.32, replay_confidence: 0.5, data_integrity: 0.7 }) }).then(setEvals);
  }, []);

  return <div className="space-y-4">
    <h1 className="text-xl font-semibold">Strategic Pathways Console</h1>
    <Card><CardTitle>Recommended pathway</CardTitle><div className="text-xs">{rec?.recommended_pathway ?? "..."}</div></Card>
    <Card><CardTitle>Active pressure signals</CardTitle><div className="text-xs">{Object.entries(evals?.triggers || {}).map(([k,v])=>`${k}:${v}`).join(" | ") || "..."}</div></Card>
    <Card><CardTitle>Trigger conditions</CardTitle><div className="text-xs">{Object.entries(rec?.trigger_conditions || {}).map(([k,v])=>`${k}:${v}`).join(" | ") || "..."}</div></Card>
    <Card><CardTitle>Entry / Exit criteria</CardTitle><div className="text-xs">Entry: {rec?.entry_criteria?.join(", ") ?? "..."} | Exit: {rec?.exit_criteria?.join(", ") ?? "..."}</div></Card>
    <Card><CardTitle>Escalation / De-escalation logic</CardTitle><div className="text-xs">Escalate: {rec?.escalation_rules?.join(", ") ?? "..."} | De-escalate: {rec?.de_escalation_rules?.join(", ") ?? "..."}</div></Card>
    <Card><CardTitle>Reversibility & approval</CardTitle><div className="text-xs">{rec?.reversibility_notes ?? "..."} | Human approval required: {String(rec?.human_approval_required)}</div></Card>
    <Card><CardTitle>No-execution safety</CardTitle><p className="text-xs text-muted">Adaptive pathways are advisory planning only and never auto-apply strategy changes.</p></Card>
  </div>;
}
