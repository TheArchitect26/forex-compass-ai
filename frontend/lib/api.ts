const DIRECT_API =
  process.env.BACKEND_API_URL ||
  process.env.NEXT_PUBLIC_API_URL ||
  "http://127.0.0.1:8000";

export const API = typeof window === "undefined" ? DIRECT_API : "/api/backend";

export async function api<T = any>(path: string, init?: RequestInit): Promise<T> {
  const r = await fetch(`${API}${path}`, { cache: "no-store", ...init });

  if (!r.ok) {
    let detail = "";
    try {
      const body = await r.json();
      detail = body?.detail ? `: ${body.detail}` : "";
    } catch {}

    throw new Error(`${r.status} ${r.statusText}${detail}`);
  }

  return r.json();
}
