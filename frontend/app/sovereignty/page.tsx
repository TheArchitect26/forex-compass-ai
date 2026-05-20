"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Card, CardTitle } from "@/components/ui";

export default function HumanSovereigntyConsolePage() {
  const [sovereignty, setSovereignty] = useState<any>(null);
  const [load, setLoad] = useState<any>(null);
  const [focusOut, setFocusOut] = useState<any[]>([]);
  const [resetResult, setResetResult] = useState<any>(null);

  useEffect(() => {
    api("/api/governance/human-sovereignty").then(setSovereignty);
    api("/api/system/operator-load").then(setLoad);
  }, []);

  const runFocusMode = async (mode: string) => {
    const out = await api("/api/governance/focus-mode", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ mode, insights: [{ title: "stability alert", tags: ["stability"] }, { title: "replay drift", tags: ["replay"] }] })
    });
    setFocusOut(out.prioritized_insights || []);
  };

  const runReset = async () => {
    const out = await api("/api/governance/strategic-reset", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ action: "archive_consolidation", approved_by_human: true })
    });
    setResetResult(out);
  };

  return <div className="space-y-4">
    <h1 className="text-xl font-semibold">Human Sovereignty Console</h1>
    <Card><CardTitle>Human authority guarantees</CardTitle><div className="text-xs space-y-1">{(sovereignty?.guarantees || []).map((g:string, i:number)=> <div key={i}>✅ {g}</div>)}</div></Card>
    <Card><CardTitle>Cognitive load and clarity</CardTitle><div className="text-xs">Cognitive load: {load?.operator_load?.cognitive_load_score ?? "..."} | Clarity: {load?.operator_load?.strategic_clarity_score ?? "..."} | Governance burden: {load?.operator_load?.governance_burden_score ?? "..."}</div></Card>
    <Card><CardTitle>Focus modes</CardTitle><div className="flex gap-2"><button className="px-2 py-1 rounded bg-accent text-bg text-xs" onClick={()=>runFocusMode("stability_focus")}>Stability</button><button className="px-2 py-1 rounded bg-panel2 border border-border text-xs" onClick={()=>runFocusMode("replay_focus")}>Replay</button><button className="px-2 py-1 rounded bg-panel2 border border-border text-xs" onClick={()=>runFocusMode("governance_focus")}>Governance</button></div><div className="text-xs mt-2">Prioritized: {focusOut.map((x:any)=>x.title).join(", ") || "none"}</div></Card>
    <Card><CardTitle>Strategic reset controls</CardTitle><button className="px-2 py-1 rounded bg-panel2 border border-border text-xs" onClick={runReset}>Run reversible reset</button><div className="text-xs mt-2">Last reset: {resetResult?.action || "none"} | reversible: {String(resetResult?.reversible ?? false)} | approved: {String(resetResult?.approved_by_human ?? false)}</div></Card>
    <Card><CardTitle>Safety</CardTitle><p className="text-xs text-muted">No autonomous execution. No self-authorized strategic changes. Human judgment is final authority.</p></Card>
  </div>;
}
