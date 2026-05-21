"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Card, CardTitle } from "@/components/ui";

export default function StrategicSynthesisPage() {
  const [status, setStatus] = useState<any>(null);
  const [brief, setBrief] = useState<any>(null);
  const [conflicts, setConflicts] = useState<any>(null);
  const [memory, setMemory] = useState<any>(null);

  useEffect(() => {
    api("/api/synthesis/status").then(setStatus);
    api("/api/synthesis/brief").then(setBrief);
    api("/api/synthesis/conflicts", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ attention_urgent: true, wisdom_wait: true }) }).then(setConflicts);
    api("/api/synthesis/memory").then(setMemory);
  }, []);

  return <div className="space-y-4">
    <h1 className="text-xl font-semibold">Strategic Synthesis Console</h1>
    <Card><CardTitle>Unified strategic brief</CardTitle><div className="text-xs">Focus: {status?.status?.recommended_focus ?? "..."} | Review: {status?.status?.timing_guidance ?? "..."}</div></Card>
    <Card><CardTitle>Top priorities</CardTitle><div className="text-xs">{brief?.top_priorities?.map((x:any)=>x.label).join(", ") ?? "..."}</div></Card>
    <Card><CardTitle>Ignored noise</CardTitle><div className="text-xs">{brief?.ignore_for_now?.map((x:any)=>x.label).join(", ") ?? "..."}</div></Card>
    <Card><CardTitle>Cross-layer conflicts</CardTitle><div className="text-xs">{conflicts?.conflicts?.join(", ") ?? "none"}</div></Card>
    <Card><CardTitle>Operator-safe actions</CardTitle><div className="text-xs">{status?.status?.operator_safe_next_actions?.join(", ") ?? "..."}</div></Card>
    <Card><CardTitle>Synthesis memory</CardTitle><div className="text-xs">{memory?.focus_decisions?.join(", ") ?? "..."}</div></Card>
    <Card><CardTitle>No-execution safety</CardTitle><p className="text-xs text-muted">Synthesis is advisory-only and never auto-applies strategy changes.</p></Card>
  </div>;
}
