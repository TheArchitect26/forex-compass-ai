"use client";

import { useEffect, useState } from "react";
import clsx from "clsx";
import { api } from "@/lib/api";
import { Card, CardTitle, Stat } from "@/components/ui";

type SymbolDiagnostic = {
  symbol: string;
  status: "supported" | "cached" | "unknown" | "provider_failed" | "synthetic_demo" | string;
  data_mode: string;
  provider_name: string;
  last_success: string | null;
  last_error: string | null;
  last_error_message: string | null;
};

type ProviderDiagnostics = {
  provider_name: string;
  provider_configured: boolean;
  last_success: string | null;
  last_error: string | null;
  last_error_message: string | null;
  symbols: SymbolDiagnostic[];
  auto_trade: false;
  no_execution: true;
};

function statusClass(status: string) {
  if (status === "supported") return "bg-bull/15 text-bull";
  if (status === "cached") return "bg-accent/15 text-accent";
  if (status === "provider_failed") return "bg-bear/15 text-bear";
  if (status === "synthetic_demo") return "bg-yellow-500/15 text-yellow-300";
  return "bg-panel2 text-muted";
}

export default function ProviderDiagnosticsPage() {
  const [data, setData] = useState<ProviderDiagnostics | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api<ProviderDiagnostics>("/api/signals/provider-diagnostics")
      .then((payload) => {
        setData(payload);
        setError(null);
      })
      .catch((err) => setError(err.message || "Provider diagnostics failed to load."));
  }, []);

  if (error) return <div className="text-sm text-bear">{error}</div>;
  if (!data) return <p className="text-sm text-muted">Loading...</p>;

  const failed = data.symbols.filter((item) => item.status === "provider_failed").length;
  const supported = data.symbols.filter((item) => item.status === "supported" || item.status === "cached").length;
  const unknown = data.symbols.filter((item) => item.status === "unknown").length;

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-end justify-between gap-3">
        <div>
          <h1 className="text-xl font-semibold">Provider Diagnostics</h1>
          <p className="mt-1 text-xs text-muted">Symbol-level visibility into market data provider reliability.</p>
        </div>
        <div className="rounded border border-yellow-500/30 bg-yellow-500/10 px-3 py-2 text-xs text-yellow-200">
          Diagnostics only. No execution, orders, or auto-trading.
        </div>
      </div>

      <div className="grid gap-3 md:grid-cols-4">
        <Stat label="Provider" value={data.provider_name} sub={data.provider_configured ? "configured" : "not configured"} />
        <Stat label="Supported/cached" value={supported} tone="bull" />
        <Stat label="Failed" value={failed} tone={failed ? "bear" : "neutral"} />
        <Stat label="Unknown" value={unknown} />
      </div>

      <Card>
        <CardTitle>Provider state</CardTitle>
        <div className="grid gap-2 text-xs md:grid-cols-3">
          <div>Configured: <span className="font-mono">{String(data.provider_configured)}</span></div>
          <div>Last success: <span className="font-mono">{data.last_success ? new Date(data.last_success).toLocaleString() : "n/a"}</span></div>
          <div>Last error: <span className="font-mono">{data.last_error ? new Date(data.last_error).toLocaleString() : "n/a"}</span></div>
        </div>
        {data.last_error_message && <div className="mt-2 text-xs text-bear">{data.last_error_message}</div>}
      </Card>

      <Card>
        <CardTitle>Symbol reliability</CardTitle>
        <div className="overflow-x-auto">
          <table className="w-full min-w-[760px] text-left text-xs">
            <thead className="text-muted">
              <tr>
                <th className="p-2 font-medium">Symbol</th>
                <th className="p-2 font-medium">Status</th>
                <th className="p-2 font-medium">Data mode</th>
                <th className="p-2 font-medium">Last success</th>
                <th className="p-2 font-medium">Last error</th>
                <th className="p-2 font-medium">Error detail</th>
              </tr>
            </thead>
            <tbody>
              {data.symbols.map((item) => (
                <tr key={item.symbol} className={clsx("border-t border-border", item.status === "provider_failed" && "bg-bear/5")}>
                  <td className="p-2 font-mono">{item.symbol}</td>
                  <td className="p-2">
                    <span className={clsx("rounded px-2 py-1 font-semibold", statusClass(item.status))}>{item.status}</span>
                  </td>
                  <td className="p-2 font-mono">{item.data_mode}</td>
                  <td className="p-2 text-muted">{item.last_success ? new Date(item.last_success).toLocaleString() : "n/a"}</td>
                  <td className="p-2 text-muted">{item.last_error ? new Date(item.last_error).toLocaleString() : "n/a"}</td>
                  <td className={clsx("max-w-sm p-2", item.last_error_message ? "text-bear" : "text-muted")}>{item.last_error_message || "n/a"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
}
