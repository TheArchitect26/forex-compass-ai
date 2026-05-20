"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Card, CardTitle } from "@/components/ui";

export default function MissionIntegrityConsolePage() {
  const [mission, setMission] = useState<any>(null);
  const [status, setStatus] = useState<any>(null);
  const [timeline, setTimeline] = useState<any>(null);
  const [anchors, setAnchors] = useState<any[]>([]);
  const [warnings, setWarnings] = useState<any>(null);
  const [humility, setHumility] = useState<any>(null);

  useEffect(() => {
    api("/api/governance/mission").then(setMission);
    api("/api/governance/mission-status").then((r) => setStatus(r.mission_status));
    api("/api/system/mission-timeline").then(setTimeline);
    api("/api/governance/anchor-note").then(setAnchors);
  }, []);

  const runDriftScan = async () => {
    const out = await api("/api/governance/mission-drift", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ mission_drift: 0.7, optimization_drift: 0.65 })
    });
    setWarnings(out);
  };

  const runHumility = async () => {
    const out = await api("/api/governance/humility-safeguards", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ overconfidence_inflation: 0.7, excessive_abstraction: 0.75 })
    });
    setHumility(out);
  };

  return <div className="space-y-4">
    <h1 className="text-xl font-semibold">Mission Integrity Console</h1>
    <Card><CardTitle>Foundational mission</CardTitle><div className="text-xs">{mission?.foundational_mission || "..."}</div><div className="text-xs mt-1">Non-goals: {(mission?.strategic_non_goals || []).join(", ")}</div></Card>
    <Card><CardTitle>Mission coherence scoring</CardTitle><div className="text-xs">Alignment: {status?.mission_alignment_score ?? "..."} | Existential coherence: {status?.existential_coherence_score ?? "..."} | Purpose integrity: {status?.strategic_purpose_integrity_score ?? "..."}</div></Card>
    <Card><CardTitle>Operator-intent anchors</CardTitle><div className="text-xs space-y-1">{anchors.map((a:any)=> <div key={a.id}>{a.mission_reaffirmation || a.operator_note}</div>)}</div></Card>
    <Card><CardTitle>Mission evolution timeline</CardTitle><div className="text-xs">Revisions: {(timeline?.mission_revisions || []).length} | Realignments: {(timeline?.governance_realignments || []).length}</div></Card>
    <Card><CardTitle>Anti-drift warnings</CardTitle><button className="px-2 py-1 rounded bg-accent text-bg text-xs" onClick={runDriftScan}>Run mission drift scan</button><div className="text-xs mt-2">Flags: {(warnings?.drift_flags || []).join(", ") || "none"}</div></Card>
    <Card><CardTitle>Humility indicators</CardTitle><button className="px-2 py-1 rounded bg-panel2 border border-border text-xs" onClick={runHumility}>Run humility safeguards</button><div className="text-xs mt-2">Flags: {(humility?.humility_flags || []).join(", ") || "none"}</div></Card>
    <Card><CardTitle>Safety</CardTitle><p className="text-xs text-muted">Human strategic intent is the anchor. No autonomous institutional authority or mission self-rewrite.</p></Card>
  </div>;
}
