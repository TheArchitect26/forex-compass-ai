"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Card, CardTitle } from "@/components/ui";

export default function PurposePage() {
  const [status, setStatus] = useState<any>(null);
  const [coherence, setCoherence] = useState<any>(null);
  const [drift, setDrift] = useState<any>(null);
  const [hollowing, setHollowing] = useState<any>(null);
  const [alignment, setAlignment] = useState<any>(null);

  useEffect(() => {
    api("/api/purpose/status").then(setStatus);
    api("/api/purpose/coherence-audit", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setCoherence);
    api("/api/purpose/meaning-drift", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setDrift);
    api("/api/purpose/anti-hollowing", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setHollowing);
    api("/api/purpose/mission-alignment", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setAlignment);
  }, []);

  return <div className="space-y-4">
    <h1 className="text-xl font-semibold">Purpose</h1>
    <Card><CardTitle>Purpose coherence scores</CardTitle><div className="text-xs">Coherence: {status?.purpose_coherence_score ?? "..."} | Mission: {status?.mission_alignment_score ?? "..."} | Meaning: {status?.meaning_preservation_score ?? "..."}</div></Card>
    <Card><CardTitle>Mission alignment</CardTitle><div className="text-xs">{alignment?.doctrine_embodiment_check?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Meaning drift signals</CardTitle><div className="text-xs">{drift?.drift_signals?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Anti-hollowing warnings</CardTitle><div className="text-xs">{hollowing?.anti_hollowing_warnings?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Doctrine embodiment checks</CardTitle><div className="text-xs">Mismatch: {coherence?.doctrine_practice_mismatch?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Purpose-preservation recommendations</CardTitle><div className="text-xs">{hollowing?.purpose_preservation_recommendations?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Safety boundary</CardTitle><p className="text-xs text-muted">Purpose governance is advisory-only and no-execution; mission and feature decisions require explicit human approval.</p></Card>
  </div>;
}
