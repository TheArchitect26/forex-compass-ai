"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Card, CardTitle } from "@/components/ui";

export default function InstitutionalLearningPage() {
  const [lessons, setLessons] = useState<any>(null);
  const [intervention, setIntervention] = useState<any>(null);
  const [forecast, setForecast] = useState<any>(null);
  const [assumption, setAssumption] = useState<any>(null);

  useEffect(() => {
    api("/api/learning/extract-lessons", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setLessons);
    api("/api/learning/intervention-review", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setIntervention);
    api("/api/learning/forecast-review", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setForecast);
    api("/api/learning/assumption-review", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setAssumption);
  }, []);

  return <div className="space-y-4">
    <h1 className="text-xl font-semibold">Institutional Learning Console</h1>
    <Card><CardTitle>Extracted lessons</CardTitle><div className="text-xs">{lessons?.lessons?.map((l:any)=>`${l.lesson} (conf:${l.confidence})`).join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Intervention effectiveness</CardTitle><div className="text-xs">Effectiveness: {intervention?.effectiveness_score ?? "..."} | Burden: {intervention?.operator_burden ?? "..."}</div></Card>
    <Card><CardTitle>Forecast accuracy review</CardTitle><div className="text-xs">Accuracy: {forecast?.accuracy_score ?? "..."} | Weak evidence: {String(forecast?.weak_evidence)}</div></Card>
    <Card><CardTitle>Assumption review</CardTitle><div className="text-xs">Assumption: {assumption?.assumption ?? "..."} | Status: {assumption?.status ?? "..."}</div></Card>
    <Card><CardTitle>Weak-evidence warnings</CardTitle><div className="text-xs">{lessons?.lessons?.filter((l:any)=>l.weak_evidence).map((l:any)=>l.lesson).join(" | ") || "none"}</div></Card>
    <Card><CardTitle>Human-review requirement</CardTitle><div className="text-xs">Learning output is advisory and requires operator adoption decisions.</div></Card>
    <Card><CardTitle>No-execution safety</CardTitle><p className="text-xs text-muted">Institutional learning never auto-modifies strategy or governance.</p></Card>
  </div>;
}
