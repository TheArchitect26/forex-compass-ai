"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Card, CardTitle } from "@/components/ui";

export default function TrustCalibrationPage() {
  const [status, setStatus] = useState<any>(null);
  const [credibility, setCredibility] = useState<any>(null);
  const [legitimacy, setLegitimacy] = useState<any>(null);
  const [uncertainty, setUncertainty] = useState<any>(null);
  const [overreach, setOverreach] = useState<any>(null);

  useEffect(() => {
    api("/api/trust-calibration/status").then(setStatus);
    api("/api/trust-calibration/credibility-audit", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setCredibility);
    api("/api/trust-calibration/recommendation-legitimacy", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setLegitimacy);
    api("/api/trust-calibration/uncertainty-audit", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setUncertainty);
    api("/api/trust-calibration/overreach-scan", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }).then(setOverreach);
  }, []);

  return <div className="space-y-4">
    <h1 className="text-xl font-semibold">Trust Calibration</h1>
    <Card><CardTitle>Credibility scores</CardTitle><div className="text-xs">Credibility: {status?.institutional_credibility_score ?? "..."} | Legitimacy: {status?.recommendation_legitimacy_score ?? "..."} | Calibration: {status?.confidence_calibration_score ?? "..."}</div></Card>
    <Card><CardTitle>Legitimacy reviews</CardTitle><div className="text-xs">Evidence: {legitimacy?.evidence_strength ?? "..."} | Proportionality: {legitimacy?.proportionality ?? "..."} | Burden: {legitimacy?.operator_burden ?? "..."}</div></Card>
    <Card><CardTitle>Uncertainty audit</CardTitle><div className="text-xs">Facts: {uncertainty?.facts?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Overreach warnings</CardTitle><div className="text-xs">{overreach?.excessive_confidence?.join(" | ") ?? "..."}</div></Card>
    <Card><CardTitle>Trust pressure indicators</CardTitle><div className="text-xs">Trust pressure: {status?.operator_trust_pressure_score ?? "..."} | False alarms: {credibility?.false_alarm_burden ?? "..."} | Missed warnings: {credibility?.missed_warning_burden ?? "..."}</div></Card>
    <Card><CardTitle>Usefulness credibility</CardTitle><div className="text-xs">Usefulness: {status?.usefulness_credibility_score ?? "..."} | Humility integrity: {status?.humility_integrity_score ?? "..."}</div></Card>
    <Card><CardTitle>Human review requirement</CardTitle><p className="text-xs text-muted">Legitimacy and confidence decisions require human review before adoption.</p></Card>
    <Card><CardTitle>Safety boundary</CardTitle><p className="text-xs text-muted">Trust calibration is advisory-only and no-execution; recommendations never auto-apply or override operator judgment.</p></Card>
  </div>;
}
