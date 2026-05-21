"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Card, CardTitle } from "@/components/ui";

const views = ["Executive View", "Release/Runtime View", "Governance View", "Architecture/Maintenance View", "Strategy/Intelligence View", "Crisis/Resilience View", "Minimal Daily View"];

export default function ControlPlanePage() {
  const [status, setStatus] = useState<any>(null);
  const [summary, setSummary] = useState<any>(null);
  const [sprawl, setSprawl] = useState<any>(null);
  const [focus, setFocus] = useState<any>(null);
  const [selectedView, setSelectedView] = useState<string>("Executive View");

  useEffect(() => {
    api("/api/control-plane/status").then(setStatus);
    api("/api/control-plane/summary", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setSummary);
    api("/api/control-plane/console-sprawl", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setSprawl);
  }, []);

  useEffect(() => {
    api("/api/control-plane/focus-view", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ view: selectedView }) }).then(setFocus);
  }, [selectedView]);

  return <div className="space-y-4">
    <h1 className="text-xl font-semibold">Control Plane</h1>
    <Card><CardTitle>Unified institutional health</CardTitle><div className="text-xs">Institutional health: {status?.institutional_health_score ?? "..."} | Clarity: {status?.operator_clarity_score ?? "..."} | Cognitive load: {status?.cognitive_load_score ?? "..."}</div></Card>
    <Card><CardTitle>Top priorities</CardTitle><div className="text-xs">{summary?.top_institutional_priorities?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>What to ignore for now</CardTitle><div className="text-xs">{summary?.top_ignore_or_defer?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Critical warnings</CardTitle><div className="text-xs">{summary?.critical_warnings?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Focus view selector</CardTitle><select className="text-xs bg-panel2 border border-border rounded px-2 py-1" value={selectedView} onChange={(e) => setSelectedView(e.target.value)}>{views.map((v) => <option key={v} value={v}>{v}</option>)}</select><div className="text-xs mt-2">Relevant signals: {focus?.relevant_signals?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Release/runtime status</CardTitle><div className="text-xs">Release/deploy: {summary?.release_deployment_status ?? "..."} | Runtime: {summary?.runtime_health ?? "..."}</div></Card>
    <Card><CardTitle>Debt/architecture status</CardTitle><div className="text-xs">Sprawl score: {status?.dashboard_sprawl_score ?? "..."} | Navigation burden: {status?.navigation_burden_score ?? "..."}</div></Card>
    <Card><CardTitle>Resilience/trust/purpose status</CardTitle><div className="text-xs">Actionability: {status?.actionability_score ?? "..."} | Signal-to-noise: {status?.signal_to_noise_score ?? "..."}</div></Card>
    <Card><CardTitle>Next best human-reviewed action</CardTitle><div className="text-xs">{summary?.next_best_human_reviewed_action ?? "..."}</div></Card>
    <Card><CardTitle>Sidebar simplification recommendation</CardTitle><div className="text-xs">{sprawl?.sidebar_simplification_recommendation?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Safety boundary</CardTitle><p className="text-xs text-muted">Control Plane is advisory-only: no automatic execution, deployment, rollback, navigation changes, or action completion.</p></Card>
  </div>;
}
