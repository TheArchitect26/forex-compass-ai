"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Card, CardTitle } from "@/components/ui";

export default function PersonalAlignmentConsolePage() {
  const [context, setContext] = useState<any>(null);
  const [alignment, setAlignment] = useState<any>(null);
  const [continuity, setContinuity] = useState<any>(null);

  useEffect(() => {
    api("/api/context/status").then(setContext);
    api("/api/context/alignment-score").then(setAlignment);
    api("/api/system/personal-continuity").then(setContinuity);
  }, []);

  return <div className="space-y-4">
    <h1 className="text-xl font-semibold">Personal Alignment Console</h1>
    <Card><CardTitle>Current priorities & focus</CardTitle><div className="text-xs">Focus: {context?.context?.active_focus_areas?.join(", ") ?? "..."}</div></Card>
    <Card><CardTitle>Cognitive sustainability</CardTitle><div className="text-xs">Score: {alignment?.alignment?.cognitive_sustainability_score ?? "..."}</div></Card>
    <Card><CardTitle>Operator alignment</CardTitle><div className="text-xs">Overall: {alignment?.alignment?.overall_personal_alignment_score ?? "..."}</div></Card>
    <Card><CardTitle>Active context modes</CardTitle><div className="text-xs">Maintenance: {String(context?.context?.maintenance_phase)} | Simplification: {String(context?.context?.simplification_phase)}</div></Card>
    <Card><CardTitle>Operational continuity memory</CardTitle><div className="text-xs">{continuity?.long_term_intent_evolution?.join(", ") ?? "..."}</div></Card>
    <Card><CardTitle>No-execution guarantee</CardTitle><p className="text-xs text-muted">Personal research and signal intelligence only. Human choice remains final.</p></Card>
  </div>;
}
