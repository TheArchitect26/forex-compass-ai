"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Card, CardTitle } from "@/components/ui";

export default function OperationsConsolePage() {
  const [status, setStatus] = useState<any>(null);
  const [plan, setPlan] = useState<any>(null);
  const [deferred, setDeferred] = useState<any>(null);
  const [maintenance, setMaintenance] = useState<any>(null);
  const [cadence, setCadence] = useState<any>(null);

  useEffect(() => {
    api("/api/operations/status").then(setStatus);
    api("/api/operations/review-plan", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setPlan);
    api("/api/operations/deferred-action", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setDeferred);
    api("/api/operations/maintenance-cycle", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setMaintenance);
    api("/api/operations/cadence-check", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setCadence);
  }, []);

  return <div className="space-y-4">
    <h1 className="text-xl font-semibold">Operations Console</h1>
    <Card><CardTitle>Operational status</CardTitle><div className="text-xs">Reviews: {status?.scheduled_reviews ?? "..."} | Debt: {status?.unresolved_operational_debt ?? "..."}</div></Card>
    <Card><CardTitle>Upcoming reviews</CardTitle><div className="text-xs">{plan?.review_plan?.slice(0,3).map((r:any)=>`${r.type}:${r.window}`).join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Deferred actions</CardTitle><div className="text-xs">Reason: {deferred?.reason_deferred ?? "..."} | Risk: {deferred?.risk_of_delay ?? "..."}</div></Card>
    <Card><CardTitle>Maintenance cycles & overdue work</CardTitle><div className="text-xs">Plan: {maintenance?.maintenance_plan?.join(", ") ?? "..."} | Overdue: {maintenance?.overdue_work?.join(", ") ?? "..."}</div></Card>
    <Card><CardTitle>Cadence health</CardTitle><div className="text-xs">Health: {cadence?.cadence_health ?? "..."} | Adherence: {cadence?.cadence_adherence ?? "..."}</div></Card>
    <Card><CardTitle>Operator-safe next actions</CardTitle><div className="text-xs">{maintenance?.operator_safe_next_actions?.join(", ") ?? "..."}</div></Card>
    <Card><CardTitle>No-execution safety</CardTitle><p className="text-xs text-muted">Operations output is advisory only; no tasks are auto-completed or auto-deleted.</p></Card>
  </div>;
}
