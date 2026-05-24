"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Card, CardTitle } from "@/components/ui";

export default function UxPage() {
  const [status, setStatus] = useState<any>(null);
  const [usability, setUsability] = useState<any>(null);
  const [navigation, setNavigation] = useState<any>(null);
  const [readability, setReadability] = useState<any>(null);
  const [plan, setPlan] = useState<any>(null);

  useEffect(() => {
    api("/api/ux/status").then(setStatus);
    api("/api/ux/usability-audit", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setUsability);
    api("/api/ux/navigation-audit", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setNavigation);
    api("/api/ux/readability-review", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setReadability);
    api("/api/ux/simplification-plan", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setPlan);
  }, []);

  return <div className="space-y-4">
    <h1 className="text-xl font-semibold">UX Quality</h1>
    <Card><CardTitle>Operator experience scores</CardTitle><div className="text-xs">UX: {status?.operator_experience_score ?? "..."} | Usability clarity: {status?.usability_clarity_score ?? "..."} | Interface coherence: {status?.interface_coherence_score ?? "..."}</div></Card>
    <Card><CardTitle>Usability audit</CardTitle><div className="text-xs">Status visibility: {usability?.visibility_of_system_status ?? "..."} | Hierarchy: {usability?.information_hierarchy_clarity ?? "..."}</div></Card>
    <Card><CardTitle>Navigation audit</CardTitle><div className="text-xs">Too many sidebar items: {String(navigation?.too_many_sidebar_items)} | Grouping: {navigation?.unclear_grouping?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Readability warnings</CardTitle><div className="text-xs">Dense cards: {readability?.dense_cards?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Simplification recommendations</CardTitle><div className="text-xs">{plan?.recommendations?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Daily-use pathway recommendations</CardTitle><div className="text-xs">{plan?.daily_use_pathway?.join(" → ") ?? "..."}</div></Card>
    <Card><CardTitle>Safety boundary</CardTitle><p className="text-xs text-muted">UX Quality is advisory-only. No auto page deletion, no automatic navigation changes, no warning suppression, and no trade execution.</p></Card>
  </div>;
}
