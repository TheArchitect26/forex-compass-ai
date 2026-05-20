"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { LineChart, Radar, Newspaper, NotebookPen, FlaskConical, Brain, Settings, BarChart3, Activity } from "lucide-react";
import clsx from "clsx";

const nav = [
  { href: "/", label: "Dashboard", icon: LineChart },
  { href: "/scanner", label: "Market Scanner", icon: Radar },
  { href: "/signals", label: "Signals", icon: Activity },
  { href: "/analysis", label: "AI Analysis", icon: Brain },
  { href: "/calendar", label: "Calendar & News", icon: Newspaper },
  { href: "/journal", label: "Trade Journal", icon: NotebookPen },
  { href: "/backtest", label: "Backtesting", icon: FlaskConical },
  { href: "/performance", label: "Performance", icon: BarChart3 },
  { href: "/portfolio", label: "Portfolio Lab", icon: BarChart3 },
  { href: "/research", label: "Research Center", icon: FlaskConical },
  { href: "/operator", label: "Operator Center", icon: Settings },
  { href: "/executive", label: "Executive Console", icon: Brain },
  { href: "/trust", label: "Trust & Governance", icon: Settings },
  { href: "/reality", label: "Reality Console", icon: Brain },
  { href: "/personal-alignment", label: "Personal Alignment", icon: Brain },
  { href: "/attention", label: "Attention & Focus", icon: Brain },
  { href: "/temporal", label: "Temporal Intelligence", icon: Brain },
  { href: "/synthesis", label: "Strategic Synthesis", icon: Brain },
  { href: "/foresight", label: "Foresight", icon: Brain },
  { href: "/scenario", label: "Scenario Lab", icon: Brain },
  { href: "/pathways", label: "Strategic Pathways", icon: Brain },
  { href: "/causal", label: "Causal Intelligence", icon: Brain },
  { href: "/ecosystem", label: "Ecosystem", icon: Brain },
  { href: "/epistemic", label: "Epistemic Console", icon: Brain },
  { href: "/sovereignty", label: "Sovereignty Console", icon: Settings },
  { href: "/longevity", label: "Longevity Console", icon: Brain },
  { href: "/renewal", label: "Renewal Console", icon: FlaskConical },
  { href: "/meta", label: "Meta-Operations", icon: Brain },
  { href: "/orientation", label: "Orientation Console", icon: Brain },
  { href: "/mission", label: "Mission Console", icon: Settings },
  { href: "/learning", label: "Institutional Learning", icon: Brain },
  { href: "/settings", label: "Settings", icon: Settings },
];

export default function Sidebar() {
  const path = usePathname();
  return (
    <aside className="hidden md:flex w-60 flex-col bg-panel border-r border-border h-screen sticky top-0">
      <div className="px-5 py-5 border-b border-border">
        <div className="text-accent font-bold tracking-wide">FX·AI</div>
        <div className="text-xs text-muted">Market Intelligence</div>
      </div>
      <nav className="flex-1 px-2 py-3 space-y-1 overflow-y-auto">
        {nav.map(({ href, label, icon: Icon }) => {
          const active = path === href;
          return (
            <Link key={href} href={href}
              className={clsx("flex items-center gap-3 px-3 py-2 rounded-md text-sm",
                active ? "bg-panel2 text-accent" : "text-muted hover:text-text hover:bg-panel2")}>
              <Icon size={16} /> {label}
            </Link>
          );
        })}
      </nav>
      <div className="px-4 py-3 text-[10px] text-muted border-t border-border">
        Signal-only. Never auto-trades. Always verify before executing.
      </div>
    </aside>
  );
}
