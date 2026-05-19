"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Card, CardTitle } from "@/components/ui";
import clsx from "clsx";

export default function CalendarPage() {
  const [events, setEvents] = useState<any[]>([]);
  const [heads, setHeads] = useState<any[]>([]);
  const [senti, setSenti] = useState<any>(null);
  useEffect(() => { (async () => {
    setEvents(await api(`/api/news/calendar`));
    setHeads(await api(`/api/news/headlines`));
    setSenti(await api(`/api/sentiment`));
  })(); }, []);
  return (
    <div className="space-y-4">
      <h1 className="text-xl font-semibold">Calendar & News</h1>

      {senti && (
        <Card>
          <CardTitle>Aggregate market sentiment</CardTitle>
          <div className="flex items-center gap-4">
            <div className="text-3xl font-semibold capitalize">{senti.label}</div>
            <div className="text-sm text-muted">Score {senti.score?.toFixed?.(2)} · {senti.sample_size} headlines</div>
          </div>
        </Card>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <Card>
          <CardTitle>Economic calendar</CardTitle>
          <ul className="space-y-2 text-sm">
            {events.map((e, i) => (
              <li key={i} className="flex justify-between border-b border-border pb-2">
                <div>
                  <div>{e.event || e.Event}</div>
                  <div className="text-xs text-muted">{e.currency || e.Country} · {new Date(e.time || e.Date).toLocaleString()}</div>
                </div>
                <span className={clsx("text-xs px-2 py-0.5 rounded h-fit",
                  (e.impact || e.Importance) === "high" ? "bg-bear/20 text-bear" : "bg-panel2 text-muted")}>
                  {e.impact || e.Importance || "—"}
                </span>
              </li>
            ))}
            {events.length === 0 && <li className="text-xs text-muted">No events.</li>}
          </ul>
        </Card>

        <Card>
          <CardTitle>Market headlines</CardTitle>
          <ul className="space-y-2 text-sm">
            {heads.map((h, i) => (
              <li key={i} className="border-b border-border pb-2">
                <a className="hover:text-accent" href={h.link} target="_blank" rel="noreferrer">{h.title}</a>
                <div className="text-xs text-muted">{h.published}</div>
              </li>
            ))}
            {heads.length === 0 && <li className="text-xs text-muted">No headlines.</li>}
          </ul>
        </Card>
      </div>
    </div>
  );
}
