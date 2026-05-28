import { cn } from "@/lib/utils";

export function Skeleton({ className }: { className?: string }) {
  return (
    <div
      className={cn(
        "animate-pulse rounded-DEFAULT bg-surface-container-high/60",
        className
      )}
    />
  );
}
