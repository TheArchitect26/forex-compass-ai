"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Card, CardTitle } from "@/components/ui";

export default function EcosystemConsolePage() {
  const [dep, setDep] = useState<any>(null);
  const [risk, setRisk] = useState<any>(null);
  const [pressure, setPressure] = useState<any>(null);
  const [memory, setMemory] = useState<any>(null);

  useEffect(() => {
    api("/api/ecosystem/dependency-map", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setDep);
    api("/api/ecosystem/risk-scan", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setRisk);
    api("/api/ecosystem/environmental-pressure", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setPressure);
    api("/api/ecosystem/memory").then(setMemory);
  }, []);

  return <div className="space-y-4">
    <h1 className="text-xl font-semibold">Ecosystem Console</h1>
    <Card><CardTitle>Dependency map</CardTitle><div className="text-xs">{dep?.dependencies?.map((d:any)=>`${d.name}:${d.current_health}`).join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Critical dependencies & concentration risk</CardTitle><div className="text-xs">{dep?.dependencies?.filter((d:any)=>d.criticality==="critical" || d.concentration_risk==="high").map((d:any)=>d.name).join(", ") || "none"}</div></Card>
    <Card><CardTitle>Ecosystem risk scores</CardTitle><div className="text-xs">Dependency risk: {risk?.ecosystem_risk_scores?.dependency_risk_score ?? "..."} | Fallback readiness: {risk?.ecosystem_risk_scores?.fallback_readiness_score ?? "..."}</div></Card>
    <Card><CardTitle>Environmental pressure warnings</CardTitle><div className="text-xs">Volatility: {pressure?.market_volatility_expansion ?? "..."} | API failures: {pressure?.api_failure_rate_increase ?? "..."}</div></Card>
    <Card><CardTitle>Recent external incidents</CardTitle><div className="text-xs">{memory?.dependency_incidents?.join(", ") ?? "..."}</div></Card>
    <Card><CardTitle>No-execution safety</CardTitle><p className="text-xs text-muted">Ecosystem outputs are advisory only and require human review for fallback actions.</p></Card>
  </div>;
}
