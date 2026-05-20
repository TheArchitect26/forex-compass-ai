"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Card, CardTitle } from "@/components/ui";

export default function ExecutiveConsolePage() {
  const [status, setStatus] = useState<any>(null);
  const [briefings, setBriefings] = useState<any[]>([]);
  const [anomalies, setAnomalies] = useState<any[]>([]);
  const [history, setHistory] = useState<any>(null);
  const [archiveQ, setArchiveQ] = useState("");
  const [archiveResults, setArchiveResults] = useState<any[]>([]);

  useEffect(() => {
    api("/api/system/strategic-status").then(setStatus);
    api("/api/system/briefings").then(setBriefings);
    api("/api/system/history/summary").then(setHistory);
  }, []);

  const runAnomalyInterpretation = async () => {
    const out = await api("/api/system/anomalies/interpret", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ replay_outlier_rate: 0.32, calibration_drift_jump: 17, workload_spike: 1, recommendations: [{ recommendation: "increase aggressive exploration" }, { recommendation: "reduce exposure" }] }),
    });
    setAnomalies(out.anomalies || []);
  };
  const searchArchive = async () => {
    const out = await api(`/api/system/archive/search?q=${encodeURIComponent(archiveQ)}`);
    setArchiveResults(out.results || []);
  };

  return <div className="space-y-4">
    <h1 className="text-xl font-semibold">Executive Research Console</h1>
    <Card><CardTitle>Strategic scores</CardTitle><div className="text-xs">Stability: {status?.strategic_scores?.strategic_stability_score ?? "..."} | Pressure: {status?.strategic_scores?.operational_pressure_score ?? "..."} | Confidence: {status?.strategic_scores?.intelligence_confidence_score ?? "..."}</div></Card>
    <Card><CardTitle>Strategic briefings</CardTitle><div className="text-xs space-y-1">{briefings.map((b)=> <div key={b.id}>{b.severity}: {b.title}</div>)}</div></Card>
    <Card><CardTitle>Dependency graph summary</CardTitle><div className="text-xs space-y-1">{(status?.dependency_map || []).map((d:any, i:number)=> <div key={i}>{d.source} → {d.target} ({d.weight})</div>)}</div></Card>
    <Card><CardTitle>Anomaly feed</CardTitle><button onClick={runAnomalyInterpretation} className="px-2 py-1 rounded bg-accent text-bg text-xs">Interpret anomalies</button><div className="text-xs mt-2 space-y-1">{anomalies.map((a:any)=> <div key={a.type}>{a.type} (conf {a.confidence})</div>)}</div><p className="text-xs text-muted mt-2">Advisory only. Human review required. No execution.</p></Card>
    <Card><CardTitle>Long-horizon memory</CardTitle><div className="text-xs">History entries: {history?.count ?? 0} | Monthly snapshots: {(history?.monthly_summaries || []).length}</div></Card>
    <Card><CardTitle>Institutional archive</CardTitle><div className="flex gap-2"><input value={archiveQ} onChange={(e)=>setArchiveQ(e.target.value)} className="px-2 py-1 rounded bg-panel2 border border-border text-xs" placeholder="search strategic archives" /><button onClick={searchArchive} className="px-2 py-1 rounded bg-accent text-bg text-xs">Search</button></div><div className="mt-2 text-xs space-y-1">{archiveResults.map((r:any)=> <div key={r.id}>{r.type}: {r.title} (conf {r.confidence})</div>)}</div></Card>
  </div>;
}
