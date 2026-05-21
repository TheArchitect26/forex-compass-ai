"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Card, CardTitle } from "@/components/ui";

export default function ResiliencePage() {
  const [status, setStatus] = useState<any>(null);
  const [scan, setScan] = useState<any>(null);
  const [plan, setPlan] = useState<any>(null);
  const [blackSwan, setBlackSwan] = useState<any>(null);
  const [recovery, setRecovery] = useState<any>(null);

  useEffect(() => {
    api("/api/resilience/status").then(setStatus);
    api("/api/resilience/crisis-scan", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setScan);
    api("/api/resilience/continuity-plan", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setPlan);
    api("/api/resilience/black-swan-review", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setBlackSwan);
    api("/api/resilience/recovery-readiness", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setRecovery);
  }, []);

  return <div className="space-y-4">
    <h1 className="text-xl font-semibold">Resilience</h1>
    <Card><CardTitle>Crisis resilience scores</CardTitle><div className="text-xs">Existential: {status?.existential_resilience_score ?? "..."} | Continuity: {status?.crisis_continuity_score ?? "..."} | Recovery: {status?.recovery_readiness_score ?? "..."}</div></Card>
    <Card><CardTitle>Black-swan warnings</CardTitle><div className="text-xs">{blackSwan?.assumptions_invalidated_by_shock?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Continuity plan</CardTitle><div className="text-xs">Crisis type: {plan?.crisis_type ?? "..."} | Preserve: {plan?.critical_systems_to_preserve?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Minimum viable institution mode</CardTitle><div className="text-xs">{plan?.minimum_viable_operating_mode?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Recovery readiness</CardTitle><div className="text-xs">Backup: {recovery?.backup_sufficiency ?? "..."} | Restart confidence: {recovery?.service_restart_confidence ?? "..."}</div></Card>
    <Card><CardTitle>Degraded-mode recommendations</CardTitle><div className="text-xs">{plan?.degraded_mode_recommendations?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Human-review requirement</CardTitle><p className="text-xs text-muted">Crisis actions require explicit human approval and coordination.</p></Card>
    <Card><CardTitle>Safety boundary</CardTitle><p className="text-xs text-muted">Resilience support is advisory-only: no auto-crisis mode, no auto-disable, no auto-recovery execution.</p></Card>
  </div>;
}
