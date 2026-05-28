import { CostEstimateData } from "@/lib/types";

interface CostChartProps {
  costs: CostEstimateData | null | undefined;
}

export function CostChart({ costs }: CostChartProps) {
  if (!costs) {
    return (
      <div className="flex h-[200px] items-center justify-center rounded-xl border border-outline-variant/40 bg-surface-container">
        <p className="text-sm text-on-surface-variant">Cost data unavailable.</p>
      </div>
    );
  }

  const data = [
    { label: "100", total: costs.users_100.total },
    { label: "1K", total: costs.users_1000.total },
    { label: "10K", total: costs.users_10000.total },
    { label: "100K", total: costs.users_100000.total }
  ];
  const max = Math.max(...data.map((item) => item.total));

  return (
    <div className="grid h-[220px] grid-cols-4 items-end gap-4">
      {data.map((item) => (
        <div key={item.label} className="flex flex-col items-center gap-2">
          <div
            className="w-12 rounded-DEFAULT bg-primary/70"
            style={{ height: `${(item.total / max) * 160 + 20}px` }}
          />
          <span className="text-xs text-on-surface-variant">{item.label} users</span>
          <span className="text-sm font-semibold text-on-surface">${item.total}</span>
        </div>
      ))}
    </div>
  );
}
