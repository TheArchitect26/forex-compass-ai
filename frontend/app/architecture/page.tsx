"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Card, CardTitle } from "@/components/ui";

export default function ArchitecturePage() {
  const [status, setStatus] = useState<any>(null);
  const [overlap, setOverlap] = useState<any>(null);
  const [plan, setPlan] = useState<any>(null);
  const [risk, setRisk] = useState<any>(null);

  useEffect(() => {
    api("/api/architecture/status").then(setStatus);
    api("/api/architecture/overlap-scan", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setOverlap);
    api("/api/architecture/consolidation-plan", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setPlan);
    api("/api/architecture/simplification-risk", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setRisk);
  }, []);

  return <div className="space-y-4">
    <h1 className="text-xl font-semibold">Architectural Coherence</h1>
    <Card><CardTitle>Coherence scores</CardTitle><div className="text-xs">Subsystem: {status?.subsystem_coherence ?? "..."} | API clarity: {status?.api_clarity ?? "..."} | Simplicity: {status?.architectural_simplicity ?? "..."}</div></Card>
    <Card><CardTitle>Overlap warnings</CardTitle><div className="text-xs">{overlap?.overlapping_apis?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Consolidation proposals</CardTitle><div className="text-xs">{plan?.proposals?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Simplification risks</CardTitle><div className="text-xs">{risk?.simplification_risks?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>High-burden subsystems</CardTitle><div className="text-xs">{risk?.high_burden_subsystems?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Advisory-only safety</CardTitle><p className="text-xs text-muted">Architecture outputs are advisory only. No execution, schema rewrites, or merges are auto-applied.</p></Card>
  </div>;
}
