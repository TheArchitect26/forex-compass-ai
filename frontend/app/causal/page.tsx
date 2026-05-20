"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Card, CardTitle } from "@/components/ui";

export default function CausalConsolePage() {
  const [analysis, setAnalysis] = useState<any>(null);
  const [graph, setGraph] = useState<any>(null);
  const [propagation, setPropagation] = useState<any>(null);
  const [effect, setEffect] = useState<any>(null);

  useEffect(() => {
    api("/api/causal/analyze", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setAnalysis);
    api("/api/causal/graph", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setGraph);
    api("/api/causal/propagation", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setPropagation);
    api("/api/causal/intervention-effect", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setEffect);
  }, []);

  return <div className="space-y-4">
    <h1 className="text-xl font-semibold">Causal Intelligence Console</h1>
    <Card><CardTitle>Root-cause analysis</CardTitle><div className="text-xs">{analysis?.likely_root_causes?.map((c:any)=>`${c.cause}:${c.score}`).join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Causal graph summary</CardTitle><div className="text-xs">Nodes: {graph?.nodes?.length ?? 0} | Edges: {graph?.edges?.length ?? 0}</div></Card>
    <Card><CardTitle>Propagation chain</CardTitle><div className="text-xs">{propagation?.propagation_chain?.join(" -> ") ?? "..."}</div></Card>
    <Card><CardTitle>Intervention-effect estimate</CardTitle><div className="text-xs">Benefit: {effect?.likely_benefit ?? "..."} | Confidence: {effect?.confidence ?? "..."}</div></Card>
    <Card><CardTitle>Uncertainty & evidence</CardTitle><div className="text-xs">Notes: {analysis?.uncertainty_notes?.join(", ") ?? "..."} | Evidence: {analysis?.evidence_references?.join(", ") ?? "..."}</div></Card>
    <Card><CardTitle>No-execution safety</CardTitle><p className="text-xs text-muted">Causal outputs are advisory, uncertain, and never auto-applied.</p></Card>
  </div>;
}
