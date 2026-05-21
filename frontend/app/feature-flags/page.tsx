"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Card, CardTitle } from "@/components/ui";

export default function FeatureFlagsPage() {
  const [status, setStatus] = useState<any>(null);
  const [audit, setAudit] = useState<any>(null);
  const [stale, setStale] = useState<any>(null);
  const [plan, setPlan] = useState<any>(null);
  const [safety, setSafety] = useState<any>(null);

  useEffect(() => {
    api("/api/feature-flags/status").then(setStatus);
    api("/api/feature-flags/audit", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setAudit);
    api("/api/feature-flags/stale-review", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setStale);
    api("/api/feature-flags/cleanup-plan", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setPlan);
    api("/api/feature-flags/rollout-safety", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setSafety);
  }, []);

  return <div className="space-y-4">
    <h1 className="text-xl font-semibold">Feature Flags</h1>
    <Card><CardTitle>Flag hygiene scores</CardTitle><div className="text-xs">Hygiene: {status?.flag_hygiene_score ?? "..."} | Lifecycle clarity: {status?.lifecycle_clarity_score ?? "..."} | Ownership clarity: {status?.ownership_clarity_score ?? "..."}</div></Card>
    <Card><CardTitle>Operator confusion risk</CardTitle><div className="text-xs">Operator confusion risk: {status?.operator_confusion_risk_score ?? "..."} | Complexity risk: {status?.complexity_risk_score ?? "..."}</div></Card>
    <Card><CardTitle>Registry items</CardTitle><div className="text-xs">{audit?.registry?.map((r: any) => `${r.flag_name} (${r.lifecycle_state}, owner: ${r.owner})`).join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Stale flags</CardTitle><div className="text-xs">No owner: {stale?.flags_with_no_owner?.join(" | ") ?? "..."} | Over lifespan: {stale?.flags_older_than_intended_lifespan?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Cleanup plan</CardTitle><div className="text-xs">Actions: {plan?.cleanup_actions?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Rollout safety</CardTitle><div className="text-xs">Blast radius: {safety?.blast_radius ?? "..."} | Rollback usefulness: {safety?.rollback_usefulness ?? "..."} | Monitoring readiness: {safety?.monitoring_readiness ?? "..."}</div></Card>
    <Card><CardTitle>Safety boundary</CardTitle><p className="text-xs text-muted">Feature flag governance is advisory-only and no-execution. No auto-enable, no auto-disable, no auto-delete, no auto-rollout state change, and no auto-production behavior change.</p></Card>
  </div>;
}
