"use client";

import * as React from "react";
import { useRouter } from "next/navigation";
import { Link2, Loader2 } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

export function AnalysisForm() {
  const [url, setUrl] = React.useState("");
  const [error, setError] = React.useState<string | null>(null);
  const [loading, setLoading] = React.useState(false);
  const router = useRouter();

  const onSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError(null);
    setLoading(true);
    const trimmed = url.trim();

    try {
      const response = await fetch("/api/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: trimmed })
      });

      if (!response.ok) {
        const payload = await response.json().catch(() => ({}));
        throw new Error(payload.detail || "Analysis failed. Try again.");
      }

      const payload = await response.json();
      router.push(`/loading?id=${payload.id}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unexpected error.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={onSubmit} className="w-full max-w-3xl">
      <div className="glass-panel input-glow flex flex-col gap-3 rounded-xl border border-outline-variant/40 p-3 sm:flex-row">
        <div className="flex flex-1 items-center gap-2 rounded-lg bg-[#050505] px-4 py-3">
          <Link2 className="h-4 w-4 text-primary" />
          <Input
            type="url"
            placeholder="https://target-startup.com"
            className="h-8 border-none bg-transparent px-0 text-base text-on-surface focus-visible:ring-0"
            value={url}
            onChange={(event) => setUrl(event.target.value)}
            required
          />
        </div>
        <Button
          type="submit"
          size="lg"
          className="btn-warp whitespace-nowrap"
          disabled={loading || !url.trim()}
        >
          {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : null}
          {loading ? "Analyzing" : "Analyze Startup"}
        </Button>
      </div>
      {error ? (
        <p className="mt-3 text-sm text-error">{error}</p>
      ) : (
        <p className="mt-3 text-xs text-on-surface-variant">
          No credit card required. Reports generated in seconds.
        </p>
      )}
    </form>
  );
}
