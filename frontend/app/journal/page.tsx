"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Card, CardTitle, Stat } from "@/components/ui";

type Entry = {
  id: number; pair: string; direction: string; entry: number; exit: number|null;
  size: number; pnl: number|null; result: string|null; notes: string; created_at: string;
};

export default function JournalPage() {
  const [list, setList] = useState<Entry[]>([]);
  const [form, setForm] = useState({ pair: "EUR/USD", direction: "BUY", entry: 0, exit: 0, size: 0.1, pnl: 0, result: "win", notes: "" });
  const refresh = async () => setList(await api<Entry[]>(`/api/journal`));
  useEffect(() => { refresh(); }, []);
  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    await api(`/api/journal`, {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ...form, entry: +form.entry, exit: +form.exit, size: +form.size, pnl: +form.pnl }),
    });
    refresh();
  };
  const wins = list.filter(e => e.result === "win").length;
  const total = list.length;
  const pnl = list.reduce((a, e) => a + (e.pnl || 0), 0);
  return (
    <div className="space-y-4">
      <h1 className="text-xl font-semibold">Trade Journal</h1>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        <Stat label="Trades logged" value={total} />
        <Stat label="Win rate" value={total ? `${Math.round(wins/total*100)}%` : "—"} tone={total && wins/total > 0.5 ? "bull" : "neutral"} />
        <Stat label="Total PnL" value={pnl.toFixed(2)} tone={pnl >= 0 ? "bull" : "bear"} />
        <Stat label="Wins" value={wins} />
      </div>

      <Card>
        <CardTitle>Log a trade</CardTitle>
        <form onSubmit={submit} className="grid grid-cols-2 md:grid-cols-4 gap-2 text-sm">
          {[
            ["pair","Pair","text"],["direction","Direction","text"],["entry","Entry","number"],
            ["exit","Exit","number"],["size","Size (lots)","number"],["pnl","PnL","number"],
            ["result","Result (win/loss/be)","text"],
          ].map(([k,l,t]) => (
            <label key={k} className="flex flex-col text-xs text-muted">
              {l}
              <input className="bg-panel2 border border-border rounded px-2 py-1 text-text mt-1"
                type={t as any} value={(form as any)[k]}
                onChange={e => setForm({ ...form, [k]: e.target.value })} />
            </label>
          ))}
          <label className="col-span-2 md:col-span-4 flex flex-col text-xs text-muted">
            Notes
            <textarea className="bg-panel2 border border-border rounded px-2 py-1 text-text mt-1" rows={2}
              value={form.notes} onChange={e => setForm({ ...form, notes: e.target.value })} />
          </label>
          <button className="col-span-2 md:col-span-4 px-4 py-2 bg-accent text-bg rounded font-medium">Add entry</button>
        </form>
      </Card>

      <Card>
        <CardTitle>History</CardTitle>
        <div className="overflow-x-auto">
          <table className="w-full text-sm font-mono">
            <thead className="text-xs text-muted">
              <tr><th className="text-left p-2">When</th><th className="text-left p-2">Pair</th><th>Dir</th><th>Entry</th><th>Exit</th><th>Size</th><th>PnL</th><th>Result</th></tr>
            </thead>
            <tbody>
              {list.map(e => (
                <tr key={e.id} className="border-t border-border">
                  <td className="p-2 text-xs">{new Date(e.created_at).toLocaleString()}</td>
                  <td className="p-2">{e.pair}</td><td className="text-center">{e.direction}</td>
                  <td className="text-center">{e.entry}</td><td className="text-center">{e.exit ?? "—"}</td>
                  <td className="text-center">{e.size}</td>
                  <td className={"text-center " + ((e.pnl ?? 0) >= 0 ? "text-bull" : "text-bear")}>{e.pnl ?? "—"}</td>
                  <td className="text-center">{e.result ?? "—"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
}
