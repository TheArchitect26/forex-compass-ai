"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Card, CardTitle, Stat, ConfidenceBar } from "@/components/ui";
import PriceChart from "@/components/PriceChart";
import clsx from "clsx";

type Heat = { pair: string; change_pct: number; price: number };
type Signal = {
  id: number; pair: string; direction: "BUY"|"SELL"; confidence: number;
  entry: number; stop_loss: number; take_profit: number; risk_reward: number;
  market_regime: string; explanation: string; created_at: string;
};

export default function Dashboard() {
  const [heat, setHeat] = useState<Heat[]>([]);
  const [signals, setSignals] = useState<Signal[]>([]);
  const [pair, setPair] = useState("EUR/USD");
  const [scanning, setScanning] = useState(false);

  useEffect(() => { (async () => {
    setHeat((await api<{items: Heat[]}>(`/api/market/heatmap`)).items);
    setSignals(await api<Signal[]>(`/api/signals`));
  })(); }, []);

  const scan = async () => {
    setScanning(true);
    try { await api(`/api/signals/scan`, { method: "POST" }); setSignals(await api<Signal[]>(`/api/signals`)); }
    finally { setScanning(false); }
  };

  const openCount = signals.filter(s => s.id && s).length;
  const avgConf = signals.length ? Math.round(signals.reduce((a, s) => a + s.confidence, 0) / signals.length) : 0;

  return (
    <div className="space-y-5">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-xl font-semibold">Dashboard</h1>
          <p className="text-xs text-muted">Live market intelligence — signal-only. You execute trades manually.</p>
        </div>
        <button onClick={scan} disabled={scanning}
          className="px-4 py-2 rounded bg-accent text-bg text-sm font-medium disabled:opacity-50">
          {scanning ? "Scanning…" : "Run AI scan"}
        </button>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        <Stat label="Active signals" value={signals.length} />
        <Stat label="Avg confidence" value={`${avgConf}%`} tone={avgConf >= 70 ? "bull" : "neutral"} />
        <Stat label="Pairs tracked" value={heat.length} />
        <Stat label="Auto-trade" value="OFF" sub="Human-in-the-loop" tone="bull" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <Card className="lg:col-span-2">
          <div className="flex items-center justify-between mb-3">
            <CardTitle>Live chart — {pair}</CardTitle>
            <select value={pair} onChange={e => setPair(e.target.value)}
              className="bg-panel2 border border-border rounded text-sm px-2 py-1">
              {heat.map(h => <option key={h.pair}>{h.pair}</option>)}
            </select>
          </div>
          <PriceChart pair={pair} />
        </Card>

        <Card>
          <CardTitle>Heatmap (1H change)</CardTitle>
          <div className="space-y-1">
            {heat.map(h => (
              <div key={h.pair} className="flex items-center justify-between text-sm py-1 px-2 rounded hover:bg-panel2 cursor-pointer"
                   onClick={() => setPair(h.pair)}>
                <span className="font-mono">{h.pair}</span>
                <span className="font-mono text-xs text-muted">{h.price.toFixed(5)}</span>
                <span className={clsx("font-mono text-sm",
                  h.change_pct >= 0 ? "text-bull" : "text-bear")}>
                  {h.change_pct >= 0 ? "+" : ""}{h.change_pct.toFixed(2)}%
                </span>
              </div>
            ))}
          </div>
        </Card>
      </div>

      <Card>
        <CardTitle>Latest signals</CardTitle>
        {signals.length === 0 ? (
          <p className="text-sm text-muted">No signals yet. Click <b>Run AI scan</b> to analyze the market.</p>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
            {signals.slice(0, 6).map(s => (
              <div key={s.id} className="bg-panel2 border border-border rounded p-3">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className={clsx("text-xs px-2 py-0.5 rounded font-bold",
                      s.direction === "BUY" ? "bg-bull/20 text-bull" : "bg-bear/20 text-bear")}>
                      {s.direction}
                    </span>
                    <span className="font-mono">{s.pair}</span>
                  </div>
                  <span className="text-xs text-muted">{s.market_regime}</span>
                </div>
                <div className="mt-2 text-xs text-muted">Confidence {s.confidence}%</div>
                <ConfidenceBar value={s.confidence} />
                <div className="mt-2 grid grid-cols-3 gap-1 text-xs font-mono">
                  <div><div className="text-muted">Entry</div>{s.entry}</div>
                  <div><div className="text-muted">SL</div><span className="text-bear">{s.stop_loss}</span></div>
                  <div><div className="text-muted">TP</div><span className="text-bull">{s.take_profit}</span></div>
                </div>
                <p className="mt-2 text-xs text-muted line-clamp-3">{s.explanation}</p>
              </div>
            ))}
          </div>
        )}
      </Card>
    </div>
  );
}
