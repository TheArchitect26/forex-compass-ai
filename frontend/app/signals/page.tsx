"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Card, CardTitle, ConfidenceBar } from "@/components/ui";
import clsx from "clsx";

type Signal = {
  id: number; pair: string; direction: "BUY"|"SELL"|"HOLD"; confidence: number;
  entry: number; stop_loss: number; take_profit: number; risk_reward: number;
  market_regime: string; explanation: string; status: string;
  reasoning: any; created_at: string; risk_level: string; reason_summary: string;
  invalidation_price: number; data_source: string; indicators_used: string[]; strength: string;
  outcome: "pending"|"win"|"loss"|"neutral"|"expired"|"invalidated";
  estimated_cost_pips: number; net_result_pips: number;
};

export default function SignalsPage() {
  const [list, setList] = useState<Signal[]>([]);
  const [reliability, setReliability] = useState<any>(null);
  const refresh = async () => setList(await api<Signal[]>(`/api/signals`));
  useEffect(() => { refresh(); (async () => setReliability(await api(`/api/signals/reliability`)))(); }, []);
  const close = async (id: number, status: "win"|"loss") => {
    await api(`/api/signals/${id}/close`, {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ status }),
    });
    refresh();
  };
  return (
    <div className="space-y-4">
      <h1 className="text-xl font-semibold">Signals</h1>
      <p className="text-xs text-muted">Every signal includes full reasoning. Mark wins/losses to feed the AI learning loop.</p>{reliability && reliability.score < 45 && <p className="text-xs text-yellow-400">Reliability warning: engine is currently {reliability.label} ({reliability.score}).</p>}
      <div className="grid gap-3">
        {list.map(s => (
          <Card key={s.id}>
            <div className="flex items-start justify-between flex-wrap gap-2">
              <div className="flex items-center gap-3">
                <span className={clsx("text-xs px-2 py-1 rounded font-bold",
                  s.direction === "BUY" ? "bg-bull/20 text-bull" : s.direction === "SELL" ? "bg-bear/20 text-bear" : "bg-yellow-500/20 text-yellow-400")}>{s.direction}</span>
                <span className="font-mono text-lg">{s.pair}</span>
                <span className="text-xs text-muted px-2 py-0.5 bg-panel2 rounded">{s.market_regime}</span>
                <span className="text-xs px-2 py-0.5 bg-panel2 rounded">outcome: {s.outcome}</span>
                <span className="text-xs px-2 py-0.5 bg-panel2 rounded">risk: {s.risk_level}</span>
                <span className="text-xs px-2 py-0.5 bg-panel2 rounded">strength: {s.strength}</span>
                <span className="text-xs text-muted">{new Date(s.created_at).toLocaleString()}</span>
              </div>
              <div className="flex items-center gap-2">
                {s.status === "open" ? (
                  <>
                    <button onClick={() => close(s.id, "win")} className="text-xs px-3 py-1 rounded bg-bull/20 text-bull">Mark win</button>
                    <button onClick={() => close(s.id, "loss")} className="text-xs px-3 py-1 rounded bg-bear/20 text-bear">Mark loss</button>
                  </>
                ) : <span className="text-xs px-2 py-1 rounded bg-panel2 text-muted">{s.status}</span>}
              </div>
            </div>
            <div className="mt-3 grid grid-cols-2 md:grid-cols-5 gap-3 text-sm font-mono">
              <div><div className="text-xs text-muted">Entry</div>{s.entry}</div>
              <div><div className="text-xs text-muted">Stop loss</div><span className="text-bear">{s.stop_loss}</span></div>
              <div><div className="text-xs text-muted">Take profit</div><span className="text-bull">{s.take_profit}</span></div>
              <div><div className="text-xs text-muted">R:R</div>1:{s.risk_reward}</div>
              <div>
                <div className="text-xs text-muted">Confidence {s.confidence}%</div>
                <ConfidenceBar value={s.confidence} />
              </div>
            </div>
            <div className="mt-2 grid grid-cols-1 md:grid-cols-2 gap-2 text-xs">
              <div className="bg-panel2 rounded p-2"><span className="text-muted">Reason: </span>{s.reason_summary}</div>
              <div className="bg-panel2 rounded p-2"><span className="text-muted">Invalidation: </span>{s.invalidation_price}</div>
            </div>
            {s.data_source === "synthetic" && <p className="mt-2 text-xs text-yellow-400">Warning: synthetic/demo data source in use.</p>}
            <div className="mt-1 text-xs text-muted">Estimated costs: {s.estimated_cost_pips} pips • Net result: {s.net_result_pips} pips</div>
            <div className="mt-2 text-xs text-muted">Indicators used: {s.indicators_used?.join(", ")}</div>
            {s.reasoning?.confirmations && <div className="mt-2 text-xs"><span className="text-bull">Confirmations:</span> {s.reasoning.confirmations.join("; ")}</div>}
            {s.reasoning?.contradictions && <div className="mt-1 text-xs"><span className="text-bear">Contradictions:</span> {s.reasoning.contradictions.join("; ")}</div>}
            <p className="mt-3 text-sm text-muted">{s.explanation}</p>
            {s.reasoning?.confidence_breakdown && (
              <details className="mt-2">
                <summary className="text-xs text-accent cursor-pointer">Confidence breakdown</summary>
                <div className="mt-2 grid grid-cols-2 md:grid-cols-4 gap-1 text-xs font-mono">
                  {Object.entries(s.reasoning.confidence_breakdown.breakdown).map(([k,v]) => (
                    <div key={k} className="flex justify-between bg-panel2 px-2 py-1 rounded">
                      <span className="text-muted">{k}</span><span>{v as number}</span>
                    </div>
                  ))}
                </div>
              </details>
            )}
          </Card>
        ))}
        {list.length === 0 && <p className="text-sm text-muted">No signals yet — run a scan from the Dashboard.</p>}
      </div>
    </div>
  );
}
