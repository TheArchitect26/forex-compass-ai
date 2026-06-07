"use client";

import { useEffect, useMemo, useState } from "react";
import clsx from "clsx";
import { api } from "@/lib/api";
import { Card, CardTitle, Stat } from "@/components/ui";

type DataMode = "provider" | "live" | "cached" | "synthetic_demo" | "unavailable" | string;
type Direction = "BUY" | "SELL" | "HOLD" | string;

type ReviewSignal = {
  signal_id: number;
  symbol: string;
  interval: string;
  direction: Direction;
  confidence: number;
  entry_price: number;
  timestamp: string;
  data_mode: DataMode;
  provider_name: string;
  demo_only: boolean;
  execution_grade: "validation_candidate" | "review_only" | string;
  validation_status: string;
  outcome: string;
  outcome_notes: string;
  created_at: string;
  auto_trade: false;
  no_execution: true;
  advisory_only: true;
};

type ReviewResponse = {
  items: ReviewSignal[];
  summary: {
    total: number;
    provider_backed: number;
    demo_only: number;
    unavailable: number;
    pending: number;
    skipped_hold: number;
    wins: number;
    losses: number;
  };
  auto_trade: false;
  no_execution: true;
  advisory_only: true;
};

function modeLabel(mode: DataMode) {
  if (mode === "provider" || mode === "live") return "Provider-backed";
  if (mode === "cached") return "Cached";
  if (mode === "synthetic_demo") return "Synthetic demo";
  if (mode === "unavailable") return "Unavailable";
  return mode;
}

function modeClass(mode: DataMode) {
  if (mode === "provider" || mode === "live") return "bg-bull/15 text-bull";
  if (mode === "cached") return "bg-accent/15 text-accent";
  if (mode === "synthetic_demo") return "bg-yellow-500/15 text-yellow-300";
  if (mode === "unavailable") return "bg-bear/15 text-bear";
  return "bg-panel2 text-muted";
}

function DirectionBadge({ direction }: { direction: Direction }) {
  return (
    <span
      className={clsx(
        "inline-flex w-12 justify-center rounded px-2 py-1 text-[11px] font-bold",
        direction === "BUY" && "bg-bull/15 text-bull",
        direction === "SELL" && "bg-bear/15 text-bear",
        direction === "HOLD" && "bg-yellow-500/15 text-yellow-300",
      )}
    >
      {direction}
    </span>
  );
}

function ModeBadge({ mode }: { mode: DataMode }) {
  return (
    <span className={clsx("inline-flex min-w-28 justify-center rounded px-2 py-1 text-[11px] font-semibold", modeClass(mode))}>
      {modeLabel(mode)}
    </span>
  );
}

export default function SignalReviewPage() {
  const [data, setData] = useState<ReviewResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [symbol, setSymbol] = useState("");
  const [interval, setInterval] = useState("");
  const [direction, setDirection] = useState("");
  const [validationStatus, setValidationStatus] = useState("");
  const [dataMode, setDataMode] = useState("");
  const [demoOnly, setDemoOnly] = useState("");

  const query = useMemo(() => {
    const params = new URLSearchParams({ limit: "100" });
    if (symbol) params.set("symbol", symbol);
    if (interval) params.set("interval", interval);
    if (direction) params.set("direction", direction);
    if (validationStatus) params.set("validation_status", validationStatus);
    if (dataMode) params.set("data_mode", dataMode);
    if (demoOnly) params.set("demo_only", demoOnly);
    return params.toString();
  }, [symbol, interval, direction, validationStatus, dataMode, demoOnly]);

  useEffect(() => {
    api<ReviewResponse>(`/api/signals/review?${query}`)
      .then((payload) => {
        setData(payload);
        setError(null);
      })
      .catch((err) => setError(err.message || "Signal review failed to load."));
  }, [query]);

  if (error) return <div className="text-sm text-bear">{error}</div>;
  if (!data) return <p className="text-sm text-muted">Loading...</p>;

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-end justify-between gap-3">
        <div>
          <h1 className="text-xl font-semibold">Signal Review</h1>
          <p className="mt-1 text-xs text-muted">Stored scan contexts and validation outcomes.</p>
        </div>
        <div className="rounded border border-yellow-500/30 bg-yellow-500/10 px-3 py-2 text-xs text-yellow-200">
          Advisory-only. No execution, broker orders, or auto-trading.
        </div>
      </div>

      <div className="grid gap-3 md:grid-cols-4">
        <Stat label="Total" value={data.summary.total} />
        <Stat label="Provider-backed" value={data.summary.provider_backed} tone="bull" />
        <Stat label="Demo only" value={data.summary.demo_only} />
        <Stat label="Unavailable" value={data.summary.unavailable} tone="bear" />
      </div>

      <div className="grid gap-3 md:grid-cols-4">
        <Stat label="Pending" value={data.summary.pending} />
        <Stat label="Skipped HOLD" value={data.summary.skipped_hold} />
        <Stat label="Wins" value={data.summary.wins} tone="bull" />
        <Stat label="Losses" value={data.summary.losses} tone="bear" />
      </div>

      <Card>
        <CardTitle>Filters</CardTitle>
        <div className="grid gap-2 text-xs md:grid-cols-6">
          <input className="rounded border border-border bg-panel2 px-2 py-2" placeholder="Symbol" value={symbol} onChange={(event) => setSymbol(event.target.value)} />
          <input className="rounded border border-border bg-panel2 px-2 py-2" placeholder="Interval" value={interval} onChange={(event) => setInterval(event.target.value)} />
          <select className="rounded border border-border bg-panel2 px-2 py-2" value={direction} onChange={(event) => setDirection(event.target.value)}>
            <option value="">Any direction</option>
            <option value="BUY">BUY</option>
            <option value="SELL">SELL</option>
            <option value="HOLD">HOLD</option>
          </select>
          <select className="rounded border border-border bg-panel2 px-2 py-2" value={validationStatus} onChange={(event) => setValidationStatus(event.target.value)}>
            <option value="">Any status</option>
            <option value="pending">Pending</option>
            <option value="validated">Validated</option>
            <option value="skipped_demo">Skipped demo</option>
            <option value="skipped_hold">Skipped HOLD</option>
          </select>
          <select className="rounded border border-border bg-panel2 px-2 py-2" value={dataMode} onChange={(event) => setDataMode(event.target.value)}>
            <option value="">Any data mode</option>
            <option value="provider">Provider-backed</option>
            <option value="cached">Cached</option>
            <option value="synthetic_demo">Synthetic demo</option>
            <option value="unavailable">Unavailable</option>
          </select>
          <select className="rounded border border-border bg-panel2 px-2 py-2" value={demoOnly} onChange={(event) => setDemoOnly(event.target.value)}>
            <option value="">Demo filter</option>
            <option value="true">Demo only</option>
            <option value="false">Provider/cache/unavailable</option>
          </select>
        </div>
      </Card>

      <Card>
        <CardTitle>Recent stored signals</CardTitle>
        <div className="overflow-x-auto">
          <table className="w-full min-w-[980px] text-left text-xs">
            <thead className="text-muted">
              <tr>
                <th className="p-2 font-medium">Created</th>
                <th className="p-2 font-medium">Signal</th>
                <th className="p-2 font-medium">Data</th>
                <th className="p-2 font-medium">Confidence</th>
                <th className="p-2 font-medium">Entry</th>
                <th className="p-2 font-medium">Review state</th>
                <th className="p-2 font-medium">Outcome</th>
                <th className="p-2 font-medium">Notes</th>
              </tr>
            </thead>
            <tbody>
              {data.items.map((signal) => (
                <tr key={signal.signal_id} className="border-t border-border align-top">
                  <td className="p-2 text-muted">{new Date(signal.created_at).toLocaleString()}</td>
                  <td className="p-2">
                    <div className="flex items-center gap-2">
                      <DirectionBadge direction={signal.direction} />
                      <span className="font-mono">{signal.symbol}</span>
                      <span className="text-muted">{signal.interval}</span>
                    </div>
                  </td>
                  <td className="p-2">
                    <ModeBadge mode={signal.data_mode} />
                    <div className="mt-1 text-[11px] text-muted">{signal.provider_name || "No provider"}</div>
                  </td>
                  <td className="p-2 font-mono">{signal.confidence}%</td>
                  <td className="p-2 font-mono">{signal.entry_price}</td>
                  <td className="p-2">
                    <div className="font-medium">{signal.execution_grade === "review_only" ? "Review-only" : "Validation candidate"}</div>
                    <div className="text-[11px] text-muted">{signal.validation_status}</div>
                  </td>
                  <td className="p-2">
                    <span className={clsx("rounded bg-panel2 px-2 py-1 font-mono", signal.outcome === "win" && "text-bull", signal.outcome === "loss" && "text-bear")}>
                      {signal.outcome}
                    </span>
                  </td>
                  <td className="max-w-sm p-2 text-muted">{signal.outcome_notes}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        {data.items.length === 0 && <p className="mt-3 text-sm text-muted">No stored signals match the current filters.</p>}
      </Card>
    </div>
  );
}
