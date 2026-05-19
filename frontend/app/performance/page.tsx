"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Card, CardTitle, Stat } from "@/components/ui";

export default function PerformancePage() {
  const [data, setData] = useState<any>(null);
  useEffect(() => { (async () => setData(await api(`/api/performance`)))(); }, []);
  if (!data) return <p className="text-sm text-muted">Loading…</p>;
  return (
    <div className="space-y-4">
      <h1 className="text-xl font-semibold">Performance Analytics</h1>
      <div className="grid grid-cols-3 gap-3">
        <Stat label="Closed signals" value={data.total} />
        <Stat label="Win rate" value={`${data.win_rate}%`} tone={data.win_rate >= 50 ? "bull" : "bear"} />
        <Stat label="Pairs covered" value={Object.keys(data.by_pair).length} />
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Card>
          <CardTitle>By pair</CardTitle>
          <table className="w-full text-sm font-mono">
            <thead className="text-xs text-muted"><tr><th className="text-left p-1">Pair</th><th>N</th><th>Wins</th><th>PnL</th></tr></thead>
            <tbody>{Object.entries<any>(data.by_pair).map(([p, v]) => (
              <tr key={p} className="border-t border-border"><td className="p-1">{p}</td><td className="text-center">{v.n}</td><td className="text-center">{v.wins}</td><td className="text-center">{v.pnl.toFixed(1)}</td></tr>
            ))}</tbody>
          </table>
        </Card>
        <Card>
          <CardTitle>By regime</CardTitle>
          <table className="w-full text-sm font-mono">
            <thead className="text-xs text-muted"><tr><th className="text-left p-1">Regime</th><th>N</th><th>Wins</th></tr></thead>
            <tbody>{Object.entries<any>(data.by_regime).map(([r, v]) => (
              <tr key={r} className="border-t border-border"><td className="p-1">{r}</td><td className="text-center">{v.n}</td><td className="text-center">{v.wins}</td></tr>
            ))}</tbody>
          </table>
        </Card>
      </div>
    </div>
  );
}
