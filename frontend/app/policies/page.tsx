"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Card, CardTitle } from "@/components/ui";

export default function PoliciesPage() {
  const [status, setStatus] = useState<any>(null);
  const [list, setList] = useState<any>(null);
  const [compliance, setCompliance] = useState<any>(null);
  const [conflict, setConflict] = useState<any>(null);
  const [summary, setSummary] = useState<any>(null);

  useEffect(() => {
    api("/api/policies/status").then(setStatus);
    api("/api/policies/list", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setList);
    api("/api/policies/evaluate-compliance", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setCompliance);
    api("/api/policies/conflict-review", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setConflict);
    api("/api/policies/doctrine-summary", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setSummary);
  }, []);

  return <div className="space-y-4">
    <h1 className="text-xl font-semibold">Policies</h1>
    <Card><CardTitle>Institutional doctrines</CardTitle><div className="text-xs">{summary?.governance_philosophy?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Constitutional rules</CardTitle><div className="text-xs">{status?.constitutional_rules?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Compliance reviews</CardTitle><div className="text-xs">Violates doctrine: {String(compliance?.violates_institutional_doctrine)} | Weakens observability: {String(compliance?.weakens_observability)}</div></Card>
    <Card><CardTitle>Doctrine conflicts</CardTitle><div className="text-xs">{conflict?.conflict_summary ?? "..."} | Severity: {conflict?.risk_severity ?? "..."}</div></Card>
    <Card><CardTitle>Policy coverage</CardTitle><div className="text-xs">Coverage: {status?.policy_coverage_score ?? "..."} | Governance completeness: {status?.governance_completeness_score ?? "..."}</div></Card>
    <Card><CardTitle>Governance protections</CardTitle><div className="text-xs">No auto-approve compliance: {String(status?.never_auto_approve_compliance)} | No doctrine rewrite: {String(status?.never_auto_rewrite_doctrine)}</div></Card>
    <Card><CardTitle>Human-review requirements</CardTitle><div className="text-xs">Human approval required: {String(status?.human_approval_required)}</div></Card>
    <Card><CardTitle>Safety boundary</CardTitle><p className="text-xs text-muted">Policy governance is advisory-only and no-execution. No auto-enforcement of destructive actions, no auto-deletion, no auto-governance-state changes, and no autonomous doctrine mutation.</p></Card>
  </div>;
}
