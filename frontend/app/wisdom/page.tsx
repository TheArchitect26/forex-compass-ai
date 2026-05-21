"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Card, CardTitle } from "@/components/ui";

export default function WisdomPage() {
  const [status, setStatus] = useState<any>(null);
  const [ambiguity, setAmbiguity] = useState<any>(null);
  const [judgment, setJudgment] = useState<any>(null);
  const [restraint, setRestraint] = useState<any>(null);
  const [prudence, setPrudence] = useState<any>(null);

  useEffect(() => {
    api("/api/wisdom/status").then(setStatus);
    api("/api/wisdom/ambiguity-review", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setAmbiguity);
    api("/api/wisdom/judgment-audit", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setJudgment);
    api("/api/wisdom/restraint-check", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setRestraint);
    api("/api/wisdom/prudence-review", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setPrudence);
  }, []);

  return <div className="space-y-4">
    <h1 className="text-xl font-semibold">Wisdom</h1>
    <Card><CardTitle>Wisdom scores</CardTitle><div className="text-xs">Wisdom: {status?.wisdom_score ?? "..."} | Prudence: {status?.prudence_score ?? "..."} | Restraint: {status?.restraint_score ?? "..."}</div></Card>
    <Card><CardTitle>Ambiguity review</CardTitle><div className="text-xs">{ambiguity?.ambiguity_pressure?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Uncertainty map</CardTitle><div className="text-xs">Known: {ambiguity?.knowns?.join(" | ") ?? "..."} || Uncertain: {ambiguity?.uncertain?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Restraint warnings</CardTitle><div className="text-xs">{restraint?.restraint_warnings?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Prudence review</CardTitle><div className="text-xs">Reflective reasoning: {prudence?.reflective_reasoning ?? "..."} | Proportionality: {prudence?.proportionality ?? "..."}</div></Card>
    <Card><CardTitle>What not to conclude yet</CardTitle><div className="text-xs">{ambiguity?.what_not_to_conclude_yet?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Human-review requirement</CardTitle><p className="text-xs text-muted">Judgment decisions remain human-reviewed and advisory-only.</p></Card>
    <Card><CardTitle>Safety boundary</CardTitle><p className="text-xs text-muted">Wisdom support never auto-decides, auto-selects pathways, or overrides operator sovereignty.</p></Card>
  </div>;
}
