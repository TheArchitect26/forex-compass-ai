"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Card, CardTitle } from "@/components/ui";

export default function EvaluationPage() {
  const [status, setStatus] = useState<any>(null);
  const [bench, setBench] = useState<any>(null);
  const [reg, setReg] = useState<any>(null);
  const [plan, setPlan] = useState<any>(null);

  useEffect(() => {
    api("/api/evaluation/status").then(setStatus);
    api("/api/evaluation/benchmark", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setBench);
    api("/api/evaluation/regression-review", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setReg);
    api("/api/evaluation/improvement-plan", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setPlan);
  }, []);

  return <div className="space-y-4">
    <h1 className="text-xl font-semibold">Evaluation</h1>
    <Card><CardTitle>Maturity scores</CardTitle><div className="text-xs">Institutional: {status?.institutional_maturity_score ?? "..."} | Usability: {status?.usability_maturity_score ?? "..."} | Runtime: {status?.runtime_maturity_score ?? "..."}</div></Card>
    <Card><CardTitle>Benchmark categories</CardTitle><div className="text-xs">{bench?.benchmarks?.map((x: any) => `${x.category}:${x.current_score}`).join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Regression warnings</CardTitle><div className="text-xs">{reg?.regression_warnings?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Improvement plan</CardTitle><div className="text-xs">{plan?.plan_items?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Trend indicators</CardTitle><div className="text-xs">Sample trend: {bench?.benchmarks?.[0]?.trend ?? "..."}</div></Card>
    <Card><CardTitle>Evidence summaries</CardTitle><div className="text-xs">Evidence required: {String(reg?.evidence_required)}</div></Card>
    <Card><CardTitle>Human-review requirement</CardTitle><div className="text-xs">Evaluation changes require explicit human review and approval.</div></Card>
    <Card><CardTitle>Safety boundary</CardTitle><p className="text-xs text-muted">Evaluation is advisory-only. No auto-approval, no auto-strategy rewrite, no hidden regressions, and no trade execution.</p></Card>
  </div>;
}
