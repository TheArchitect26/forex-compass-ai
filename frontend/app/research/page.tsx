"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Card, CardTitle } from "@/components/ui";

export default function ResearchCenterPage() {
  const [health, setHealth] = useState<any>(null);
  const [tasks, setTasks] = useState<any[]>([]);
  const [findings, setFindings] = useState<any[]>([]);
  const [q, setQ] = useState("");
  const [results, setResults] = useState<any[]>([]);

  const refresh = async () => {
    setHealth(await api("/api/system/health"));
    setTasks(await api("/api/system/research/tasks"));
    setFindings(await api("/api/system/research/findings"));
  };

  useEffect(() => { refresh(); }, []);
  const doSearch = async () => {
    const out = await api(`/api/research/search?q=${encodeURIComponent(q)}`);
    setResults(out.results || []);
  };

  return <div className="space-y-4">
    <h1 className="text-xl font-semibold">Research Center</h1>
    <Card><CardTitle>System health</CardTitle><div className="text-xs">Global score: {health?.system_health?.score ?? "..."}</div></Card>
    <Card><CardTitle>Active investigations</CardTitle><div className="space-y-1 text-xs">{tasks.map(t => <div key={t.id}>#{t.id} {t.type} · {t.status} · {t.priority}</div>)}</div></Card>
    <Card><CardTitle>Recent findings</CardTitle><div className="space-y-1 text-xs">{findings.map(f => <div key={f.id}>{f.message} (conf {f.confidence})</div>)}</div><p className="text-xs text-muted mt-2">Recommendations are advisory only and never auto-applied. No trade execution.</p></Card>
    <Card><CardTitle>Search & saved investigations</CardTitle><div className="flex gap-2"><input value={q} onChange={(e)=>setQ(e.target.value)} className="px-2 py-1 rounded bg-panel2 border border-border text-xs" placeholder="search findings/experiments/replays" /><button onClick={doSearch} className="px-2 py-1 rounded bg-accent text-bg text-xs">Search</button></div><div className="mt-2 text-xs space-y-1">{results.map((r)=> <div key={r.id}>{r.kind}: {r.summary || r.message}</div>)}</div></Card>
  </div>;
}
