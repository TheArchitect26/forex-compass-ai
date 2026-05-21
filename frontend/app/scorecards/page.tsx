"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Card, CardTitle } from "@/components/ui";

export default function ScorecardsPage() {
  const [status, setStatus] = useState<any>(null);
  const [evaluation, setEvaluation] = useState<any>(null);
  const [entity, setEntity] = useState<any>(null);
  const [gates, setGates] = useState<any>(null);
  const [plan, setPlan] = useState<any>(null);

  useEffect(() => {
    api("/api/scorecards/status").then(setStatus);
    api("/api/scorecards/evaluate", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setEvaluation);
    api("/api/scorecards/entity-scorecard", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setEntity);
    api("/api/scorecards/readiness-gates", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setGates);
    api("/api/scorecards/improvement-plan", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setPlan);
  }, []);

  return <div className="space-y-4">
    <h1 className="text-xl font-semibold">Scorecards</h1>
    <Card><CardTitle>Scorecard overview</CardTitle><div className="text-xs">Overall: {status?.overall_score ?? "..."} | Readiness: {status?.readiness_level ?? "..."} | Pass/Fail: {status?.pass_fail_status ?? "..."}</div></Card>
    <Card><CardTitle>Readiness gate results</CardTitle><div className="text-xs">Missing tests: {gates?.missing_tests?.join(" | ") ?? "..."} | Missing docs: {gates?.missing_documentation?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Entity-level scorecards</CardTitle><div className="text-xs">Entity: {entity?.entity_name ?? "..."} | Owner present: {String(entity?.scorecard?.owner_present)} | Tests present: {String(entity?.scorecard?.tests_present)}</div></Card>
    <Card><CardTitle>Failed checks</CardTitle><div className="text-xs">Unregistered router: {gates?.unregistered_router?.join(" | ") ?? "..."} | Orphan frontend: {gates?.orphaned_frontend_console?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Improvement plan</CardTitle><div className="text-xs">{plan?.improvements?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Evidence summaries</CardTitle><div className="text-xs">Evidence strength: {evaluation?.evidence_strength ?? "..."} | Gap severity: {evaluation?.gap_severity ?? "..."} | Priority: {evaluation?.improvement_priority ?? "..."}</div></Card>
    <Card><CardTitle>Safety boundary</CardTitle><p className="text-xs text-muted">Scorecard governance is advisory-only and no-execution. No auto-pass, no auto-lifecycle changes, no auto-create files, no auto-register routers, and no auto-run migrations.</p></Card>
  </div>;
}
