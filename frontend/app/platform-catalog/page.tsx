"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Card, CardTitle } from "@/components/ui";

export default function PlatformCatalogPage() {
  const [status, setStatus] = useState<any>(null);
  const [entities, setEntities] = useState<any>(null);
  const [ownership, setOwnership] = useState<any>(null);
  const [dependency, setDependency] = useState<any>(null);
  const [paths, setPaths] = useState<any>(null);

  useEffect(() => {
    api("/api/platform-catalog/status").then(setStatus);
    api("/api/platform-catalog/entities", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setEntities);
    api("/api/platform-catalog/ownership-audit", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setOwnership);
    api("/api/platform-catalog/dependency-map", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setDependency);
    api("/api/platform-catalog/golden-paths", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setPaths);
  }, []);

  return <div className="space-y-4">
    <h1 className="text-xl font-semibold">Platform Catalog</h1>
    <Card><CardTitle>Catalog completeness</CardTitle><div className="text-xs">Completeness: {status?.catalog_completeness_score ?? "..."} | Coherence: {status?.platform_coherence_score ?? "..."} | Golden path maturity: {status?.golden_path_maturity_score ?? "..."}</div></Card>
    <Card><CardTitle>Entity registry</CardTitle><div className="text-xs">{entities?.entities?.map((e: any) => `${e.entity_name} [${e.entity_type}] owner=${e.owner}`).join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Ownership gaps</CardTitle><div className="text-xs">Missing owner: {ownership?.missing_owner?.join(" | ") ?? "..."} | Unclear lifecycle: {ownership?.unclear_lifecycle_state?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Dependency map</CardTitle><div className="text-xs">Upstream: {dependency?.upstream_dependencies?.join(" | ") ?? "..."} | Risk: {dependency?.risk_if_changed ?? "..."}</div></Card>
    <Card><CardTitle>Golden paths</CardTitle><div className="text-xs">{paths?.golden_paths?.map((p: any) => p.path_name).join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Orphaned capabilities</CardTitle><div className="text-xs">{ownership?.orphaned_capability?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Documentation/test gaps</CardTitle><div className="text-xs">Missing tests: {ownership?.missing_tests?.join(" | ") ?? "..."} | Missing README docs: {ownership?.missing_readme_documentation?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Safety boundary</CardTitle><p className="text-xs text-muted">Platform catalog governance is advisory-only and no-execution. No auto-create files, no auto-delete capabilities, no auto-change ownership, no auto-register routers, and no auto-run migrations.</p></Card>
  </div>;
}
