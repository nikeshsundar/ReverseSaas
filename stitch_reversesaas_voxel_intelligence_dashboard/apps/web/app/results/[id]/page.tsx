"use client";

import * as React from "react";
import { useParams } from "next/navigation";
import {
  AlertTriangle,
  Download,
  Globe,
  Layers,
  LayoutGrid,
  Rocket,
  Search,
  Shield,
  TrendingUp
} from "lucide-react";

import { ArchitectureGraph } from "@/components/architecture-graph";
import { CostChart } from "@/components/cost-chart";
import { SectionHeading } from "@/components/section-heading";
import { ThemeToggle } from "@/components/theme-toggle";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Skeleton } from "@/components/ui/skeleton";
import { apiFetch } from "@/lib/api";
import { AnalysisResponse, TechnologySignal } from "@/lib/types";

export default function ResultsPage() {
  const params = useParams();
  const analysisId = params.id as string;
  const [analysis, setAnalysis] = React.useState<AnalysisResponse | null>(null);
  const [loading, setLoading] = React.useState(true);
  const [error, setError] = React.useState<string | null>(null);
  const [search, setSearch] = React.useState("");

  React.useEffect(() => {
    const load = async () => {
      try {
        const data = await apiFetch<AnalysisResponse>(`/api/analysis/${analysisId}`);
        setAnalysis(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Unable to load analysis.");
      } finally {
        setLoading(false);
      }
    };

    load();
  }, [analysisId]);

  const exportReport = async () => {
    const response = await fetch(`/api/report/${analysisId}`);
    if (!response.ok) {
      setError("Failed to download report.");
      return;
    }
    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `analysis-${analysisId}.pdf`;
    link.click();
    window.URL.revokeObjectURL(url);
  };

  const filteredFeatures = analysis?.features.filter((feature) =>
    feature.title.toLowerCase().includes(search.toLowerCase())
  );

  const filteredCompetitors = analysis?.competitors.filter((competitor) =>
    competitor.name.toLowerCase().includes(search.toLowerCase())
  );

  const stackSections = analysis?.technology_stack
    ? [
        { label: "Frontend", items: analysis.technology_stack.frontend },
        { label: "Backend", items: analysis.technology_stack.backend },
        { label: "Database", items: analysis.technology_stack.database },
        { label: "Hosting", items: analysis.technology_stack.hosting },
        { label: "Analytics", items: analysis.technology_stack.analytics },
        { label: "Payments", items: analysis.technology_stack.payments }
      ]
    : [];

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-background text-on-background">
        <Skeleton className="h-10 w-40" />
      </div>
    );
  }

  if (error || !analysis) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-background text-on-background">
        <div className="rounded-xl border border-error/40 bg-error/10 p-6 text-sm text-error">
          {error || "Analysis not available."}
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background text-on-background">
      <div className="flex">
        <aside className="hidden w-[260px] flex-col border-r border-outline-variant/30 bg-surface-container-low/90 p-6 md:flex">
          <div className="mb-8">
            <h1 className="text-lg font-semibold text-primary">ReverseSaaS</h1>
            <p className="text-xs uppercase tracking-[0.2em] text-on-surface-variant">
              Analysis complete
            </p>
          </div>
          <nav className="space-y-3 text-xs uppercase tracking-[0.2em] text-on-surface-variant">
            {[
              "overview",
              "technology",
              "features",
              "architecture",
              "competitors",
              "costs",
              "roadmap"
            ].map((section) => (
              <a
                key={section}
                href={`#${section}`}
                className="block rounded-DEFAULT px-3 py-2 hover:bg-surface-container-high hover:text-on-surface"
              >
                {section}
              </a>
            ))}
          </nav>
          <Button className="mt-auto" onClick={exportReport}>
            <Download className="h-4 w-4" />
            Export report
          </Button>
        </aside>

        <main className="flex-1 px-6 py-8">
          <div className="mb-8 flex flex-wrap items-center justify-between gap-4">
            <div>
              <h2 className="text-2xl font-semibold text-on-surface">
                {analysis.company_name || "Unknown Company"}
              </h2>
              <p className="text-sm text-on-surface-variant">{analysis.url}</p>
            </div>
            <div className="flex items-center gap-3">
              <div className="flex items-center gap-2 rounded-DEFAULT border border-outline-variant/40 bg-surface-container px-3 py-2">
                <Search className="h-4 w-4 text-on-surface-variant" />
                <Input
                  value={search}
                  onChange={(event) => setSearch(event.target.value)}
                  placeholder="Search insights"
                  className="h-6 border-none bg-transparent px-0 text-xs focus-visible:ring-0"
                />
              </div>
              <ThemeToggle />
            </div>
          </div>

          <section id="overview" className="mb-12">
            <SectionHeading
              title="Overview"
              subtitle="High-level understanding of the startup and market fit."
              icon={Globe}
            />
            <div className="grid gap-6 md:grid-cols-3">
              <Card>
                <CardHeader>
                  <CardTitle>Summary</CardTitle>
                </CardHeader>
                <CardContent className="text-sm text-on-surface-variant">
                  {analysis.ai_insights?.startup_summary ||
                    analysis.description ||
                    "Summary not available yet."}
                </CardContent>
              </Card>
              <Card>
                <CardHeader>
                  <CardTitle>Target Customers</CardTitle>
                </CardHeader>
                <CardContent className="text-sm text-on-surface-variant">
                  {analysis.ai_insights?.target_customers || ""}
                </CardContent>
              </Card>
              <Card>
                <CardHeader>
                  <CardTitle>Market Category</CardTitle>
                </CardHeader>
                <CardContent className="text-sm text-on-surface-variant">
                  {analysis.ai_insights?.market_category || analysis.industry}
                </CardContent>
              </Card>
            </div>
          </section>

          <section id="technology" className="mb-12">
            <SectionHeading
              title="Technology Stack"
              subtitle="Detected frameworks and infrastructure signals."
              icon={Layers}
            />
            <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-3">
              {stackSections.map((section) => (
                <Card key={section.label}>
                  <CardHeader>
                    <CardTitle className="text-base">{section.label}</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-3">
                    {section.items.length === 0 ? (
                      <p className="text-xs text-on-surface-variant">No signal detected.</p>
                    ) : (
                      section.items.map((item: TechnologySignal) => (
                        <div key={item.name} className="flex items-center justify-between">
                          <span className="text-sm text-on-surface">{item.name}</span>
                          <Badge>{Math.round(item.confidence * 100)}%</Badge>
                        </div>
                      ))
                    )}
                  </CardContent>
                </Card>
              ))}
            </div>
          </section>

          <section id="features" className="mb-12">
            <SectionHeading
              title="Core Features"
              subtitle="AI distilled capabilities and differentiators."
              icon={LayoutGrid}
            />
            <div className="grid gap-4 md:grid-cols-2">
              {filteredFeatures && filteredFeatures.length > 0 ? (
                filteredFeatures.map((feature) => (
                  <Card key={feature.title}>
                    <CardHeader>
                      <CardTitle className="text-base">{feature.title}</CardTitle>
                    </CardHeader>
                    <CardContent className="text-sm text-on-surface-variant">
                      {feature.description}
                    </CardContent>
                  </Card>
                ))
              ) : (
                <div className="rounded-xl border border-outline-variant/40 bg-surface-container/70 p-6 text-sm text-on-surface-variant">
                  No feature data available yet.
                </div>
              )}
            </div>
          </section>

          <section id="architecture" className="mb-12">
            <SectionHeading
              title="Architecture"
              subtitle="Predicted topology based on detected stack signals."
              icon={Shield}
            />
            <ArchitectureGraph graph={analysis.architecture} />
          </section>

          <section id="competitors" className="mb-12">
            <SectionHeading
              title="Competitors"
              subtitle="Top rivals and alternative approaches in the market."
              icon={AlertTriangle}
            />
            <div className="grid gap-4 md:grid-cols-2">
              {filteredCompetitors && filteredCompetitors.length > 0 ? (
                filteredCompetitors.map((competitor) => (
                  <Card key={competitor.name}>
                    <CardHeader>
                      <CardTitle className="text-base">{competitor.name}</CardTitle>
                    </CardHeader>
                    <CardContent className="text-sm text-on-surface-variant">
                      {competitor.description}
                    </CardContent>
                  </Card>
                ))
              ) : (
                <div className="rounded-xl border border-outline-variant/40 bg-surface-container/70 p-6 text-sm text-on-surface-variant">
                  Competitor data is still being compiled.
                </div>
              )}
            </div>
          </section>

          <section id="costs" className="mb-12">
            <SectionHeading
              title="Cost Estimates"
              subtitle="Infrastructure projections across growth tiers."
              icon={TrendingUp}
            />
            <Card>
              <CardContent>
                <CostChart costs={analysis.cost_estimate} />
              </CardContent>
            </Card>
          </section>

          <section id="roadmap" className="mb-12">
            <SectionHeading
              title="Roadmap"
              subtitle="AI-generated strategic roadmap for scaling."
              icon={Rocket}
            />
            <div className="grid gap-4 md:grid-cols-2">
              {analysis.ai_insights?.roadmap && analysis.ai_insights.roadmap.length > 0 ? (
                analysis.ai_insights.roadmap.map((item) => (
                  <Card key={item}>
                    <CardContent className="text-sm text-on-surface-variant">
                      {item}
                    </CardContent>
                  </Card>
                ))
              ) : (
                <div className="rounded-xl border border-outline-variant/40 bg-surface-container/70 p-6 text-sm text-on-surface-variant">
                  Roadmap insights pending.
                </div>
              )}
            </div>
          </section>
        </main>
      </div>
    </div>
  );
}
