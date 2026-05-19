export const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function api<T = any>(path: string, init?: RequestInit): Promise<T> {
  const r = await fetch(`${API}${path}`, { cache: "no-store", ...init });
  if (!r.ok) throw new Error(`${r.status} ${r.statusText}`);
  return r.json();
}
