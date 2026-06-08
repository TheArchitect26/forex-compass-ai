"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Card, CardTitle } from "@/components/ui";
import clsx from "clsx";

type Heat = { pair: string; change_pct: number; price: number };
type SignalStatus = {
  pending_validation_count?: number;
  recent_accuracy?: number;
  data_mode?: string;
  last_validation_run_at?: string | null;
  last_validation_counts?: { signals_checked: number; outcomes_updated: number };
  validation?: {
    provider_backed?: { validated: number; pending: number; win_rate: number; loss_rate: number };
    synthetic_demo?: { total: number; pending: number; win_rate: number };
  };
};
type ScanSummary = {
  data_mode: string;
  real_count: number;
  cached_count: number;
  synthetic_demo_count: number;
  unavailable_count: number;
  provider_failed_symbols: string[];
  skipped_unavailable_symbols?: string[];
  requested_symbols?: string[];
  scanned_symbols?: string[];
};
type ProviderDiagnostics = {
  recommended_symbols: string[];
  unavailable_symbols: string[];
  symbol_presets: {
    forex_majors: string[];
    commodities: string[];
    experimental: string[];
    unsupported: string[];
  };
};

export default function ScannerPage() {
  const [heat, setHeat] = useState<Heat[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [warning, setWarning] = useState<string | null>(null);
  const [updatedAt, setUpdatedAt] = useState<string | null>(null);
  const [status, setStatus] = useState<SignalStatus | null>(null);
  const [scanSummary, setScanSummary] = useState<ScanSummary | null>(null);
  const [diagnostics, setDiagnostics] = useState<ProviderDiagnostics | null>(null);
  const [selectedSymbols, setSelectedSymbols] = useState<string[]>([]);
  const [retrySymbols, setRetrySymbols] = useState<string[]>([]);
  const [symbolsInitialized, setSymbolsInitialized] = useState(false);
  useEffect(() => {
    const tick = async () => {
      setLoading(true);
      try {
        const sample = await api<any>(`/api/market/ohlcv?pair=EUR/USD&timeframe=1h&limit=2`);
        setWarning(sample.warning || null);
        setStatus(await api<SignalStatus>(`/api/signals/status`));
        const providerDiagnostics = await api<ProviderDiagnostics>(`/api/signals/provider-diagnostics`);
        setDiagnostics(providerDiagnostics);
        if (!symbolsInitialized) {
          setSelectedSymbols(providerDiagnostics.recommended_symbols);
          setSymbolsInitialized(true);
        }
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
  }, [symbolsInitialized]);
  const runScan = async () => {
    const result = await api<ScanSummary>(`/api/signals/scan`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ symbols: selectedSymbols, retry_symbols: retrySymbols }),
    });
    setScanSummary(result);
    setRetrySymbols([]);
    setDiagnostics(await api<ProviderDiagnostics>(`/api/signals/provider-diagnostics`));
  };
  const toggleSymbol = (symbol: string) => {
    setSelectedSymbols((current) => current.includes(symbol) ? current.filter((item) => item !== symbol) : [...current, symbol]);
  };
  const toggleRetry = (symbol: string) => {
    setRetrySymbols((current) => current.includes(symbol) ? current.filter((item) => item !== symbol) : [...current, symbol]);
    setSelectedSymbols((current) => current.includes(symbol) ? current : [...current, symbol]);
  };
  const allPresetSymbols = diagnostics ? Array.from(new Set([
    ...diagnostics.symbol_presets.forex_majors,
    ...diagnostics.symbol_presets.commodities,
    ...diagnostics.symbol_presets.experimental,
  ])) : [];
  const unavailable = new Set(diagnostics?.unavailable_symbols || []);
  return (
    <div className="space-y-4">
      <h1 className="text-xl font-semibold">Live Market Scanner</h1>
      <p className="text-xs text-muted">Refreshes every 15 seconds. Signal Assistant mode (analysis only).</p>
      <div className="flex items-center gap-2">
        <button onClick={runScan} disabled={selectedSymbols.length === 0} className="px-3 py-1 rounded bg-accent text-bg text-xs disabled:opacity-50">Run signal scan</button>
        {status?.data_mode && <span className="text-xs text-muted">Status mode: {status.data_mode}</span>}
      </div>
      {loading && <div className="text-xs text-accent bg-panel2 border border-border rounded p-2">Loading scanner data…</div>}
      {!loading && !error && <div className="text-xs text-bull bg-bull/10 border border-bull/30 rounded p-2">Scanner updated successfully{updatedAt ? ` at ${updatedAt}` : ""}.</div>}
      {warning && <div className="text-xs text-yellow-400 bg-yellow-950/30 border border-yellow-700 rounded p-2">{warning}</div>}
      {error && <div className="text-xs text-bear bg-bear/10 border border-bear/40 rounded p-2">{error}</div>}
      {status && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-3">
          <Card>
            <CardTitle>Validation queue</CardTitle>
            <div className="text-lg font-mono">{status.pending_validation_count ?? 0}</div>
            <div className="text-xs text-muted">provider-backed pending outcomes</div>
            <div className="mt-1 text-xs text-muted">
              Last run: {status.last_validation_run_at ? new Date(status.last_validation_run_at).toLocaleString() : "not run"}
            </div>
          </Card>
          <Card>
            <CardTitle>Provider accuracy</CardTitle>
            <div className="text-lg font-mono">{status.validation?.provider_backed?.win_rate ?? status.recent_accuracy ?? 0}%</div>
            <div className="text-xs text-muted">{status.validation?.provider_backed?.validated ?? 0} validated records</div>
          </Card>
          <Card>
            <CardTitle>Demo results</CardTitle>
            <div className="text-lg font-mono">{status.validation?.synthetic_demo?.total ?? 0}</div>
            <div className="text-xs text-muted">synthetic/demo records are separated from provider stats</div>
          </Card>
          <Card>
            <CardTitle>Last validation</CardTitle>
            <div className="text-lg font-mono">{status.last_validation_counts?.outcomes_updated ?? 0}</div>
            <div className="text-xs text-muted">updates from {status.last_validation_counts?.signals_checked ?? 0} checked records</div>
          </Card>
        </div>
      )}
      {diagnostics && (
        <Card>
          <CardTitle>Provider symbol presets</CardTitle>
          <div className="grid gap-3 md:grid-cols-3">
            <div>
              <div className="text-xs text-muted mb-1">Recommended scan list</div>
              <div className="text-sm font-mono">{diagnostics.recommended_symbols.join(", ") || "n/a"}</div>
            </div>
            <div>
              <div className="text-xs text-muted mb-1">Recently failed / unavailable</div>
              <div className="text-sm font-mono text-bear">{diagnostics.unavailable_symbols.join(", ") || "none"}</div>
            </div>
            <div>
              <div className="text-xs text-muted mb-1">Selected</div>
              <div className="text-sm font-mono">{selectedSymbols.length}</div>
            </div>
          </div>
          <div className="mt-3 grid gap-2 md:grid-cols-4">
            {allPresetSymbols.map((symbol) => (
              <label key={symbol} className={clsx("flex items-center justify-between gap-2 rounded border border-border bg-panel2 px-2 py-2 text-xs", unavailable.has(symbol) && "border-bear/40 bg-bear/5")}>
                <span className="flex items-center gap-2">
                  <input type="checkbox" checked={selectedSymbols.includes(symbol)} onChange={() => toggleSymbol(symbol)} />
                  <span className="font-mono">{symbol}</span>
                </span>
                {unavailable.has(symbol) ? (
                  <button type="button" onClick={(event) => { event.preventDefault(); toggleRetry(symbol); }} className={clsx("rounded px-2 py-1", retrySymbols.includes(symbol) ? "bg-accent text-bg" : "bg-bear/15 text-bear")}>
                    {retrySymbols.includes(symbol) ? "retrying" : "retry"}
                  </button>
                ) : (
                  <span className="text-muted">ok</span>
                )}
              </label>
            ))}
          </div>
          {diagnostics.symbol_presets.unsupported.length > 0 && (
            <div className="mt-2 text-xs text-muted">Unsupported preset symbols: {diagnostics.symbol_presets.unsupported.join(", ")}</div>
          )}
        </Card>
      )}
      {scanSummary && (
        <Card>
          <CardTitle>Latest scan data mode: {scanSummary.data_mode}</CardTitle>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-2 text-xs">
            <div>Live: <span className="font-mono">{scanSummary.real_count}</span></div>
            <div>Cached: <span className="font-mono">{scanSummary.cached_count}</span></div>
            <div>Demo: <span className="font-mono">{scanSummary.synthetic_demo_count}</span></div>
            <div>Unavailable: <span className="font-mono">{scanSummary.unavailable_count}</span></div>
          </div>
          {scanSummary.provider_failed_symbols.length > 0 && (
            <div className="text-xs text-yellow-400 mt-2">
              Provider failed: {scanSummary.provider_failed_symbols.join(", ")}
            </div>
          )}
          {(scanSummary.skipped_unavailable_symbols || []).length > 0 && (
            <div className="text-xs text-bear mt-2">
              Skipped unavailable: {(scanSummary.skipped_unavailable_symbols || []).join(", ")}
            </div>
          )}
        </Card>
      )}
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
