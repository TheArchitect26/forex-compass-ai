"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Card, CardTitle } from "@/components/ui";

export default function GoldenPathsPage() {
  const [status, setStatus] = useState<any>(null);
  const [flow, setFlow] = useState<any>(null);
  const [list, setList] = useState<any>(null);
  const [validation, setValidation] = useState<any>(null);
  const [deviation, setDeviation] = useState<any>(null);

  useEffect(() => {
    api("/api/golden-paths/status").then(setStatus);
    api("/api/golden-paths/workflow", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setFlow);
    api("/api/golden-paths/checklist", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setList);
    api("/api/golden-paths/validate-plan", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setValidation);
    api("/api/golden-paths/deviation-review", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setDeviation);
  }, []);

  return <div className="space-y-4">
    <h1 className="text-xl font-semibold">Golden Paths</h1>
    <Card><CardTitle>Workflow generator</CardTitle><div className="text-xs">Workflow: {flow?.workflow_name ?? "..."} | Steps: {flow?.guided_steps?.join(" -> ") ?? "..."}</div></Card>
    <Card><CardTitle>Checklist output</CardTitle><div className="text-xs">Required files: {list?.required_files?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Validation readiness</CardTitle><div className="text-xs">Readiness: {validation?.validation_readiness ?? "..."} | Scorecard: {validation?.scorecard_alignment ?? "..."}</div></Card>
    <Card><CardTitle>Deviation review</CardTitle><div className="text-xs">Reason: {deviation?.deviation_reason ?? "..."} | Risk: {deviation?.risk_introduced ?? "..."}</div></Card>
    <Card><CardTitle>Required commands</CardTitle><div className="text-xs">{list?.validation_commands?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Rollback notes</CardTitle><div className="text-xs">{list?.rollback_notes ?? "..."}</div></Card>
    <Card><CardTitle>Scorecard requirements</CardTitle><div className="text-xs">{list?.scorecard_checks?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Safety boundary</CardTitle><p className="text-xs text-muted">Golden-path workflows are advisory-only and no-execution. No auto-create files, no auto-run commands, no auto-commit, no auto-router registration, and no auto-migrations.</p></Card>
  </div>;
}
