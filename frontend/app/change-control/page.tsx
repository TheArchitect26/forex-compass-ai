"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Card, CardTitle } from "@/components/ui";

export default function ChangeControlPage() {
  const [status, setStatus] = useState<any>(null);
  const [impact, setImpact] = useState<any>(null);
  const [reviews, setReviews] = useState<any>(null);
  const [rollback, setRollback] = useState<any>(null);
  const [brief, setBrief] = useState<any>(null);

  useEffect(() => {
    api("/api/change-control/status").then(setStatus);
    api("/api/change-control/impact-analysis", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setImpact);
    api("/api/change-control/review-requirements", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setReviews);
    api("/api/change-control/rollback-readiness", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setRollback);
    api("/api/change-control/approval-brief", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setBrief);
  }, []);

  return <div className="space-y-4">
    <h1 className="text-xl font-semibold">Change Control</h1>
    <Card><CardTitle>Impact score</CardTitle><div className="text-xs">Impact: {status?.change_impact_score ?? "..."} | Implementation risk: {status?.implementation_risk_score ?? "..."} | Dependency risk: {status?.dependency_risk_score ?? "..."}</div></Card>
    <Card><CardTitle>Affected systems</CardTitle><div className="text-xs">{impact?.affected_systems?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Review requirements</CardTitle><div className="text-xs">Release review: {String(reviews?.release_review)} | Architecture review: {String(reviews?.architecture_review)} | Governance review: {String(reviews?.governance_review)}</div></Card>
    <Card><CardTitle>Rollback readiness</CardTitle><div className="text-xs">Plan present: {String(rollback?.rollback_plan_present)} | Risk: {rollback?.rollback_risk_level ?? "..."}</div></Card>
    <Card><CardTitle>Approval brief</CardTitle><div className="text-xs">Summary: {brief?.change_summary ?? "..."} | Benefit: {brief?.expected_benefit ?? "..."}</div></Card>
    <Card><CardTitle>Dependency risks</CardTitle><div className="text-xs">Upstream: {impact?.upstream_dependencies?.join(" | ") ?? "..."} | Downstream: {impact?.downstream_dependents?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Required validations</CardTitle><div className="text-xs">{brief?.validation_plan?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Safety boundary</CardTitle><p className="text-xs text-muted">Change control is advisory-only and no-execution. No auto-approve/reject, no command execution, no commits, no deploys, no rollbacks, and no automatic migrations.</p></Card>
  </div>;
}
