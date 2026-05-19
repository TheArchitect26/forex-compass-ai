"use client";
import { useState } from "react";
import { api } from "@/lib/api";
import { Card, CardTitle, Stat } from "@/components/ui";

export default function BacktestPage() {
  const [pair, setPair] = useState("EUR/USD");
  const [tf, setTf] = useState("1h");
  const [fast, setFast] = useState(20);
  const [slow, setSlow] = useState(50);
  const [res, setRes] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const run = async () => {
    setLoading(true);
    try { setRes(await api(`/api/backtest/ema-cross?pair=${encodeURIComponent(pair)}&timeframe=${tf}&fast=${fast}&slow=${slow}`)); }
    finally { setLoading(false); }
  };

  return (
    <div className="space-y-4">
      <h1 className="text-xl font-semibold">Backtesting</h1>
      <Card>
        <CardTitle>EMA cross strategy</CardTitle>
        <div className="grid grid-cols-2 md:grid-cols-5 gap-2 text-sm">
          <input className="bg-panel2 border border-border rounded px-2 py-1" value={pair} onChange={e => setPair(e.target.value)} />
          <input className="bg-panel2 border border-border rounded px-2 py-1" value={tf} onChange={e => setTf(e.target.value)} />
          <input type="number" className="bg-panel2 border border-border rounded px-2 py-1" value={fast} onChange={e => setFast(+e.target.value)} />
          <input type="number" className="bg-panel2 border border-border rounded px-2 py-1" value={slow} onChange={e => setSlow(+e.target.value)} />
          <button onClick={run} disabled={loading} className="px-3 py-1 rounded bg-accent text-bg font-medium">{loading ? "…" : "Run"}</button>
        </div>
      </Card>
      {res && (
        <>
          <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
            <Stat label="Sharpe" value={res.metrics.sharpe} tone={res.metrics.sharpe > 1 ? "bull" : "neutral"} />
            <Stat label="Win rate" value={`${res.metrics.win_rate}%`} />
            <Stat label="Max DD" value={`${res.metrics.max_drawdown_pct}%`} tone="bear" />
            <Stat label="Expectancy (pips)" value={res.metrics.expectancy} />
            <Stat label="Final equity" value={res.metrics.final_equity} />
          </div>
          <Card>
            <CardTitle>Equity curve (sampled)</CardTitle>
            <div className="overflow-x-auto text-xs font-mono text-muted">
              {res.equity_curve.length} points · final {res.equity_curve.at(-1)?.v?.toFixed(3)}
            </div>
          </Card>
        </>
      )}
    </div>
  );
}
