"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Card, CardTitle } from "@/components/ui";

export default function StrategicRenewalConsolePage() {
  const [adapt, setAdapt] = useState<any>(null);
  const [identity, setIdentity] = useState<any>(null);
  const [timeline, setTimeline] = useState<any>(null);
  const [plans, setPlans] = useState<any[]>([]);
  const [dogma, setDogma] = useState<any>(null);

  useEffect(() => {
    api("/api/governance/adaptability-status").then((r) => setAdapt(r.adaptability));
    api("/api/governance/identity/health").then(setIdentity);
    api("/api/system/evolution-timeline").then(setTimeline);
    api("/api/governance/evolution/plan").then(setPlans);
  }, []);

  const runDogmaScan = async () => {
    const out = await api("/api/governance/anti-dogma/scan", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ unchallenged_assumptions: 6, stale_narratives: 5, governance_ossification: 0.7 })
    });
    setDogma(out);
  };

  return <div className="space-y-4">
    <h1 className="text-xl font-semibold">Strategic Renewal Console</h1>
    <Card><CardTitle>Inertia scores</CardTitle><div className="text-xs">Strategic inertia: {adapt?.strategic_inertia ?? "..."} | Governance inertia: {adapt?.governance_inertia ?? "..."} | Replay rigidity: {adapt?.replay_rigidity ?? "..."}</div></Card>
    <Card><CardTitle>Modernization proposals</CardTitle><div className="text-xs space-y-1">{plans.map((p:any)=> <div key={p.id}>{p.proposed_evolution} · compatibility: {p.compatibility_impact}</div>)}</div></Card>
    <Card><CardTitle>Institutional identity health</CardTitle><div className="text-xs">Constitution preserved: {String(identity?.constitutional_principles_preserved ?? false)} | Mission continuity: {identity?.institutional_mission_continuity ?? "..."}</div></Card>
    <Card><CardTitle>Anti-dogma warnings</CardTitle><button className="px-2 py-1 rounded bg-accent text-bg text-xs" onClick={runDogmaScan}>Run anti-dogma scan</button><div className="text-xs mt-2">Warnings: {(dogma?.warnings || []).join(", ") || "none"}</div></Card>
    <Card><CardTitle>Evolution timeline</CardTitle><div className="text-xs">Transitions: {(timeline?.governance_transitions || []).join(" | ") || "none"}</div></Card>
    <Card><CardTitle>Safety</CardTitle><p className="text-xs text-muted">Operator-reviewed transitions only. Reversible where possible. No autonomous strategic authority.</p></Card>
  </div>;
}
