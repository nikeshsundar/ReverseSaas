import { ArchitectureGraphData } from "@/lib/types";

interface ArchitectureGraphProps {
  graph: ArchitectureGraphData | null | undefined;
}

export function ArchitectureGraph({ graph }: ArchitectureGraphProps) {
  if (!graph || graph.nodes.length === 0) {
    return (
      <div className="flex h-[280px] items-center justify-center rounded-xl border border-outline-variant/40 bg-surface-container">
        <p className="text-sm text-on-surface-variant">Architecture data is still processing.</p>
      </div>
    );
  }

  const xs = graph.nodes.map((node) => node.x);
  const ys = graph.nodes.map((node) => node.y);
  const minX = Math.min(...xs);
  const maxX = Math.max(...xs);
  const minY = Math.min(...ys);
  const maxY = Math.max(...ys);

  const normalize = (value: number, min: number, max: number) =>
    max - min === 0 ? 50 : ((value - min) / (max - min)) * 100;

  const nodes = graph.nodes.map((node) => ({
    ...node,
    left: normalize(node.x, minX, maxX),
    top: normalize(node.y, minY, maxY)
  }));

  return (
    <div className="relative h-[320px] overflow-hidden rounded-xl border border-outline-variant/40 bg-surface-container">
      <svg className="absolute inset-0 h-full w-full" xmlns="http://www.w3.org/2000/svg">
        {graph.edges.map((edge) => {
          const source = nodes.find((node) => node.id === edge.source);
          const target = nodes.find((node) => node.id === edge.target);
          if (!source || !target) {
            return null;
          }
          return (
            <line
              key={edge.id}
              x1={`${source.left}%`}
              y1={`${source.top}%`}
              x2={`${target.left}%`}
              y2={`${target.top}%`}
              stroke="rgba(78, 222, 163, 0.35)"
              strokeWidth="2"
              strokeDasharray="6 6"
            />
          );
        })}
      </svg>
      {nodes.map((node) => (
        <div
          key={node.id}
          className="absolute flex flex-col items-center rounded-lg border border-outline-variant/50 bg-[#0b0b0b] px-3 py-2 text-xs text-on-surface shadow-[0_0_18px_rgba(78,222,163,0.15)]"
          style={{ left: `${node.left}%`, top: `${node.top}%`, transform: "translate(-50%, -50%)" }}
        >
          <span className="text-primary/80">{node.category}</span>
          <span className="font-semibold text-on-surface">{node.label}</span>
        </div>
      ))}
    </div>
  );
}
