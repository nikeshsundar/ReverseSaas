"use client";

import * as React from "react";
import { Suspense } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { Loader2 } from "lucide-react";

import { LoadingSteps } from "@/components/loading-steps";
import { LoadingTerminal } from "@/components/loading-terminal";
import { Button } from "@/components/ui/button";
import { apiFetch } from "@/lib/api";
import { AnalysisResponse } from "@/lib/types";

function LoadingContent() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const analysisId = searchParams.get("id");
  const [step, setStep] = React.useState(0);
  const [status, setStatus] = React.useState<AnalysisResponse | null>(null);
  const [error, setError] = React.useState<string | null>(null);

  React.useEffect(() => {
    const timer = setInterval(() => {
      setStep((prev) => (prev < 4 ? prev + 1 : prev));
    }, 2200);
    return () => clearInterval(timer);
  }, []);

  React.useEffect(() => {
    if (!analysisId) {
      return;
    }
    let interval: ReturnType<typeof setInterval> | null = null;

    const poll = async () => {
      try {
        const data = await apiFetch<AnalysisResponse>(`/api/analysis/${analysisId}`);
        setStatus(data);
        if (data.status === "completed") {
          router.push(`/results/${analysisId}`);
          if (interval) {
            clearInterval(interval);
          }
        }
        if (data.status === "failed") {
          setError(data.error || "Analysis failed.");
          if (interval) {
            clearInterval(interval);
          }
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : "Unable to fetch status.");
        if (interval) {
          clearInterval(interval);
        }
      }
    };

    poll();
    interval = setInterval(poll, 2500);
    return () => {
      if (interval) {
        clearInterval(interval);
      }
    };
  }, [analysisId, router]);

  if (!analysisId) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-background text-on-surface">
        Missing analysis id.
      </div>
    );
  }

  return (
    <div className="flex min-h-screen flex-col bg-background text-on-background md:flex-row">
      <aside className="w-full border-b border-outline-variant/30 bg-surface-container-low/90 p-6 md:w-[320px] md:border-b-0 md:border-r">
        <div className="mb-8">
          <h1 className="text-xl font-semibold text-primary">ReverseSaaS</h1>
          <p className="text-xs uppercase tracking-[0.2em] text-on-surface-variant">
            Analysis protocol initiated
          </p>
        </div>
        <LoadingSteps currentStep={step} />
        <div className="mt-6">
          <Button variant="ghost" className="w-full" onClick={() => router.push("/")}>
            Abort process
          </Button>
        </div>
      </aside>
      <main className="flex flex-1 flex-col gap-6 p-6">
        <div className="flex items-center gap-3">
          <Loader2 className="h-5 w-5 animate-spin text-primary" />
          <div>
            <h2 className="text-lg font-semibold text-on-surface">Running analysis</h2>
            <p className="text-xs text-on-surface-variant">
              {status?.status === "completed" ? "Finalizing report" : "Streaming live telemetry"}
            </p>
          </div>
        </div>
        {error ? (
          <div className="rounded-lg border border-error/40 bg-error/10 p-4 text-sm text-error">
            {error}
          </div>
        ) : null}
        <div className="flex flex-1 flex-col gap-6 md:flex-row">
          <div className="flex flex-1 items-center justify-center rounded-2xl border border-outline-variant/40 bg-surface-container/70 p-6">
            <div className="flex h-44 w-44 items-center justify-center rounded-full border border-primary/40 shadow-[0_0_30px_rgba(78,222,163,0.25)]">
              <div className="h-20 w-20 rounded-xl border border-primary/40 bg-primary/10 animate-pulse" />
            </div>
          </div>
          <div className="flex-1">
            <LoadingTerminal />
          </div>
        </div>
      </main>
    </div>
  );
}

export default function LoadingPage() {
  return (
    <Suspense fallback={
      <div className="flex min-h-screen items-center justify-center bg-background text-on-surface">
        Loading...
      </div>
    }>
      <LoadingContent />
    </Suspense>
  );
}
