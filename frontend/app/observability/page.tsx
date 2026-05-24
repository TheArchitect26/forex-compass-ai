"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Card, CardTitle } from "@/components/ui";

export default function ObservabilityPage() {
  const [status, setStatus] = useState<any>(null);
  const [runtime, setRuntime] = useState<any>(null);
  const [endpoints, setEndpoints] = useState<any>(null);
  const [regressions, setRegressions] = useState<any>(null);
  const [incident, setIncident] = useState<any>(null);

  useEffect(() => {
    api("/api/observability/status").then(setStatus);
    api("/api/observability/runtime-scan", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setRuntime);
    api("/api/observability/endpoint-health", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setEndpoints);
    api("/api/observability/regression-check", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setRegressions);
    api("/api/observability/incident-summary", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setIncident);
  }, []);

  return <div className="space-y-4">
    <h1 className="text-xl font-semibold">Observability</h1>
    <Card><CardTitle>Runtime health scores</CardTitle><div className="text-xs">Runtime health: {status?.runtime_health_score ?? "..."} | Endpoint reliability: {status?.endpoint_reliability_score ?? "..."} | Monitoring readiness: {status?.monitoring_readiness_score ?? "..."}</div></Card>
    <Card><CardTitle>Endpoint health list</CardTitle><div className="text-xs">{endpoints?.endpoint_observations?.map((x: any) => `${x.method} ${x.endpoint_path} -> ${x.observed_status}`).join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Regression warnings</CardTitle><div className="text-xs">{regressions?.routes_failing_after_release?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Incident summaries</CardTitle><div className="text-xs">Issue: {incident?.likely_issue ?? "..."} | Severity: {incident?.severity ?? "..."}</div></Card>
    <Card><CardTitle>Latency and error pressure</CardTitle><div className="text-xs">Latency risk: {status?.latency_risk_score ?? "..."} | Error pressure: {status?.error_pressure_score ?? "..."} | Runtime pressure: {runtime?.latency_pressure ?? "..."}</div></Card>
    <Card><CardTitle>Recovery visibility</CardTitle><div className="text-xs">Recovery visibility score: {status?.recovery_visibility_score ?? "..."}</div></Card>
    <Card><CardTitle>Safety boundary</CardTitle><p className="text-xs text-muted">Observability is advisory-only. No automatic rollback, route disabling, environment mutation, deployment fix, or trade execution.</p></Card>
  </div>;
}
