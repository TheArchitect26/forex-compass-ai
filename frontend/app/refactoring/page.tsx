"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Card, CardTitle } from "@/components/ui";

export default function RefactoringPage() {
  const [status, setStatus] = useState<any>(null);
  const [entropy, setEntropy] = useState<any>(null);
  const [recovery, setRecovery] = useState<any>(null);
  const [coupling, setCoupling] = useState<any>(null);
  const [priorities, setPriorities] = useState<any>(null);

  useEffect(() => {
    api("/api/refactoring/status").then(setStatus);
    api("/api/refactoring/entropy-scan", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setEntropy);
    api("/api/refactoring/recovery-plan", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setRecovery);
    api("/api/refactoring/coupling-analysis", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setCoupling);
    api("/api/refactoring/refactor-priorities", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setPriorities);
  }, []);

  return <div className="space-y-4">
    <h1 className="text-xl font-semibold">Refactoring Intelligence</h1>
    <Card><CardTitle>Entropy scores</CardTitle><div className="text-xs">Entropy: {status?.entropy_score ?? "..."} | Coupling: {status?.coupling_risk_score ?? "..."} | Maintainability: {status?.maintainability_score ?? "..."}</div></Card>
    <Card><CardTitle>Coupling analysis</CardTitle><div className="text-xs">{coupling?.tightly_coupled_modules?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Architectural recovery proposals</CardTitle><div className="text-xs">{recovery?.architectural_recovery_proposals?.map((x:any)=>x.action).join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Refactor priorities</CardTitle><div className="text-xs">{priorities?.priority_rankings?.map((x:any)=>`P${x.priority}:${x.focus}`).join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Maintenance hotspots</CardTitle><div className="text-xs">{entropy?.maintenance_hotspots?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Simplification opportunities</CardTitle><div className="text-xs">{priorities?.simplification_opportunities?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Advisory-only safety</CardTitle><p className="text-xs text-muted">Refactoring intelligence is advisory only. No code is auto-deleted, no migrations are auto-run, and no architecture is auto-changed.</p></Card>
  </div>;
}
