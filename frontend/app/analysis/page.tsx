"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Card, CardTitle, ConfidenceBar } from "@/components/ui";
import PriceChart from "@/components/PriceChart";
import clsx from "clsx";

export default function AnalysisPage() {
  const [pairs, setPairs] = useState<string[]>([]);
  const [pair, setPair] = useState("EUR/USD");
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => { (async () => {
    const p = await api<{pairs: string[]}>(`/api/market/pairs`); setPairs(p.pairs);
  })(); }, []);

  const run = async (sel: string) => {
    setLoading(true);
    try {
      const [b, q] = sel.split("/");
      setData(await api(`/api/analysis/${b}/${q}`));
    } finally { setLoading(false); }
  };
  useEffect(() => { run(pair); }, [pair]);

  const sig = data?.signal;
  const confidenceBreakdown = sig?.reasoning?.confidence_breakdown?.breakdown ?? {};
  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-semibold">AI Analysis</h1>
        <select value={pair} onChange={e => setPair(e.target.value)}
          className="bg-panel2 border border-border rounded text-sm px-2 py-1">
          {pairs.map(p => <option key={p}>{p}</option>)}
        </select>
      </div>

      <Card><PriceChart pair={pair} timeframe="1h" height={380} /></Card>

      {loading && <p className="text-xs text-muted">Analyzing multi-timeframe context…</p>}

      {data && !sig && (
        <Card>
          <CardTitle>No qualifying setup</CardTitle>
          <p className="text-sm text-muted">Regime: {data.regime}. The AI did not find enough confluence on {pair} right now. This is correct behavior — wait for higher-probability conditions.</p>
        </Card>
      )}

      {sig && (
        <>
          <Card>
            <div className="flex items-center justify-between flex-wrap gap-2">
              <div className="flex items-center gap-3">
                <span className={clsx("text-sm px-3 py-1 rounded font-bold",
                  sig.direction === "BUY" ? "bg-bull/20 text-bull" : "bg-bear/20 text-bear")}>{sig.direction}</span>
                <span className="font-mono text-lg">{sig.pair}</span>
                <span className="text-xs text-muted">{sig.market_regime}</span>
              </div>
              <div className="text-right">
                <div className="text-xs text-muted">Confidence</div>
                <div className="text-2xl font-semibold">{sig.confidence}%</div>
              </div>
            </div>
            <div className="mt-3"><ConfidenceBar value={sig.confidence} /></div>
            <div className="mt-4 grid grid-cols-2 md:grid-cols-4 gap-3 text-sm font-mono">
              <div><div className="text-xs text-muted">Entry</div>{sig.entry}</div>
              <div><div className="text-xs text-muted">Stop</div><span className="text-bear">{sig.stop_loss}</span></div>
              <div><div className="text-xs text-muted">Target</div><span className="text-bull">{sig.take_profit}</span></div>
              <div><div className="text-xs text-muted">R:R</div>1:{sig.risk_reward}</div>
            </div>
            <p className="mt-4 text-sm">{sig.explanation}</p>
          </Card>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
            {(["htf","mtf","ltf"] as const).map(tf => {
              const t = sig?.reasoning?.technical?.[tf];
              const labels = { htf: "Higher TF (4H)", mtf: "Intermediate (1H)", ltf: "Entry TF (15M)" };
              return (
                <Card key={tf}>
                  <CardTitle>{labels[tf]}</CardTitle>
                  <div className="text-sm space-y-1">
                    <Row k="Trend" v={t?.trend ?? "Unavailable"} />
                    <Row k="Momentum" v={t?.momentum ?? "Unavailable"} />
                    <Row k="RSI" v={typeof t?.rsi === "number" ? `${t.rsi.toFixed(1)} (${t.rsi_state})` : "Unavailable"} />
                    <Row k="ADX" v={typeof t?.adx === "number" ? t.adx.toFixed(1) : "Unavailable"} />
                  </div>
                </Card>
              );
            })}
          </div>

          <Card>
            <CardTitle>Confidence breakdown</CardTitle>
            {Object.keys(confidenceBreakdown).length > 0 ? (
              <div className="grid grid-cols-2 md:grid-cols-4 gap-2 text-xs font-mono">
                {Object.entries(confidenceBreakdown).map(([k, v]) => (
                  <div key={k} className="bg-panel2 px-2 py-2 rounded">
                    <div className="text-muted">{k}</div>
                    <div className="text-lg">{v as number}</div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-sm text-muted">Confidence breakdown unavailable for this signal.</p>
            )}
          </Card>
        </>
      )}
    </div>
  );
}

function Row({ k, v }: { k: string; v: React.ReactNode }) {
  return <div className="flex justify-between"><span className="text-muted">{k}</span><span className="font-mono">{v}</span></div>;
}
