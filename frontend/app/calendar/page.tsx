"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Card, CardTitle } from "@/components/ui";
import clsx from "clsx";

export default function CalendarPage() {
  const [events, setEvents] = useState<any[]>([]);
  const [heads, setHeads] = useState<any[]>([]);
  const [senti, setSenti] = useState<any>(null);
  const [status, setStatus] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    (async () => {
      try {
        const [calendar, headlines, sentiment, providerStatus] = await Promise.all([
          api(`/api/news/calendar`),
          api(`/api/news/headlines`),
          api(`/api/sentiment`),
          api(`/api/news/status`),
        ]);
        setEvents(calendar);
        setHeads(headlines);
        setSenti(sentiment);
        setStatus(providerStatus);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Unable to load calendar and news.");
      }
    })();
  }, []);

  const calendarProvider = status?.calendar?.configured
    ? "Trading Economics"
    : "Not configured";
  const headlineProvider = status?.headlines?.finnhub_configured
    ? "Finnhub + RSS"
    : "RSS fallback";

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between gap-4 flex-wrap">
        <h1 className="text-xl font-semibold">Calendar & News</h1>
        <div className="text-xs text-muted">
          Calendar: {calendarProvider} · Headlines: {headlineProvider}
        </div>
      </div>

      {error && (
        <div className="text-xs text-bear bg-bear/10 border border-bear/40 rounded p-2">
          {error}
        </div>
      )}

      {senti && (
        <Card>
          <CardTitle>Aggregate market sentiment</CardTitle>
          <div className="flex items-center gap-4">
            <div className="text-3xl font-semibold capitalize">{senti.label}</div>
            <div className="text-sm text-muted">Score {senti.score?.toFixed?.(2)} · {senti.sample_size} headlines</div>
          </div>
          <div className="text-xs text-muted mt-2">
            Current sentiment is headline-based and should support—not override—the technical signal engine.
          </div>
        </Card>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <Card>
          <CardTitle>Economic calendar</CardTitle>
          <ul className="space-y-2 text-sm">
            {events.map((e, i) => (
              <li key={`${e.time}-${e.event}-${i}`} className="border-b border-border pb-2">
                <div className="flex justify-between gap-3">
                  <div>
                    <div>{e.event}</div>
                    <div className="text-xs text-muted">
                      {e.currency || e.country || "—"} · {e.time ? new Date(e.time).toLocaleString() : "Time unavailable"}
                    </div>
                  </div>
                  <span className={clsx(
                    "text-xs px-2 py-0.5 rounded h-fit capitalize",
                    e.impact === "high"
                      ? "bg-bear/20 text-bear"
                      : e.impact === "medium"
                        ? "bg-yellow-400/20 text-yellow-300"
                        : "bg-panel2 text-muted"
                  )}>
                    {e.impact || "unknown"}
                  </span>
                </div>
                <div className="grid grid-cols-3 gap-2 text-xs text-muted mt-2">
                  <div>Previous: <span className="text-foreground">{e.previous || "—"}</span></div>
                  <div>Forecast: <span className="text-foreground">{e.forecast || "—"}</span></div>
                  <div>Actual: <span className="text-foreground">{e.actual || "—"}</span></div>
                </div>
              </li>
            ))}
            {events.length === 0 && (
              <li className="text-xs text-muted">
                {status?.calendar?.configured
                  ? "No upcoming events returned by the calendar provider."
                  : "Trading Economics API is not configured yet. No placeholder events are shown."}
              </li>
            )}
          </ul>
        </Card>

        <Card>
          <CardTitle>Market headlines</CardTitle>
          <ul className="space-y-2 text-sm">
            {heads.map((h, i) => (
              <li key={`${h.link}-${i}`} className="border-b border-border pb-2">
                <a className="hover:text-accent" href={h.link} target="_blank" rel="noreferrer">{h.title}</a>
                <div className="text-xs text-muted flex justify-between gap-2 mt-1">
                  <span>{h.published || "Time unavailable"}</span>
                  <span>{h.source || h.provider || "market feed"}</span>
                </div>
              </li>
            ))}
            {heads.length === 0 && <li className="text-xs text-muted">No headlines available.</li>}
          </ul>
        </Card>
      </div>
    </div>
  );
}
