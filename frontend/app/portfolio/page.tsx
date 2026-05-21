"use client";
import { useState } from "react";
import { api } from "@/lib/api";
import { Card, CardTitle } from "@/components/ui";

export default function PortfolioLabPage() {
  const [session, setSession] = useState<any>(null);
  const [stress, setStress] = useState<any>(null);

  const start = async () => {
    const now = new Date();
    const start = new Date(now.getTime() - 24 * 3600 * 1000).toISOString();
    const out = await api(`/api/replay/portfolio/start`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ pair: "EUR/USD", timeframe: "1h", start, end: now.toISOString(), initial_balance: 10000, sizing_mode: "fixed_risk" }) });
    setSession(await api(`/api/replay/portfolio/${out.portfolio_session_id}`));
  };
  const step = async () => {
    if (!session) return;
    await api(`/api/replay/portfolio/step`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ portfolio_session_id: session.id, action: "accept" }) });
    setSession(await api(`/api/replay/portfolio/${session.id}`));
  };
  const runStress = async () => setStress(await api(`/api/replay/stress-test`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ base_score: 60 }) }));

  return (
    <div className="space-y-4">
      <h1 className="text-xl font-semibold">Portfolio Research Lab</h1>
      <div className="flex gap-2">
        <button onClick={start} className="px-3 py-1 rounded bg-accent text-bg">Start portfolio replay</button>
        <button onClick={step} className="px-3 py-1 rounded bg-panel2 border border-border">Step</button>
        <button onClick={runStress} className="px-3 py-1 rounded bg-panel2 border border-border">Run stress test</button>
      </div>
      {session && <Card><CardTitle>Portfolio state</CardTitle><div className="text-xs">Balance: {session.balance} | Open: {session.open_positions?.length || 0} | Closed: {session.closed_positions?.length || 0}</div><div className="text-xs mt-1">Drawdown: {session.analytics?.max_drawdown} | Expectancy: {session.analytics?.expectancy} | Recovery: {session.analytics?.recovery_factor}</div><div className="text-xs mt-1">Session exposure: {session.risk_state?.session_exposure || "n/a"} | Correlation warning: {session.risk_state?.correlation_warning || "none"}</div></Card>}
      {stress && <Card><CardTitle>Stress results</CardTitle><div className="text-xs">Score: {stress.stress_score}</div><div className="text-xs">Scenarios: {(stress.scenarios||[]).join(", ")}</div></Card>}
      <Card><CardTitle>Disclaimer</CardTitle><p className="text-xs text-muted">Simulation research only. This is not broker execution and does not place real trades.</p></Card>
    </div>
  );
}
