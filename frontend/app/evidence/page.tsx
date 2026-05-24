"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Card, CardTitle } from "@/components/ui";

export default function EvidencePage() {
  const [status, setStatus] = useState<any>(null);
  const [mapping, setMapping] = useState<any>(null);
  const [chain, setChain] = useState<any>(null);
  const [review, setReview] = useState<any>(null);

  useEffect(() => {
    api("/api/evidence/status").then(setStatus);
    api("/api/evidence/control-map", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setMapping);
    api("/api/evidence/chain-of-custody", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setChain);
    api("/api/evidence/readiness-review", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setReview);
  }, []);

  return <div className="space-y-4">
    <h1 className="text-xl font-semibold">Evidence</h1>
    <Card><CardTitle>Evidence completeness</CardTitle><div className="text-xs">Completeness: {status?.evidence_completeness_score ?? "..."} | Freshness: {status?.evidence_freshness_score ?? "..."}</div></Card>
    <Card><CardTitle>Control mappings</CardTitle><div className="text-xs">{mapping?.risk_to_control?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Chain-of-custody view</CardTitle><div className="text-xs">Path: {chain?.evidence_path?.join(" -> ") ?? "..."}</div></Card>
    <Card><CardTitle>Audit readiness gaps</CardTitle><div className="text-xs">{review?.missing_evidence?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Stale evidence</CardTitle><div className="text-xs">{review?.stale_evidence?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Missing evidence</CardTitle><div className="text-xs">{review?.controls_without_proof?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Policy/control links</CardTitle><div className="text-xs">{mapping?.evidence_to_policy?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Safety boundary</CardTitle><p className="text-xs text-muted">Evidence registry is advisory-only and no-execution. No fabrication, no deletion, no evidence-history rewrite, and no automatic compliance approvals.</p></Card>
  </div>;
}
