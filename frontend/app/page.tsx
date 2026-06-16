"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Card, CardTitle, Stat, ConfidenceBar } from "@/components/ui";
import PriceChart from "@/components/PriceChart";
import clsx from "clsx";

type Heat = { pair: string; change_pct: number; price: number };
type Health = {
  backend: string;
  database: string;
  redis: string;
  market_data_mode: "real" | "synthetic";
  twelve_data_configured: boolean;
  version: string;
};
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
  const [error, setError] = useState<string | null>(null);
  const [marketWarning, setMarketWarning] = useState<string | null>(null);
  const [health, setHealth] = useState<Health | null>(null);
  const [regime, setRegime] = useState<any>(null);
  const [profile, setProfile] = useState<any>(null);
  const [relHist, setRelHist] = useState<any[]>([]);
  const [driftWarnings, setDriftWarnings] = useState<string[]>([]);

  useEffect(() => { (async () => {
    try {
      const market = await api<any>(`/api/market/ohlcv?pair=EUR/USD&timeframe=1h&limit=3`);
      setMarketWarning(market.warning || null);
      setHealth(await api<Health>(`/api/health`));
      setHeat((await api<{items: Heat[]}>(`/api/market/heatmap`)).items);
      setRegime(await api(`/api/market/regime?pair=EUR/USD&timeframe=1h`));
      const st = await api(`/api/strategies`); setProfile(st.active);
      const rh = await api(`/api/signals/reliability-history`); setRelHist(rh.items || []);
      const rel = await api(`/api/signals/reliability`); setDriftWarnings(rel.drift_warnings || []);
      setSignals(await api<Signal[]>(`/api/signals`));
      setError(null);
    } catch (e: any) {
      setError(e.message || "Failed to load dashboard data");
    }
  })(); }, []);

  const scan = async () => {
    setScanning(true);
    setError(null);
    try {
      await api(`/api/signals/scan`, { method: "POST" });
      setSignals(await api<Signal[]>(`/api/signals`));
    } catch (e: any) {
      setError(e.message || "AI scan failed. Sign in from the Access page and try again.");
    } finally {
      setScanning(false);
    }
  };

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
      {marketWarning && <div className="text-xs text-yellow-400 bg-yellow-950/30 border border-yellow-700 rounded p-2">{marketWarning}</div>}
      {error && <div className="text-xs text-bear bg-bear/10 border border-bear/40 rounded p-2">{error}</div>}

      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        <Stat label="Active signals" value={signals.length} />
        <Stat label="Avg confidence" value={`${avgConf}%`} tone={avgConf >= 70 ? "bull" : "neutral"} />
        <Stat label="Pairs tracked" value={heat.length} />
        <Stat label="Auto-trade" value="OFF" sub="Human-in-the-loop" tone="bull" />
      </div>

      <Card>
        <CardTitle>System status</CardTitle>
        {health ? (
          <div className="grid grid-cols-2 md:grid-cols-3 gap-2 text-xs">
            <div>API: <span className={health.backend === "ok" ? "text-bull" : "text-bear"}>{health.backend === "ok" ? "Connected" : "Disconnected"}</span></div>
            <div>Database: <span className={health.database === "ok" ? "text-bull" : "text-bear"}>{health.database}</span></div>
            <div>Redis: <span className={health.redis === "ok" ? "text-bull" : "text-bear"}>{health.redis}</span></div>
            <div>Market data: <span className={health.market_data_mode === "real" ? "text-bull" : "text-yellow-400"}>{health.market_data_mode}</span></div>
            <div>Twelve Data key: <span className={health.twelve_data_configured ? "text-bull" : "text-yellow-400"}>{health.twelve_data_configured ? "configured" : "missing"}</span></div>
            <div>Version: <span className="text-muted">{health.version}</span></div>
          </div>
        ) : <p className="text-xs text-muted">Health check unavailable.</p>}
      </Card>

      <Card>
        <CardTitle>Adaptive intelligence</CardTitle>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-xs">
          <div>Current regime: <span className="text-accent">{regime?.regime || "n/a"}</span> ({regime?.confidence || 0}%)</div>
          <div>Active strategy profile: <span className="text-accent">{profile?.name || "n/a"}</span></div>
          <div>Reliability trend points: <span className="text-accent">{relHist.length}</span></div>
          <div>Adaptive engine status: <span className="text-bull">active</span></div>
        </div>
        {driftWarnings.length > 0 && <div className="mt-2 text-xs text-yellow-400">Drift warnings: {driftWarnings.join("; ")}</div>}
      </Card>

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
