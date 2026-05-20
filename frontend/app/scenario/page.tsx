"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Card, CardTitle } from "@/components/ui";

export default function ScenarioLabPage() {
  const [run, setRun] = useState<any>(null);
  const [compare, setCompare] = useState<any>(null);
  const [memory, setMemory] = useState<any>(null);

  useEffect(() => {
    api("/api/scenario/run", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ scenario: "governance_simplification" }) }).then(setRun);
    api("/api/scenario/compare", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ left: "pause_expansion", right: "continue_research", left_score: 0.66, right_score: 0.61 }) }).then(setCompare);
    api("/api/scenario/memory").then(setMemory);
  }, []);

  return <div className="space-y-4">
    <h1 className="text-xl font-semibold">Scenario Lab</h1>
    <Card><CardTitle>Scenario runner</CardTitle><div className="text-xs">Scenario: {run?.scenario ?? "..."} | Horizon: {run?.time_horizon ?? "..."}</div></Card>
    <Card><CardTitle>Consequence map</CardTitle><div className="text-xs">Primary: {run?.primary_effects?.join(", ") ?? "..."} | Second-order: {run?.second_order_effects?.join(", ") ?? "..."}</div></Card>
    <Card><CardTitle>Comparison cards</CardTitle><div className="text-xs">Preferred: {compare?.preferred_option ?? "..."}</div></Card>
    <Card><CardTitle>Tradeoff summary</CardTitle><div className="text-xs">{compare?.tradeoff_table?.map((t:any)=>`${t.option}(fit:${t.fit}, burden:${t.burden})`).join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Uncertainty notes</CardTitle><div className="text-xs">{compare?.uncertainty_notes?.join(", ") ?? "..."}</div></Card>
    <Card><CardTitle>Recommended human review</CardTitle><div className="text-xs">{run?.recommended_human_review ?? "..."}</div></Card>
    <Card><CardTitle>No-execution safety</CardTitle><p className="text-xs text-muted">Scenario output is advisory only and never auto-applies changes.</p></Card>
  </div>;
}
