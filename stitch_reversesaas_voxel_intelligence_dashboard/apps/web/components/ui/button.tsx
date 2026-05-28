import * as React from "react";

import { cn } from "@/lib/utils";

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "ghost" | "outline" | "secondary";
  size?: "sm" | "md" | "lg" | "icon";
}

const variantClasses: Record<NonNullable<ButtonProps["variant"]>, string> = {
  primary:
    "bg-primary text-on-primary hover:brightness-110 shadow-[0_0_20px_rgba(78,222,163,0.2)]",
  ghost:
    "bg-transparent border border-outline-variant/40 text-on-surface-variant hover:text-on-surface hover:border-primary/50",
  outline:
    "border border-outline-variant/60 text-on-surface hover:bg-surface-container",
  secondary:
    "bg-surface-container text-on-surface hover:bg-surface-container-high",
};

const sizeClasses: Record<NonNullable<ButtonProps["size"]>, string> = {
  sm: "h-9 px-3 text-xs",
  md: "h-10 px-4 text-sm",
  lg: "h-12 px-6 text-base",
  icon: "h-9 w-9",
};

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = "primary", size = "md", ...props }, ref) => {
    return (
      <button
        ref={ref}
        className={cn(
          "inline-flex items-center justify-center gap-2 rounded-DEFAULT font-semibold transition-all",
          "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary/60",
          variantClasses[variant],
          sizeClasses[size],
          className
        )}
        {...props}
      />
    );
  }
);
Button.displayName = "Button";

export { Button };
