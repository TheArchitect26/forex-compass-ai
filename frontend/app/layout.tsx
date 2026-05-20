import "./globals.css";
import type { Metadata } from "next";
import Sidebar from "@/components/Sidebar";

export const metadata: Metadata = {
  title: "FX·AI — Market Intelligence",
  description: "Institutional-grade AI Forex analysis. Signals only — never auto-trades.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-bg text-text">
        <div className="flex min-h-screen">
          <Sidebar />
          <main className="flex-1 min-w-0">
            <header className="h-12 border-b border-border flex items-center px-4 justify-between bg-panel">
              <div className="text-sm text-muted">AI Forex Intelligence</div>
              <div className="flex items-center gap-2 text-xs">
                <span className="inline-block w-2 h-2 rounded-full bg-bull animate-pulse" />
                <span className="text-muted">Markets live</span>
              </div>
            </header>
            <div className="p-4 md:p-6">{children}</div>
            <div className="px-4 md:px-6 pb-4 text-xs text-muted">
              Personal signal assistant only. Not financial advice. Does not execute trades.
            </div>
          </main>
        </div>
      </body>
    </html>
  );
}
