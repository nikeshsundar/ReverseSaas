interface LoadingStepsProps {
  currentStep: number;
}

const STEPS = [
  { title: "Crawling Website", description: "Mapping key pages" },
  { title: "Detecting Stack", description: "Scanning scripts and headers" },
  { title: "Generating Insights", description: "Summarizing business model" },
  { title: "Building Architecture", description: "Predicting infrastructure" },
  { title: "Estimating Costs", description: "Computing spend tiers" }
];

export function LoadingSteps({ currentStep }: LoadingStepsProps) {
  return (
    <div className="space-y-6">
      {STEPS.map((step, index) => {
        const status =
          index < currentStep ? "done" : index === currentStep ? "active" : "pending";

        return (
          <div key={step.title} className="flex items-start gap-4">
            <div className="mt-1 flex flex-col items-center">
              <div
                className={`flex h-6 w-6 items-center justify-center rounded-full border ${
                  status === "done"
                    ? "border-primary/60 bg-primary/20 text-primary"
                    : status === "active"
                    ? "border-primary bg-surface-container text-primary shadow-[0_0_12px_rgba(78,222,163,0.4)]"
                    : "border-outline-variant/60 bg-surface-container text-on-surface-variant"
                }`}
              >
                {status === "done" ? "OK" : "-"}
              </div>
              {index < STEPS.length - 1 ? (
                <div className="h-8 w-px bg-outline-variant/40" />
              ) : null}
            </div>
            <div>
              <h3 className="text-xs font-semibold uppercase tracking-[0.2em] text-on-surface">
                {step.title}
              </h3>
              <p className="mt-1 text-xs text-on-surface-variant">{step.description}</p>
            </div>
          </div>
        );
      })}
    </div>
  );
}
