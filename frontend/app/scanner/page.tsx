"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Card, CardTitle } from "@/components/ui";
import clsx from "clsx";

type Heat = { pair: string; change_pct: number; price: number };

export default function ScannerPage() {
  const [heat, setHeat] = useState<Heat[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [warning, setWarning] = useState<string | null>(null);
  const [updatedAt, setUpdatedAt] = useState<string | null>(null);
  useEffect(() => {
    const tick = async () => {
      setLoading(true);
      try {
        const sample = await api<any>(`/api/market/ohlcv?pair=EUR/USD&timeframe=1h&limit=2`);
        setWarning(sample.warning || null);
        setHeat((await api<{items: Heat[]}>(`/api/market/heatmap`)).items);
        setUpdatedAt(new Date().toLocaleTimeString());
        setError(null);
      } catch (e: any) {
        setError(e.message || "Scanner failed to load.");
      } finally {
        setLoading(false);
      }
    };
    tick(); const t = setInterval(tick, 15000); return () => clearInterval(t);
  }, []);
  return (
    <div className="space-y-4">
      <h1 className="text-xl font-semibold">Live Market Scanner</h1>
      <p className="text-xs text-muted">Refreshes every 15 seconds. Signal Assistant mode (analysis only).</p>
      {loading && <div className="text-xs text-accent bg-panel2 border border-border rounded p-2">Loading scanner data…</div>}
      {!loading && !error && <div className="text-xs text-bull bg-bull/10 border border-bull/30 rounded p-2">Scanner updated successfully{updatedAt ? ` at ${updatedAt}` : ""}.</div>}
      {warning && <div className="text-xs text-yellow-400 bg-yellow-950/30 border border-yellow-700 rounded p-2">{warning}</div>}
      {error && <div className="text-xs text-bear bg-bear/10 border border-bear/40 rounded p-2">{error}</div>}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        {heat.map(h => (
          <Card key={h.pair} className={clsx("border-l-4",
            h.change_pct >= 0 ? "border-l-bull" : "border-l-bear")}>
            <div className="flex justify-between items-baseline">
              <span className="font-mono text-lg">{h.pair}</span>
              <span className={clsx("font-mono text-sm",
                h.change_pct >= 0 ? "text-bull" : "text-bear")}>
                {h.change_pct >= 0 ? "+" : ""}{h.change_pct.toFixed(2)}%
              </span>
            </div>
            <div className="text-xs text-muted font-mono">{h.price.toFixed(5)}</div>
          </Card>
        ))}
      </div>
    </div>
  );
}
