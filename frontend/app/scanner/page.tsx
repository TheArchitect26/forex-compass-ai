"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Card, CardTitle } from "@/components/ui";
import clsx from "clsx";

type Heat = { pair: string; change_pct: number; price: number };

export default function ScannerPage() {
  const [heat, setHeat] = useState<Heat[]>([]);
  useEffect(() => {
    const tick = async () => setHeat((await api<{items: Heat[]}>(`/api/market/heatmap`)).items);
    tick(); const t = setInterval(tick, 15000); return () => clearInterval(t);
  }, []);
  return (
    <div className="space-y-4">
      <h1 className="text-xl font-semibold">Live Market Scanner</h1>
      <p className="text-xs text-muted">Refreshes every 15 seconds. Click a pair to view full AI analysis.</p>
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
