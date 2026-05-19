import clsx from "clsx";
export function Card({ children, className }: { children: React.ReactNode; className?: string }) {
  return <div className={clsx("bg-panel border border-border rounded-lg p-4", className)}>{children}</div>;
}
export function CardTitle({ children }: { children: React.ReactNode }) {
  return <div className="text-xs uppercase tracking-wider text-muted mb-2">{children}</div>;
}
export function Stat({ label, value, sub, tone }: { label: string; value: React.ReactNode; sub?: string; tone?: "bull"|"bear"|"neutral" }) {
  return (
    <Card>
      <CardTitle>{label}</CardTitle>
      <div className={clsx("text-2xl font-semibold",
        tone === "bull" && "text-bull", tone === "bear" && "text-bear")}>{value}</div>
      {sub && <div className="text-xs text-muted mt-1">{sub}</div>}
    </Card>
  );
}
export function ConfidenceBar({ value }: { value: number }) {
  const color = value >= 75 ? "bg-bull" : value >= 55 ? "bg-accent" : "bg-bear";
  return (
    <div className="w-full h-2 bg-panel2 rounded overflow-hidden">
      <div className={clsx("h-full", color)} style={{ width: `${Math.min(100, Math.max(0, value))}%` }} />
    </div>
  );
}
