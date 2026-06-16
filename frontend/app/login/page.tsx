"use client";

import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";
import { api, clearAuthToken, getAuthToken, setAuthToken } from "@/lib/api";
import { Card, CardTitle } from "@/components/ui";

type TokenResponse = {
  access_token: string;
  token_type: string;
};

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [mode, setMode] = useState<"login" | "register">("login");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const submit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setBusy(true);
    setError(null);

    try {
      const result = await api<TokenResponse>(`/api/auth/${mode}`, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      setAuthToken(result.access_token);

      const requested = new URLSearchParams(window.location.search).get("next");
      const destination = requested?.startsWith("/") ? requested : "/";
      router.push(destination);
      router.refresh();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Authentication failed.");
    } finally {
      setBusy(false);
    }
  };

  const signedIn = Boolean(getAuthToken());

  return (
    <div className="mx-auto max-w-md space-y-4">
      <div>
        <h1 className="text-xl font-semibold">Compass access</h1>
        <p className="mt-1 text-xs text-muted">
          Sign in before running protected scans or changing system settings.
        </p>
      </div>

      <Card>
        <CardTitle>{mode === "login" ? "Sign in" : "Create private account"}</CardTitle>

        <form onSubmit={submit} className="mt-4 space-y-3">
          <label className="block text-xs text-muted">
            Email
            <input
              type="email"
              autoComplete="email"
              required
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              className="mt-1 w-full rounded border border-border bg-panel2 px-3 py-2 text-sm text-text"
            />
          </label>

          <label className="block text-xs text-muted">
            Password
            <input
              type="password"
              autoComplete={mode === "login" ? "current-password" : "new-password"}
              minLength={8}
              required
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              className="mt-1 w-full rounded border border-border bg-panel2 px-3 py-2 text-sm text-text"
            />
          </label>

          {error && (
            <div className="rounded border border-bear/40 bg-bear/10 p-2 text-xs text-bear">
              {error}
            </div>
          )}

          <button
            type="submit"
            disabled={busy}
            className="w-full rounded bg-accent px-4 py-2 text-sm font-medium text-bg disabled:opacity-50"
          >
            {busy ? "Please wait…" : mode === "login" ? "Sign in" : "Create account"}
          </button>
        </form>

        <button
          type="button"
          onClick={() => {
            setMode(mode === "login" ? "register" : "login");
            setError(null);
          }}
          className="mt-3 text-xs text-accent hover:underline"
        >
          {mode === "login"
            ? "First time here? Create the private account"
            : "Already registered? Sign in"}
        </button>

        {signedIn && (
          <button
            type="button"
            onClick={() => {
              clearAuthToken();
              router.refresh();
            }}
            className="mt-3 block text-xs text-muted hover:text-text"
          >
            Clear the saved session
          </button>
        )}
      </Card>
    </div>
  );
}
