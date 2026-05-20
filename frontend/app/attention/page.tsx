"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Card, CardTitle } from "@/components/ui";

export default function AttentionFocusConsolePage() {
  const [priority, setPriority] = useState<any>(null);
  const [memory, setMemory] = useState<any>(null);
  const [focusMode, setFocusMode] = useState<any>(null);

  useEffect(() => {
    api("/api/attention/priority-status").then(setPriority);
    api("/api/attention/attention-memory").then(setMemory);
    api("/api/attention/focus-mode", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ mode: "executive_overview" }) }).then(setFocusMode);
  }, []);

  return <div className="space-y-4">
    <h1 className="text-xl font-semibold">Attention & Focus Console</h1>
    <Card><CardTitle>Attention load & signal-to-noise</CardTitle><div className="text-xs">SNR: {priority?.priority_status?.signal_to_noise_ratio ?? "..."} | Efficiency: {priority?.priority_status?.attention_efficiency_score ?? "..."}</div></Card>
    <Card><CardTitle>Urgency distribution</CardTitle><div className="text-xs">Urgency score: {priority?.priority_status?.urgency_score ?? "..."}</div></Card>
    <Card><CardTitle>Top-priority intelligence</CardTitle><div className="text-xs">{memory?.highest_value_insights?.join(", ") ?? "..."}</div></Card>
    <Card><CardTitle>Strategic focus mode</CardTitle><div className="text-xs">Mode: {focusMode?.mode ?? "..."} | Priorities: {focusMode?.priorities?.join(", ") ?? "..."}</div></Card>
    <Card><CardTitle>Stale-information pressure</CardTitle><div className="text-xs">Suppression systems prioritize stale low-impact items for archival.</div></Card>
    <Card><CardTitle>No-execution guarantee</CardTitle><p className="text-xs text-muted">Signal intelligence only. Prioritization never overrides operator intent.</p></Card>
  </div>;
}
