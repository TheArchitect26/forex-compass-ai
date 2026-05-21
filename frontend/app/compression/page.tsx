"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Card, CardTitle } from "@/components/ui";

export default function CompressionPage() {
  const [status, setStatus] = useState<any>(null);
  const [distilled, setDistilled] = useState<any>(null);
  const [lessons, setLessons] = useState<any>(null);
  const [patterns, setPatterns] = useState<any>(null);
  const [heur, setHeur] = useState<any>(null);

  useEffect(() => {
    api("/api/compression/status").then(setStatus);
    api("/api/compression/distill", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setDistilled);
    api("/api/compression/strategic-lessons", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setLessons);
    api("/api/compression/anti-patterns", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setPatterns);
    api("/api/compression/heuristics", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setHeur);
  }, []);

  return <div className="space-y-4">
    <h1 className="text-xl font-semibold">Compression</h1>
    <Card><CardTitle>Distilled strategic lessons</CardTitle><div className="text-xs">{lessons?.what_repeatedly_worked?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Institutional heuristics</CardTitle><div className="text-xs">{heur?.institutional_heuristics?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Recurring anti-patterns</CardTitle><div className="text-xs">{patterns?.recurring_anti_patterns?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Compressed governance insights</CardTitle><div className="text-xs">{distilled?.governance_doctrines?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Deployment/runtime lessons</CardTitle><div className="text-xs">{distilled?.deployment_lessons?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Clutter-reduction opportunities</CardTitle><div className="text-xs">{lessons?.clutter_reduction_opportunities?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Compression status</CardTitle><div className="text-xs">Efficiency: {status?.compression_efficiency_score ?? "..."} | Recall usefulness: {status?.recall_usefulness_score ?? "..."} | Clutter reduction: {status?.clutter_reduction_score ?? "..."}</div></Card>
    <Card><CardTitle>Safety boundary</CardTitle><p className="text-xs text-muted">Compression is advisory-only. No auto-delete of history, no history rewrite, no warning suppression, and no trade execution.</p></Card>
  </div>;
}
