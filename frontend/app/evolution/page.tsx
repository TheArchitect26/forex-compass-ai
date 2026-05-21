"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Card, CardTitle } from "@/components/ui";

export default function EvolutionPage() {
  const [status, setStatus] = useState<any>(null);
  const [assessment, setAssessment] = useState<any>(null);
  const [readiness, setReadiness] = useState<any>(null);
  const [continuity, setContinuity] = useState<any>(null);
  const [rollback, setRollback] = useState<any>(null);

  useEffect(() => {
    api("/api/evolution/status").then(setStatus);
    api("/api/evolution/transition-assessment", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setAssessment);
    api("/api/evolution/migration-readiness", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setReadiness);
    api("/api/evolution/continuity-plan", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setContinuity);
    api("/api/evolution/rollback-plan", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setRollback);
  }, []);

  return <div className="space-y-4">
    <h1 className="text-xl font-semibold">Evolution</h1>
    <Card><CardTitle>Transition readiness</CardTitle><div className="text-xs">Readiness: {status?.transition_readiness_score ?? "..."} | Migration risk: {status?.migration_risk_score ?? "..."}</div></Card>
    <Card><CardTitle>Continuity preservation</CardTitle><div className="text-xs">Continuity: {status?.continuity_preservation_score ?? "..."} | Memory safety: {status?.institutional_memory_safety_score ?? "..."}</div></Card>
    <Card><CardTitle>Migration risks</CardTitle><div className="text-xs">{assessment?.transition_risks_detected?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Rollback readiness</CardTitle><div className="text-xs">Rollback readiness: {rollback?.rollback_readiness_score ?? "..."} | Feasibility: {rollback?.rollback_feasibility ?? "..."}</div></Card>
    <Card><CardTitle>Mission continuity</CardTitle><div className="text-xs">Mission continuity: {status?.mission_continuity_score ?? "..."} | Explainability preservation: {status?.explainability_preservation_score ?? "..."}</div></Card>
    <Card><CardTitle>Operator disruption</CardTitle><div className="text-xs">Disruption risk: {status?.operator_disruption_risk_score ?? "..."} | Review gates: {rollback?.operator_review_gates?.join(", ") ?? "..."}</div></Card>
    <Card><CardTitle>Advisory-only safety</CardTitle><p className="text-xs text-muted">Evolution governance is advisory only. No migrations, rewrites, deletions, or mission changes are auto-applied.</p></Card>
  </div>;
}
