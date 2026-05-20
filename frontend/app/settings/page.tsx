"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Card, CardTitle } from "@/components/ui";

export default function Settings() {
  const [active, setActive] = useState<any>(null);
  const [profiles, setProfiles] = useState<Record<string, any>>({});

  const load = async () => {
    const data = await api<any>(`/api/strategies`);
    setActive(data.active); setProfiles(data.profiles || {});
  };

  useEffect(() => { load(); }, []);

  const select = async (profile: string) => {
    await api(`/api/strategies/select`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ profile }) });
    await load();
  };

  return (
    <div className="space-y-4">
      <h1 className="text-xl font-semibold">Settings</h1>
      <Card>
        <CardTitle>Strategy Profile</CardTitle>
        <p className="text-xs text-muted mb-2">Active: <b>{active?.name || "n/a"}</b></p>
        <div className="flex flex-wrap gap-2">
          {Object.keys(profiles).map(p => (
            <button key={p} onClick={() => select(p)} className="px-2 py-1 rounded bg-panel2 border border-border text-xs">{p}</button>
          ))}
        </div>
      </Card>
      <Card>
        <CardTitle>Safety</CardTitle>
        <p className="text-sm">This system never executes trades. Every signal requires a human decision and manual execution in your broker.</p>
      </Card>
    </div>
  );
}
