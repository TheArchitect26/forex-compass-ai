"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Card, CardTitle } from "@/components/ui";

export default function EpistemicGovernanceConsolePage() {
  const [coherence, setCoherence] = useState<any>(null);
  const [assumptions, setAssumptions] = useState<any[]>([]);
  const [fragmentation, setFragmentation] = useState<any>(null);

  useEffect(() => {
    api("/api/governance/coherence-status").then((r) => setCoherence(r.coherence_scores));
    api("/api/governance/assumptions").then(setAssumptions);
  }, []);

  const checkFragmentation = async () => {
    const out = await api("/api/governance/knowledge/fragmentation", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ nodes: [{ id: "a" }, { id: "b" }, { id: "c" }], edges: [{ source: "a", target: "b", relation: "supports", resolved: true }] }),
    });
    setFragmentation(out.fragmentation);
  };

  return <div className="space-y-4">
    <h1 className="text-xl font-semibold">Epistemic Governance Console</h1>
    <Card><CardTitle>Coherence status</CardTitle><div className="text-xs">Epistemic integrity: {coherence?.epistemic_integrity ?? "..."} | Contradiction pressure: {coherence?.contradiction_pressure ?? "..."} | Governance resilience: {coherence?.governance_resilience ?? "..."}</div></Card>
    <Card><CardTitle>Assumption tracking</CardTitle><div className="text-xs space-y-1">{assumptions.map((a:any)=> <div key={a.id}>{a.assumption} (conf {a.historical_confidence})</div>)}</div></Card>
    <Card><CardTitle>Contradiction map</CardTitle><button onClick={checkFragmentation} className="px-2 py-1 rounded bg-accent text-bg text-xs">Analyze fragmentation</button><div className="text-xs mt-2">Isolated conclusions: {(fragmentation?.isolated_conclusions || []).join(", ") || "none"} | Unresolved chains: {fragmentation?.unresolved_contradiction_chains ?? 0}</div></Card>
    <Card><CardTitle>Governance note</CardTitle><p className="text-xs text-muted">Human-review-first governance. No autonomous execution. Advisory reasoning only.</p></Card>
  </div>;
}
