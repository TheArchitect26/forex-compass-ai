"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Card, CardTitle } from "@/components/ui";

export default function ReleasePage() {
  const [status, setStatus] = useState<any>(null);
  const [readiness, setReadiness] = useState<any>(null);
  const [risk, setRisk] = useState<any>(null);
  const [rollback, setRollback] = useState<any>(null);
  const [review, setReview] = useState<any>(null);

  useEffect(() => {
    api("/api/release/status").then(setStatus);
    api("/api/release/readiness-check", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setReadiness);
    api("/api/release/build-risk", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setRisk);
    api("/api/release/rollback-plan", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setRollback);
    api("/api/release/post-release-review", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setReview);
  }, []);

  return <div className="space-y-4">
    <h1 className="text-xl font-semibold">Release</h1>
    <Card><CardTitle>Release readiness score</CardTitle><div className="text-xs">Readiness: {status?.release_readiness_score ?? "..."} | Build confidence: {status?.build_confidence_score ?? "..."} | Production suitability: {status?.production_suitability_score ?? "..."}</div></Card>
    <Card><CardTitle>Build/deployment risk</CardTitle><div className="text-xs">Deployment risk: {risk?.deployment_risk_score ?? "..."} | Migration risk: {risk?.migration_risk_score ?? "..."}</div></Card>
    <Card><CardTitle>Rollback plan</CardTitle><div className="text-xs">{rollback?.rollback_steps?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Environment readiness</CardTitle><div className="text-xs">Env readiness: {status?.environment_readiness_score ?? "..."} | Env vars documented: {readiness?.checklist?.required_env_vars_documented?.length ?? "..."}</div></Card>
    <Card><CardTitle>Post-release review</CardTitle><div className="text-xs">Build: {review?.build_result ?? "..."} | Deploy: {review?.deployment_result ?? "..."} | Runtime errors: {review?.runtime_errors?.length ?? "..."}</div></Card>
    <Card><CardTitle>Production-readiness checklist</CardTitle><div className="text-xs">Backend compile: {String(readiness?.checklist?.backend_compiles)} | Frontend build: {String(readiness?.checklist?.frontend_builds)} | Tests: {String(readiness?.checklist?.tests_pass)}</div></Card>
    <Card><CardTitle>Safety boundary</CardTitle><p className="text-xs text-muted">Advisory-only release governance. No auto-deploy, no auto-rollback, no auto-migrations, no auto-env changes, and no trade execution.</p></Card>
  </div>;
}
