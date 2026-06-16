const DIRECT_API =
  process.env.BACKEND_API_URL ||
  process.env.NEXT_PUBLIC_API_URL ||
  "http://127.0.0.1:8000";

export const API = typeof window === "undefined" ? DIRECT_API : "/api/backend";
export const AUTH_TOKEN_KEY = "forex_compass_access_token";

export function getAuthToken(): string | null {
  if (typeof window === "undefined") return null;
  return window.localStorage.getItem(AUTH_TOKEN_KEY);
}

export function setAuthToken(token: string): void {
  if (typeof window === "undefined") return;
  window.localStorage.setItem(AUTH_TOKEN_KEY, token);
}

export function clearAuthToken(): void {
  if (typeof window === "undefined") return;
  window.localStorage.removeItem(AUTH_TOKEN_KEY);
}

export async function api<T = any>(path: string, init?: RequestInit): Promise<T> {
  const headers = new Headers(init?.headers);
  const token = getAuthToken();

  if (token && !headers.has("authorization")) {
    headers.set("authorization", `Bearer ${token}`);
  }

  const r = await fetch(`${API}${path}`, {
    cache: "no-store",
    ...init,
    headers,
  });

  if (!r.ok) {
    let detail = "";
    try {
      const body = await r.json();
      detail = body?.detail ? `: ${body.detail}` : "";
    } catch {}

    if (r.status === 401) {
      clearAuthToken();
      detail = detail || ": Authentication required. Sign in at /login";
    }

    throw new Error(`${r.status} ${r.statusText}${detail}`);
  }

  return r.json();
}
