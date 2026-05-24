"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Card, CardTitle } from "@/components/ui";

export default function EvolutionControlPage() {
  const [status, setStatus] = useState<any>(null);
  const [audit, setAudit] = useState<any>(null);
  const [retire, setRetire] = useState<any>(null);
  const [plan, setPlan] = useState<any>(null);

  useEffect(() => {
    api("/api/evolution-control/status").then(setStatus);
    api("/api/evolution-control/capability-audit", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setAudit);
    api("/api/evolution-control/retirement-candidates", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setRetire);
    api("/api/evolution-control/evolution-plan", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setPlan);
  }, []);

  return <div className="space-y-4">
    <h1 className="text-xl font-semibold">Evolution Control</h1>
    <Card><CardTitle>Capability lifecycle map</CardTitle><div className="text-xs">States: {status?.lifecycle_states?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Retirement candidates</CardTitle><div className="text-xs">{retire?.unused_or_low_value_consoles?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Consolidation candidates</CardTitle><div className="text-xs">{retire?.better_grouped_under_control_plane?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Freeze recommendations</CardTitle><div className="text-xs">{plan?.what_to_freeze?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Evolution plan</CardTitle><div className="text-xs">Evolve: {plan?.what_to_evolve_next?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Operator-value evidence</CardTitle><div className="text-xs">{audit?.capability_audit?.[0]?.value_evidence ?? "..."}</div></Card>
    <Card><CardTitle>Maintenance burden</CardTitle><div className="text-xs">{audit?.capability_audit?.[0]?.maintenance_burden ?? "..."}</div></Card>
    <Card><CardTitle>Safety boundary</CardTitle><p className="text-xs text-muted">Evolution Control is advisory-only. No auto-delete, no auto-retire, no auto-freeze, no auto-route removal, and no trade execution.</p></Card>
  </div>;
}
