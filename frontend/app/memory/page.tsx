"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Card, CardTitle } from "@/components/ui";

export default function MemoryPage() {
  const [status, setStatus] = useState<any>(null);
  const [search, setSearch] = useState<any>(null);
  const [recall, setRecall] = useState<any>(null);
  const [related, setRelated] = useState<any>(null);
  const [stale, setStale] = useState<any>(null);

  useEffect(() => {
    api("/api/memory/status").then(setStatus);
    api("/api/memory/search", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setSearch);
    api("/api/memory/contextual-recall", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setRecall);
    api("/api/memory/related-items", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setRelated);
    api("/api/memory/staleness-review", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setStale);
  }, []);

  return <div className="space-y-4">
    <h1 className="text-xl font-semibold">Memory</h1>
    <Card><CardTitle>Memory search</CardTitle><div className="text-xs">Coverage: {status?.memory_coverage_score ?? "..."} | Accuracy est.: {status?.retrieval_accuracy_estimate ?? "..."}</div></Card>
    <Card><CardTitle>Contextual recall results</CardTitle><div className="text-xs">Lessons: {recall?.most_relevant_prior_lessons?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Related phase history</CardTitle><div className="text-xs">{related?.related_phase_history?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Stale knowledge warnings</CardTitle><div className="text-xs">{stale?.old_assumptions_no_longer_reliable?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Unresolved assumptions</CardTitle><div className="text-xs">{recall?.related_assumptions?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Important lessons</CardTitle><div className="text-xs">{search?.matches?.map((m: any) => m.title).join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Safety boundary</CardTitle><p className="text-xs text-muted">Memory retrieval is advisory-only. No auto-delete, no auto-rewrite of history, no auto-resolution of assumptions, and no trade execution.</p></Card>
  </div>;
}
