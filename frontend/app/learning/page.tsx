"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Card, CardTitle } from "@/components/ui";

export default function LearningPage() {
  const [insights, setInsights] = useState<any[]>([]);
  const [trainStatus, setTrainStatus] = useState<any>(null);
  const refresh = async () => setInsights(await api(`/api/learning/insights`));
  useEffect(() => { refresh(); }, []);
  const train = async () => setTrainStatus(await api(`/api/learning/train`, { method: "POST" }));
  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-semibold">AI Learning Center</h1>
        <button onClick={train} className="px-4 py-2 rounded bg-accent text-bg text-sm font-medium">Retrain ML model</button>
      </div>
      {trainStatus && <Card><CardTitle>Last training run</CardTitle><pre className="text-xs">{JSON.stringify(trainStatus, null, 2)}</pre></Card>}
      <Card>
        <CardTitle>Top-weighted patterns (what the AI has learned works)</CardTitle>
        <table className="w-full text-sm font-mono">
          <thead className="text-xs text-muted"><tr>
            <th className="text-left p-1">Pattern fingerprint</th><th>Pair</th><th>Wins</th><th>Losses</th><th>Win rate</th><th>Weight</th>
          </tr></thead>
          <tbody>{insights.map((r, i) => (
            <tr key={i} className="border-t border-border">
              <td className="p-1 text-xs">{r.pattern}</td>
              <td className="text-center">{r.pair}</td>
              <td className="text-center">{r.wins}</td>
              <td className="text-center">{r.losses}</td>
              <td className="text-center">{r.win_rate}%</td>
              <td className="text-center">{r.weight.toFixed(2)}</td>
            </tr>
          ))}</tbody>
        </table>
        {insights.length === 0 && <p className="text-xs text-muted mt-2">No learning data yet. Close some signals as win/loss to build memory.</p>}
      </Card>
    </div>
  );
}
