"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Card, CardTitle } from "@/components/ui";

export default function LongevityConsolePage() {
  const [lineage, setLineage] = useState<any[]>([]);
  const [surv, setSurv] = useState<any>(null);
  const [plans, setPlans] = useState<any[]>([]);
  const [eras, setEras] = useState<any>(null);
  const [compat, setCompat] = useState<any>(null);

  useEffect(() => {
    api("/api/governance/lineage").then(setLineage);
    api("/api/governance/survivability").then((r) => setSurv(r.survivability));
    api("/api/governance/migration/plan").then((r) => setPlans(r.plans || []));
    api("/api/system/eras").then(setEras);
  }, []);

  const checkCompat = async () => {
    const out = await api("/api/governance/replay/compatibility", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ engine_version: "v_legacy", deprecated_logic: true, adapter_required: true }) });
    setCompat(out);
  };

  return <div className="space-y-4">
    <h1 className="text-xl font-semibold">Longevity Console</h1>
    <Card><CardTitle>Survivability scoring</CardTitle><div className="text-xs">Architecture: {surv?.architectural_survivability ?? "..."} | Migration safety: {surv?.migration_safety ?? "..."} | Replay compatibility: {surv?.replay_compatibility ?? "..."}</div></Card>
    <Card><CardTitle>Strategic lineage</CardTitle><div className="text-xs space-y-1">{lineage.map((l:any)=> <div key={l.id}>{l.changed_component}: {l.why}</div>)}</div></Card>
    <Card><CardTitle>Migration status</CardTitle><div className="text-xs space-y-1">{plans.map((p:any)=> <div key={p.id}>{p.target} · {p.status} · reversible: {String(p.reversible)}</div>)}</div></Card>
    <Card><CardTitle>Replay compatibility warnings</CardTitle><button className="px-2 py-1 rounded bg-accent text-bg text-xs" onClick={checkCompat}>Check compatibility</button><div className="text-xs mt-2">Mode: {compat?.compatibility_mode || "n/a"} | Warnings: {(compat?.integrity_warnings || []).join(", ") || "none"}</div></Card>
    <Card><CardTitle>Institutional-era timeline</CardTitle><div className="text-xs">Reliability eras: {(eras?.reliability_eras || []).join(", ") || "none"}</div></Card>
    <Card><CardTitle>Safety</CardTitle><p className="text-xs text-muted">Human oversight remains mandatory. No autonomous authority, no self-authorized strategic evolution.</p></Card>
  </div>;
}
