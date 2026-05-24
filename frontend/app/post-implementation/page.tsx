"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Card, CardTitle } from "@/components/ui";

export default function PostImplementationPage() {
  const [status, setStatus] = useState<any>(null);
  const [pir, setPir] = useState<any>(null);
  const [comparison, setComparison] = useState<any>(null);
  const [lessons, setLessons] = useState<any>(null);
  const [actions, setActions] = useState<any>(null);

  useEffect(() => {
    api("/api/post-implementation/status").then(setStatus);
    api("/api/post-implementation/review", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setPir);
    api("/api/post-implementation/expected-vs-actual", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setComparison);
    api("/api/post-implementation/lessons-learned", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setLessons);
    api("/api/post-implementation/improvement-actions", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setActions);
  }, []);

  return <div className="space-y-4">
    <h1 className="text-xl font-semibold">Post-Implementation</h1>
    <Card><CardTitle>PIR summary</CardTitle><div className="text-xs">Summary: {pir?.change_summary ?? "..."} | Planned: {pir?.planned_outcome ?? "..."} | Actual: {pir?.actual_outcome ?? "..."}</div></Card>
    <Card><CardTitle>Expected vs actual comparison</CardTitle><div className="text-xs">Systems alignment: {comparison?.predicted_vs_actual_affected_systems ?? "..."} | Risk delta: {comparison?.expected_vs_actual_risk ?? "..."}</div></Card>
    <Card><CardTitle>Implementation score</CardTitle><div className="text-xs">Success: {status?.implementation_success_score ?? "..."} | Alignment: {status?.expected_vs_actual_alignment_score ?? "..."}</div></Card>
    <Card><CardTitle>Deviations</CardTitle><div className="text-xs">{pir?.deviations?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Lessons learned</CardTitle><div className="text-xs">{lessons?.golden_paths_lessons?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Improvement actions</CardTitle><div className="text-xs">{actions?.actions?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Affected systems</CardTitle><div className="text-xs">{pir?.affected_systems?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Rollback outcome</CardTitle><div className="text-xs">Rollback status: {pir?.rollback_status ?? "..."}</div></Card>
    <Card><CardTitle>Safety boundary</CardTitle><p className="text-xs text-muted">Post-implementation review is advisory-only and no-execution. No history rewrites, no auto-close actions, no auto-scorecard or golden-path changes, and no deploy/rollback execution.</p></Card>
  </div>;
}
