"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Card, CardTitle } from "@/components/ui";

export default function DebtPage() {
  const [status, setStatus] = useState<any>(null);
  const [scan, setScan] = useState<any>(null);
  const [priorities, setPriorities] = useState<any>(null);
  const [plan, setPlan] = useState<any>(null);
  const [deps, setDeps] = useState<any>(null);

  useEffect(() => {
    api("/api/debt/status").then(setStatus);
    api("/api/debt/scan", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setScan);
    api("/api/debt/prioritize", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setPriorities);
    api("/api/debt/paydown-plan", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setPlan);
    api("/api/debt/dependency-risk", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setDeps);
  }, []);

  return <div className="space-y-4">
    <h1 className="text-xl font-semibold">Technical Debt</h1>
    <Card><CardTitle>Debt scores</CardTitle><div className="text-xs">Debt: {status?.technical_debt_score ?? "..."} | Maintainability: {status?.maintainability_score ?? "..."} | Refactor urgency: {status?.refactor_urgency_score ?? "..."}</div></Card>
    <Card><CardTitle>Debt categories</CardTitle><div className="text-xs">Hotspots: {scan?.code_complexity_hotspots?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Highest-risk debt items</CardTitle><div className="text-xs">{priorities?.priority_ordering?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Dependency/build risks</CardTitle><div className="text-xs">{deps?.frontend_backend_build_mismatch?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Paydown plan</CardTitle><div className="text-xs">{plan?.paydown_actions?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Test confidence</CardTitle><div className="text-xs">Test confidence: {status?.test_confidence_score ?? "..."} | Build fragility: {status?.build_fragility_score ?? "..."}</div></Card>
    <Card><CardTitle>Human-review requirement</CardTitle><p className="text-xs text-muted">Debt prioritization and paydown actions require explicit human approval.</p></Card>
    <Card><CardTitle>Safety boundary</CardTitle><p className="text-xs text-muted">Debt observatory is advisory-only; no automatic deletion, migration, dependency rewrite, or architecture rewrite is performed.</p></Card>
  </div>;
}
