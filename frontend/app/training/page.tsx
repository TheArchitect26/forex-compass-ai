"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Card, CardTitle, Stat } from "@/components/ui";

type PairStat = {
  symbol: string;
  validated: number;
  wins: number;
  losses: number;
  accuracy: number;
};

type TrainingStatus = {
  enabled: boolean;
  duration_days: number;
  progress_percent: number;
  run: null | {
    status: string;
    started_at: string;
    completed_at: string | null;
    last_scan_at: string | null;
    interval_minutes: number;
    symbols: string[];
    total_scans: number;
    provider_backed_signals: number;
    synthetic_skipped: number;
    unavailable_skipped: number;
  };
  statistics: {
    eligible_buy_sell: number;
    validated_buy_sell: number;
    pending_buy_sell: number;
    wins: number;
    losses: number;
    accuracy: number;
    hold_count: number;
    excluded_non_execution_grade: number;
    best_pairs: PairStat[];
    worst_pairs: PairStat[];
  };
  safety_flags: Record<string, boolean>;
};

function PairTable({ title, rows }: { title: string; rows: PairStat[] }) {
  return (
    <Card>
      <CardTitle>{title}</CardTitle>
      {rows.length === 0 ? (
        <div className="text-xs text-muted">No validated provider-backed BUY/SELL samples yet.</div>
      ) : (
        <div className="space-y-2">
          {rows.map((row) => (
            <div key={row.symbol} className="flex items-center justify-between rounded bg-panel2 px-3 py-2 text-xs">
              <span className="font-mono">{row.symbol}</span>
              <span>{row.accuracy}% from {row.validated} validated</span>
            </div>
          ))}
        </div>
      )}
    </Card>
  );
}

export default function TrainingPage() {
  const [status, setStatus] = useState<TrainingStatus | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const load = async () => {
      try {
        setStatus(await api<TrainingStatus>("/api/signals/training-status"));
        setError(null);
      } catch (e: any) {
        setError(e.message || "Training status failed to load.");
      }
    };
    load();
    const timer = setInterval(load, 30000);
    return () => clearInterval(timer);
  }, []);

  const run = status?.run;
  const stats = status?.statistics;
  return (
    <div className="space-y-4">
      <div>
        <h1 className="text-xl font-semibold">7-Day Auto Training</h1>
        <p className="mt-1 text-xs text-muted">Scheduled provider-backed signal validation only. No demo or live trades are placed.</p>
      </div>

      {error && <div className="rounded border border-bear/40 bg-bear/10 p-2 text-xs text-bear">{error}</div>}
      {status && !status.enabled && (
        <div className="rounded border border-yellow-700 bg-yellow-950/30 p-2 text-xs text-yellow-400">
          Auto training is disabled. Set AUTO_TRAINING_ENABLED=true to begin one 7-day validation run.
        </div>
      )}

      <Card>
        <CardTitle>7-day progress</CardTitle>
        <div className="mb-2 flex justify-between text-xs">
          <span>{run?.status || "not started"}</span>
          <span className="font-mono">{status?.progress_percent ?? 0}%</span>
        </div>
        <div className="h-3 overflow-hidden rounded bg-panel2">
          <div className="h-full bg-accent" style={{ width: `${status?.progress_percent ?? 0}%` }} />
        </div>
        <div className="mt-3 grid gap-2 text-xs text-muted md:grid-cols-3">
          <div>Started: {run ? new Date(run.started_at).toLocaleString() : "not started"}</div>
          <div>Last scan: {run?.last_scan_at ? new Date(run.last_scan_at).toLocaleString() : "not run"}</div>
          <div>Interval: {run?.interval_minutes ?? 30} minutes</div>
        </div>
      </Card>

      <div className="grid gap-3 md:grid-cols-4">
        <Stat label="Accuracy" value={`${stats?.accuracy ?? 0}%`} sub={`${stats?.validated_buy_sell ?? 0} validated BUY/SELL`} />
        <Stat label="Provider signals" value={run?.provider_backed_signals ?? 0} sub={`${run?.total_scans ?? 0} scheduled scans`} />
        <Stat label="Pending BUY/SELL" value={stats?.pending_buy_sell ?? 0} sub={`${stats?.eligible_buy_sell ?? 0} eligible samples`} />
        <Stat label="HOLD separate" value={stats?.hold_count ?? 0} sub="excluded from BUY/SELL win-rate" />
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <PairTable title="Best pairs" rows={stats?.best_pairs ?? []} />
        <PairTable title="Worst pairs" rows={stats?.worst_pairs ?? []} />
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <CardTitle>Skipped records</CardTitle>
          <div className="space-y-2 text-xs">
            <div className="flex justify-between"><span>Synthetic/demo</span><span className="font-mono">{run?.synthetic_skipped ?? 0}</span></div>
            <div className="flex justify-between"><span>Unavailable</span><span className="font-mono">{run?.unavailable_skipped ?? 0}</span></div>
            <div className="flex justify-between"><span>Execution grade false</span><span className="font-mono">{stats?.excluded_non_execution_grade ?? 0}</span></div>
          </div>
        </Card>
        <Card>
          <CardTitle>Safety flags</CardTitle>
          <div className="grid gap-2 text-xs md:grid-cols-2">
            {Object.entries(status?.safety_flags ?? {}).map(([key, value]) => (
              <div key={key} className="flex justify-between rounded bg-panel2 px-2 py-1">
                <span>{key.replaceAll("_", " ")}</span>
                <span className={value ? "text-bull" : "text-bear"}>{String(value)}</span>
              </div>
            ))}
          </div>
        </Card>
      </div>

      {run && <Card><CardTitle>Training symbols</CardTitle><div className="text-xs font-mono">{run.symbols.join(", ")}</div></Card>}
    </div>
  );
}
