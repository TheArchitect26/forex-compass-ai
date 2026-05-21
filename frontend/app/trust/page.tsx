"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Card, CardTitle } from "@/components/ui";

export default function TrustGovernanceConsolePage() {
  const [constitution, setConstitution] = useState<any[]>([]);
  const [explainability, setExplainability] = useState<any>(null);
  const [incidents, setIncidents] = useState<any[]>([]);
  const [pressure, setPressure] = useState<any>(null);

  useEffect(() => {
    api("/api/governance/constitution").then((r) => setConstitution(r.rules || []));
    api("/api/governance/explainability-score").then(setExplainability);
    api("/api/governance/incidents").then(setIncidents);
    api("/api/governance/trust-pressure", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ unresolved_contradictions: 1, anomaly_fatigue: 1 }) }).then(setPressure);
  }, []);

  return <div className="space-y-4">
    <h1 className="text-xl font-semibold">Trust & Governance Console</h1>
    <Card><CardTitle>Constitutional compliance</CardTitle><div className="text-xs space-y-1">{constitution.map((r:any)=> <div key={r.key}>{r.enabled ? "✅" : "⚠️"} {r.text}</div>)}</div></Card>
    <Card><CardTitle>Explainability integrity</CardTitle><div className="text-xs">Score: {explainability?.score ?? "..."}</div></Card>
    <Card><CardTitle>Trust pressure indicators</CardTitle><div className="text-xs">Pressure: {pressure?.trust_pressure_score ?? "..."} | Level: {pressure?.level ?? "..."}</div></Card>
    <Card><CardTitle>Governance warnings</CardTitle><div className="text-xs space-y-1">{incidents.map((i:any)=> <div key={i.id}>{i.severity}: {i.incident_type}</div>)}</div></Card>
    <Card><CardTitle>Policy safety</CardTitle><p className="text-xs text-muted">All recommendations remain advisory only and reversible. No autonomous execution.</p></Card>
  </div>;
}
