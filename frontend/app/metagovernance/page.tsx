"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Card, CardTitle } from "@/components/ui";

export default function MetaGovernancePage() {
  const [status, setStatus] = useState<any>(null);
  const [conflicts, setConflicts] = useState<any>(null);
  const [audit, setAudit] = useState<any>(null);
  const [plan, setPlan] = useState<any>(null);
  const [drift, setDrift] = useState<any>(null);

  useEffect(() => {
    api("/api/metagovernance/status").then(setStatus);
    api("/api/metagovernance/policy-conflicts", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setConflicts);
    api("/api/metagovernance/safeguard-audit", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setAudit);
    api("/api/metagovernance/harmonization-plan", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setPlan);
    api("/api/metagovernance/doctrine-drift", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setDrift);
  }, []);

  return <div className="space-y-4">
    <h1 className="text-xl font-semibold">Meta-Governance</h1>
    <Card><CardTitle>Governance alignment scores</CardTitle><div className="text-xs">Alignment: {status?.governance_alignment_score ?? "..."} | Safeguards: {status?.safeguard_consistency_score ?? "..."} | Policy clarity: {status?.policy_clarity_score ?? "..."}</div></Card>
    <Card><CardTitle>Policy conflicts</CardTitle><div className="text-xs">{conflicts?.policy_contradictions?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Safeguard audit</CardTitle><div className="text-xs">Drift: {audit?.safeguard_drift?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Doctrine drift warnings</CardTitle><div className="text-xs">{drift?.drift_warnings?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Harmonization proposals</CardTitle><div className="text-xs">{plan?.harmonization_proposals?.map((p:any)=>p.proposed_resolution).join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Affected systems</CardTitle><div className="text-xs">{plan?.harmonization_proposals?.flatMap((p:any)=>p.affected_systems || []).join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Safety boundary</CardTitle><p className="text-xs text-muted">Meta-governance is advisory-only and no-execution; policy changes require explicit human approval.</p></Card>
  </div>;
}
