"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Card, CardTitle } from "@/components/ui";

export default function AuditTrailPage() {
  const [status, setStatus] = useState<any>(null);
  const [event, setEvent] = useState<any>(null);
  const [prov, setProv] = useState<any>(null);
  const [traceRes, setTraceRes] = useState<any>(null);
  const [lineage, setLineage] = useState<any>(null);

  useEffect(() => {
    api("/api/audit-trail/status").then(setStatus);
    api("/api/audit-trail/record", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setEvent);
    api("/api/audit-trail/provenance", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setProv);
    api("/api/audit-trail/trace", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setTraceRes);
    api("/api/audit-trail/governance-lineage", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setLineage);
  }, []);

  return <div className="space-y-4">
    <h1 className="text-xl font-semibold">Audit Trail</h1>
    <Card><CardTitle>Recent audit events</CardTitle><div className="text-xs">{event?.what_decided_or_recommended ?? "..."}</div></Card>
    <Card><CardTitle>Decision provenance</CardTitle><div className="text-xs">Decision ID: {prov?.decision_id ?? "..."} | Source: {prov?.recommendation_source?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Governance lineage</CardTitle><div className="text-xs">{lineage?.lineage_summary ?? "..."}</div></Card>
    <Card><CardTitle>Policy references</CardTitle><div className="text-xs">{lineage?.policy_references?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Evidence summaries</CardTitle><div className="text-xs">{event?.evidence_used?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Traceability gaps</CardTitle><div className="text-xs">{traceRes?.traceability_gaps?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Safety boundary</CardTitle><p className="text-xs text-muted">Audit trail is advisory-only and no-execution. No history rewrite, no audit deletion, no hidden governance conflicts, and no automatic approvals.</p></Card>
  </div>;
}
