import { Card, CardTitle } from "@/components/ui";
export default function Settings() {
  return (
    <div className="space-y-4">
      <h1 className="text-xl font-semibold">Settings</h1>
      <Card>
        <CardTitle>Environment</CardTitle>
        <p className="text-sm text-muted">API keys and notification webhooks are configured via the <code>.env</code> file at the repo root. See <code>.env.example</code>.</p>
      </Card>
      <Card>
        <CardTitle>Safety</CardTitle>
        <p className="text-sm">This system never executes trades. Every signal requires a human decision and manual execution in your broker.</p>
      </Card>
    </div>
  );
}
