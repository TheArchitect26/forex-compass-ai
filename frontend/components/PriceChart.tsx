"use client";

import { useEffect, useRef, useState } from "react";
import { createChart, ColorType } from "lightweight-charts";
import { api } from "@/lib/api";

type Candle = { time: number; open: number; high: number; low: number; close: number };

export default function PriceChart({
  pair,
  timeframe = "1h",
  height = 360,
}: {
  pair: string;
  timeframe?: string;
  height?: number;
}) {
  const ref = useRef<HTMLDivElement>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!ref.current) return;

    setError("");

    const chart = createChart(ref.current, {
      height,
      layout: {
        background: { type: ColorType.Solid, color: "#0f1521" },
        textColor: "#94a3b8",
      },
      grid: {
        vertLines: { color: "#1f2937" },
        horzLines: { color: "#1f2937" },
      },
      timeScale: { borderColor: "#1f2937" },
      rightPriceScale: { borderColor: "#1f2937" },
    });

    const series = chart.addCandlestickSeries({
      upColor: "#10b981",
      downColor: "#ef4444",
      borderVisible: false,
      wickUpColor: "#10b981",
      wickDownColor: "#ef4444",
    });

    let alive = true;

    (async () => {
      try {
        const data = await api<{ candles?: Candle[] }>(
          `/api/market/ohlcv?pair=${encodeURIComponent(pair)}&timeframe=${encodeURIComponent(timeframe)}&limit=300`
        );

        if (!alive) return;

        if (!data.candles || data.candles.length === 0) {
          setError("Chart data unavailable for this pair.");
          return;
        }

        series.setData(data.candles as any);
        chart.timeScale().fitContent();
      } catch (err) {
        if (!alive) return;
        console.error("PriceChart fetch failed", err);
        setError("Chart data unavailable. Signal engine is still running.");
      }
    })();

    const onResize = () => {
      if (ref.current) {
        chart.applyOptions({ width: ref.current.clientWidth });
      }
    };

    window.addEventListener("resize", onResize);
    onResize();

    return () => {
      alive = false;
      window.removeEventListener("resize", onResize);
      chart.remove();
    };
  }, [pair, timeframe, height]);

  return (
    <div className="w-full">
      <div ref={ref} className="w-full" />
      {error ? <div className="mt-2 text-xs text-muted">{error}</div> : null}
    </div>
  );
}
