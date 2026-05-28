import * as React from "react";

import { cn } from "@/lib/utils";

export interface BadgeProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: "default" | "secondary" | "warning";
}

const variantClasses: Record<NonNullable<BadgeProps["variant"]>, string> = {
  default: "bg-primary/15 text-primary border border-primary/30",
  secondary: "bg-secondary/15 text-secondary border border-secondary/30",
  warning: "bg-tertiary/15 text-tertiary border border-tertiary/30",
};

const Badge = ({ className, variant = "default", ...props }: BadgeProps) => (
  <div
    className={cn(
      "inline-flex items-center rounded-DEFAULT px-2 py-1 text-xs uppercase tracking-[0.12em]",
      variantClasses[variant],
      className
    )}
    {...props}
  />
);

export { Badge };
