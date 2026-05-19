"use client";
import { useEffect, useRef } from "react";
import { createChart, CandlestickSeries, ColorType, type IChartApi } from "lightweight-charts";
import { api } from "@/lib/api";

type Candle = { time: number; open: number; high: number; low: number; close: number };

export default function PriceChart({ pair, timeframe = "1h", height = 360 }:
  { pair: string; timeframe?: string; height?: number }) {
  const ref = useRef<HTMLDivElement>(null);
  useEffect(() => {
    if (!ref.current) return;
    const chart = createChart(ref.current, {
      height, layout: { background: { type: ColorType.Solid, color: "#0f1521" }, textColor: "#94a3b8" },
      grid: { vertLines: { color: "#1f2937" }, horzLines: { color: "#1f2937" } },
      timeScale: { borderColor: "#1f2937" }, rightPriceScale: { borderColor: "#1f2937" },
    });
    const series = chart.addCandlestickSeries({
      upColor: "#10b981", downColor: "#ef4444", borderVisible: false, wickUpColor: "#10b981", wickDownColor: "#ef4444",
    });
    let alive = true;
    (async () => {
      const data = await api<{ candles: Candle[] }>(`/api/market/ohlcv?pair=${encodeURIComponent(pair)}&timeframe=${timeframe}&limit=300`);
      if (!alive) return;
      series.setData(data.candles as any);
      chart.timeScale().fitContent();
    })();
    const onResize = () => chart.applyOptions({ width: ref.current!.clientWidth });
    window.addEventListener("resize", onResize); onResize();
    return () => { alive = false; window.removeEventListener("resize", onResize); chart.remove(); };
  }, [pair, timeframe, height]);
  return <div ref={ref} className="w-full" />;
}
