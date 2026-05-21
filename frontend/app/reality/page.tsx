"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Card, CardTitle } from "@/components/ui";

export default function RealityConsolePage() {
  const [status, setStatus] = useState<any>(null);
  const [score, setScore] = useState<any>(null);
  const [timeline, setTimeline] = useState<any>(null);

  useEffect(() => {
    api("/api/governance/reality-status").then(setStatus);
    api("/api/governance/relevance-score").then(setScore);
    api("/api/system/reality-timeline").then(setTimeline);
  }, []);

  return <div className="space-y-4">
    <h1 className="text-xl font-semibold">Reality & Relevance Console</h1>
    <Card><CardTitle>Reality alignment</CardTitle><div className="text-xs">Alignment: {score?.relevance_score?.reality_alignment_score ?? "..."}</div></Card>
    <Card><CardTitle>Usefulness scores</CardTitle><div className="text-xs">Overall: {score?.relevance_score?.overall_relevance_score ?? "..."} | Operator utility: {status?.reality_status?.operator_utility ?? "..."}</div></Card>
    <Card><CardTitle>Practical relevance indicators</CardTitle><div className="text-xs">Real-world relevance: {status?.reality_status?.real_world_relevance ?? "..."} | External grounding: {status?.external_grounding?.real_world_outcome_alignment ?? "..."}</div></Card>
    <Card><CardTitle>Replay realism gaps</CardTitle><div className="text-xs">Replay-to-reality consistency: {status?.reality_status?.replay_to_reality_consistency ?? "..."}</div></Card>
    <Card><CardTitle>Usefulness anchors</CardTitle><div className="text-xs">{timeline?.usefulness_recoveries?.join(", ") ?? "..."}</div></Card>
    <Card><CardTitle>No-execution guarantee</CardTitle><p className="text-xs text-muted">Research and signal intelligence only. No autonomous strategic or trade execution.</p></Card>
  </div>;
}
