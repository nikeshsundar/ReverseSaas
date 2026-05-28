import { LucideIcon } from "lucide-react";

import { Badge } from "@/components/ui/badge";

interface SectionHeadingProps {
  title: string;
  subtitle?: string;
  icon?: LucideIcon;
  badge?: string;
}

export function SectionHeading({ title, subtitle, icon: Icon, badge }: SectionHeadingProps) {
  return (
    <div className="mb-6 flex flex-wrap items-center justify-between gap-4">
      <div>
        <div className="flex items-center gap-3">
          {Icon ? <Icon className="h-5 w-5 text-primary" /> : null}
          <h2 className="text-2xl font-semibold text-on-surface">{title}</h2>
        </div>
        {subtitle ? (
          <p className="mt-2 text-sm text-on-surface-variant">{subtitle}</p>
        ) : null}
      </div>
      {badge ? <Badge>{badge}</Badge> : null}
    </div>
  );
}
