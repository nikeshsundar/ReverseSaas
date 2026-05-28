import { ArrowRight, Layers, Network, Radar } from "lucide-react";

import { AnalysisForm } from "@/components/analysis-form";
import { AnimatedBackground } from "@/components/animated-background";
import { FadeUp } from "@/components/fade-up";
import { ThemeToggle } from "@/components/theme-toggle";
import { Button } from "@/components/ui/button";

const FEATURES = [
  {
    title: "Tech Stack Extraction",
    description: "Identify frameworks, vendors, and hidden integrations in seconds.",
    icon: Layers
  },
  {
    title: "Architecture Mapping",
    description: "Predict infrastructure topology and data flow with precision.",
    icon: Network
  },
  {
    title: "Market Intelligence",
    description: "Translate signals into positioning, revenue, and competitive insights.",
    icon: Radar
  }
];

export default function HomePage() {
  return (
    <div className="relative min-h-screen overflow-hidden obsidian-bg">
      <AnimatedBackground />
      <header className="sticky top-0 z-20 border-b border-outline-variant/30 bg-background/80 backdrop-blur-xl">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
          <div className="flex items-center gap-3 text-lg font-semibold text-primary">
            ReverseSaaS
          </div>
          <nav className="hidden items-center gap-6 text-xs uppercase tracking-[0.2em] text-on-surface-variant md:flex">
            <a href="#analysis" className="hover:text-on-surface">Analysis</a>
            <a href="#features" className="hover:text-on-surface">Features</a>
            <a href="#docs" className="hover:text-on-surface">Docs</a>
          </nav>
          <div className="flex items-center gap-3">
            <ThemeToggle />
            <Button variant="ghost" size="sm">
              Talk to sales
            </Button>
          </div>
        </div>
      </header>

      <main className="relative z-10">
        <section id="analysis" className="mx-auto flex max-w-6xl flex-col items-center px-6 py-20 text-center">
          <FadeUp>
            <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-primary/30 bg-primary/10 px-4 py-1 text-xs uppercase tracking-[0.35em] text-primary">
              System Online v2.4
            </div>
          </FadeUp>
          <FadeUp delay={0.1}>
            <h1 className="text-4xl font-semibold text-on-surface md:text-6xl">
              Reverse engineer any startup in minutes.
            </h1>
          </FadeUp>
          <FadeUp delay={0.2}>
            <p className="mt-6 max-w-2xl text-base text-on-surface-variant">
              Paste a URL and unlock stack intelligence, architecture predictions, cost
              estimates, and competitive positioning in one export-ready report.
            </p>
          </FadeUp>
          <FadeUp delay={0.3}>
            <div className="mt-10 flex w-full justify-center">
              <AnalysisForm />
            </div>
          </FadeUp>
          <FadeUp delay={0.4}>
            <div className="mt-6 flex items-center gap-3 text-xs uppercase tracking-[0.2em] text-on-surface-variant">
              <span>Instant insights</span>
              <ArrowRight className="h-3 w-3" />
              <span>Exportable reports</span>
              <ArrowRight className="h-3 w-3" />
              <span>AI-guided strategy</span>
            </div>
          </FadeUp>
        </section>

        <section
          id="features"
          className="mx-auto grid max-w-6xl grid-cols-1 gap-6 px-6 pb-20 md:grid-cols-3"
        >
          {FEATURES.map((feature) => (
            <div key={feature.title} className="voxel-card rounded-xl p-6 text-left">
              <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-lg bg-primary/10">
                <feature.icon className="h-5 w-5 text-primary" />
              </div>
              <h3 className="text-lg font-semibold text-on-surface">{feature.title}</h3>
              <p className="mt-2 text-sm text-on-surface-variant">{feature.description}</p>
            </div>
          ))}
        </section>

        <section id="docs" className="mx-auto max-w-6xl px-6 pb-24">
          <div className="rounded-2xl border border-outline-variant/40 bg-surface-container/80 p-8">
            <h2 className="text-2xl font-semibold text-on-surface">Built for technical teams</h2>
            <p className="mt-3 max-w-2xl text-sm text-on-surface-variant">
              ReverseSaaS blends real-world crawling, stack detection, and AI synthesis
              into a single operational dashboard. Export insights directly into decks,
              architecture reviews, and go-to-market briefs.
            </p>
            <Button className="mt-6" size="lg">
              View documentation
            </Button>
          </div>
        </section>
      </main>
    </div>
  );
}
