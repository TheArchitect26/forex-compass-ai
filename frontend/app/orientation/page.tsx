"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Card, CardTitle } from "@/components/ui";

export default function StrategicOrientationConsolePage() {
  const [orientation, setOrientation] = useState<any>(null);
  const [score, setScore] = useState<any>(null);
  const [glossary, setGlossary] = useState<any[]>([]);
  const [lineage, setLineage] = useState<any[]>([]);
  const [conflicts, setConflicts] = useState<any>(null);

  useEffect(() => {
    api("/api/meta/orientation").then(setOrientation);
    api("/api/meta/orientation-score").then((r) => setScore(r.orientation_score));
    api("/api/governance/glossary").then(setGlossary);
    api("/api/governance/concept-lineage").then(setLineage);
  }, []);

  const scanConflicts = async () => {
    const out = await api("/api/meta/meaning-conflicts", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ concepts: [{ term: "risk envelope", meaning: "max risk per cluster" }, { term: "risk envelope", meaning: "max risk per position" }] })
    });
    setConflicts(out);
  };

  return <div className="space-y-4">
    <h1 className="text-xl font-semibold">Strategic Orientation Console</h1>
    <Card><CardTitle>Institutional orientation</CardTitle><div className="text-xs">Optimizing for: {orientation?.optimization_target || "..."} | Priorities: {(orientation?.dominant_priorities || []).join(", ")}</div></Card>
    <Card><CardTitle>Semantic stability indicators</CardTitle><div className="text-xs">Semantic coherence: {score?.semantic_coherence_score ?? "..."} | Strategic clarity: {score?.strategic_clarity_score ?? "..."} | Orientation stability: {score?.operator_orientation_stability_score ?? "..."}</div></Card>
    <Card><CardTitle>Concept lineage map</CardTitle><div className="text-xs space-y-1">{lineage.map((x:any)=> <div key={x.id}>{x.concept} · revs: {(x.revisions||[]).length}</div>)}</div></Card>
    <Card><CardTitle>Glossary explorer</CardTitle><div className="text-xs space-y-1">{glossary.map((g:any)=> <div key={g.id}>{g.term}: {g.canonical_definition}</div>)}</div></Card>
    <Card><CardTitle>Meaning conflict alerts</CardTitle><button className="px-2 py-1 rounded bg-accent text-bg text-xs" onClick={scanConflicts}>Scan conflicts</button><div className="text-xs mt-2">Conflicts: {(conflicts?.conflicts || []).length}</div></Card>
    <Card><CardTitle>Comprehension safeguard</CardTitle><p className="text-xs text-muted">Human comprehension remains central. No recursive self-justifying governance or autonomous authority.</p></Card>
  </div>;
}
