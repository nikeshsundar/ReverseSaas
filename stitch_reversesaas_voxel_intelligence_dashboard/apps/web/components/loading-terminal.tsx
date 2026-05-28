"use client";

import * as React from "react";

const LOGS = [
  "[SYSTEM] Initializing reverse-engineering protocol...",
  "[CRAWL] Fetching robots.txt rules... OK.",
  "[CRAWL] Mapping domain structure...",
  "[DISCOVER] Parsing main JS bundles...",
  "[ANALYZE] Detecting frameworks...",
  "[AI] Synthesizing business insights...",
  "[COST] Estimating infrastructure spend..."
];

export function LoadingTerminal() {
  const [lines, setLines] = React.useState<string[]>([LOGS[0]]);

  React.useEffect(() => {
    let index = 1;
    const timer = setInterval(() => {
      setLines((prev) => {
        const next = [...prev, LOGS[index]];
        return next;
      });
      index += 1;
      if (index >= LOGS.length) {
        clearInterval(timer);
      }
    }, 900);

    return () => clearInterval(timer);
  }, []);

  return (
    <div className="terminal-scan flex h-full flex-col overflow-y-auto rounded-lg border border-outline-variant/40 bg-black p-4 text-xs text-primary/80">
      {lines.map((line, idx) => (
        <div key={`${line}-${idx}`} className="opacity-80">
          {line}
        </div>
      ))}
      <div className="mt-2 flex items-center gap-2 text-primary">
        <span>&gt;</span>
        <span className="animate-pulse">_</span>
      </div>
    </div>
  );
}
