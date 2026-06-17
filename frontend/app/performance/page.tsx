"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Card, CardTitle, Stat } from "@/components/ui";

export default function PerformancePage() {
  const [data, setData] = useState<any>(null);
  const [runs, setRuns] = useState<any[]>([]);
  const [cal, setCal] = useState<any>(null);
  const [rel, setRel] = useState<any>(null);
  const [regimePerf, setRegimePerf] = useState<any>(null);
  const [relHist, setRelHist] = useState<any[]>([]);
  const [replayResult, setReplayResult] = useState<any>(null);
  const [maint, setMaint] = useState<any>(null);
  const [versions, setVersions] = useState<any>(null);
  const [experiments, setExperiments] = useState<any[]>([]);
  const [integrity, setIntegrity] = useState<any>(null);
  const [pair, setPair] = useState("");
  const [timeframe, setTimeframe] = useState("");
  const [includeSynthetic, setIncludeSynthetic] = useState(false);
  const [actionError, setActionError] = useState<string | null>(null);
  const [validating, setValidating] = useState(false);
  const [replaying, setReplaying] = useState(false);

  const load = async () => {
    const q = `?include_synthetic=${includeSynthetic}&pair=${encodeURIComponent(pair)}&timeframe=${encodeURIComponent(timeframe)}`;
    setData(await api(`/api/signals/performance${q}`));
    setRuns(await api(`/api/signals/validation-runs`));
    setCal(await api(`/api/signals/calibration`));
    setRel(await api(`/api/signals/reliability`));
    setRegimePerf(await api(`/api/signals/regime-performance`));
    const rh = await api(`/api/signals/reliability-history`); setRelHist(rh.items || []);
    setMaint(await api(`/api/schema-version`));
    setVersions(await api(`/api/versions`));
    const ex = await api(`/api/experiments`); setExperiments(ex.items || []);
    setIntegrity(await api(`/api/data/integrity`));
  };

  useEffect(() => {
    load().catch((error) => {
      setActionError(error instanceof Error ? error.message : "Failed to load performance data.");
    });
  }, [pair, timeframe, includeSynthetic]);

  const validateNow = async () => {
    setValidating(true);
    setActionError(null);
    try {
      await api(`/api/signals/validate-outcomes`, { method: "POST" });
      await load();
    } catch (error) {
      setActionError(error instanceof Error ? error.message : "Validation failed.");
    } finally {
      setValidating(false);
    }
  };

  const replayNow = async () => {
    setReplaying(true);
    setActionError(null);
    try {
      const payload = {
        experiment_id: `exp-${Date.now()}`,
        name: "Sandbox Replay",
        target_logic_area: "weighting",
        pair: pair || "EUR/USD",
        timeframe: timeframe || "1h",
        strategy_profile: "intraday",
      };
      const out = await api(`/api/experiments/run-replay`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      setReplayResult(out);
      await load();
    } catch (error) {
      setActionError(error instanceof Error ? error.message : "Replay failed.");
    } finally {
      setReplaying(false);
    }
  };

  if (!data) return <p className="text-sm text-muted">Loading…</p>;
  const latest = runs[0];

  return (
    <div className="space-y-4">
      <h1 className="text-xl font-semibold">Signal Assistant Performance</h1>
      <div className="flex gap-2 items-center text-xs flex-wrap">
        <input className="bg-panel2 border border-border rounded px-2 py-1" placeholder="Pair (EUR/USD)" value={pair} onChange={e => setPair(e.target.value)} />
        <input className="bg-panel2 border border-border rounded px-2 py-1" placeholder="Timeframe (15min)" value={timeframe} onChange={e => setTimeframe(e.target.value)} />
        <label className="flex items-center gap-1"><input type="checkbox" checked={includeSynthetic} onChange={e => setIncludeSynthetic(e.target.checked)} /> include synthetic</label>
        <button onClick={validateNow} disabled={validating} className="px-3 py-1 rounded bg-accent text-bg disabled:opacity-50">
          {validating ? "Validating…" : "Validate outcomes now"}
        </button>
        <button onClick={replayNow} disabled={replaying} className="px-3 py-1 rounded bg-panel2 border border-border disabled:opacity-50">
          {replaying ? "Running replay…" : "Run replay"}
        </button>
      </div>
      {actionError && <div className="text-xs text-bear bg-bear/10 border border-bear/40 rounded p-2">{actionError}</div>}
      {latest && <div className="text-xs text-muted">Latest validation run: {latest.status} • checked {latest.signals_checked} • updated {latest.outcomes_updated}</div>}
      {maint && <div className="text-xs text-muted">Engine/schema: {maint.schema_version} • migrations: {(maint.migrations||[]).join(", ")}</div>}
      {versions?.active && <div className="text-xs text-muted">Active engine version: {versions.active.engine_version} / {versions.active.weighting_version}</div>}
      {integrity && <div className="text-xs text-muted">Data integrity score: {integrity.replay_dataset_integrity_score}</div>}
      {!latest && <div className="text-xs text-yellow-400">Warning: scheduler may not be active yet (no validation runs found).</div>}
      <div className="grid grid-cols-3 gap-3">
        <Stat label="Validated signals" value={data.total_signals} />
        <Stat label="Win rate (ex HOLD)" value={`${data.win_rate_excl_hold}%`} tone={data.win_rate_excl_hold >= 50 ? "bull" : "bear"} />
        <Stat label="Pending outcomes" value={data.pending_outcomes} />
      </div>
      {data.validation && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          <Stat label="Provider validated" value={data.validation.provider_backed.validated} />
          <Stat label="Provider pending" value={data.validation.provider_backed.pending} />
          <Stat label="Provider win rate" value={`${data.validation.provider_backed.win_rate}%`} tone={data.validation.provider_backed.win_rate >= 50 ? "bull" : "bear"} />
          <Stat label="Demo records" value={data.validation.synthetic_demo.total} />
        </div>
      )}
      {rel && <div className="text-xs text-muted">Reliability: <b>{rel.score}</b> ({rel.label}) {rel.sample_size < 30 ? "• warning: sample size is small" : ""} {(rel.drift_warnings||[]).length>0 ? `• drift: ${(rel.drift_warnings||[]).join("; ")}` : ""}</div>}
      <div className="text-xs text-muted">Results are estimated from candles with spread/slippage assumptions; not broker-confirmed execution.</div>
      {regimePerf && <Card><CardTitle>Regime performance</CardTitle><div className="text-xs">Best: {regimePerf.best_regime} • Worst: {regimePerf.worst_regime}</div><div className="text-xs mt-1">Sessions tracked: {Object.keys(regimePerf.by_session||{}).length}</div></Card>}
      {replayResult && <Card><CardTitle>Replay output</CardTitle><div className="text-xs">Sandbox isolated: {String(replayResult.sandbox_isolation)} • Severity: {replayResult.experiment?.comparison_results?.severity || "n/a"}</div></Card>}
      <Card><CardTitle>Experiments</CardTitle><div className="text-xs">Total: {experiments.length}</div><div className="text-xs">Latest: {experiments[0]?.name || "n/a"} ({experiments[0]?.status || "n/a"})</div></Card>
      {relHist.length>0 && <Card><CardTitle>Reliability trend data</CardTitle><div className="text-xs">Points: {relHist.length} (graph-ready endpoint)</div></Card>}
      {cal && <Card><CardTitle>Calibration</CardTitle><table className="w-full text-xs font-mono"><thead className="text-muted"><tr><th className="text-left p-1">Bucket</th><th>N</th><th>Win%</th><th>Avg net pips</th><th>Align</th></tr></thead><tbody>{cal.buckets.map((b:any)=><tr key={b.bucket} className="border-t border-border"><td className="p-1">{b.bucket}</td><td className="text-center">{b.signals_count}</td><td className="text-center">{b.win_rate}</td><td className="text-center">{b.average_net_pips}</td><td className="text-center">{b.alignment}</td></tr>)}</tbody></table></Card>}
      <Card>
        <CardTitle>Validation run history</CardTitle>
        <table className="w-full text-xs font-mono"><thead className="text-muted"><tr><th className="text-left p-1">Start</th><th>Status</th><th>Checked</th><th>Updated</th></tr></thead><tbody>
          {runs.map(r => <tr key={r.id} className="border-t border-border"><td className="p-1">{new Date(r.started_at).toLocaleString()}</td><td className="text-center">{r.status}</td><td className="text-center">{r.signals_checked}</td><td className="text-center">{r.outcomes_updated}</td></tr>)}
        </tbody></table>
      </Card>
    </div>
  );
}
