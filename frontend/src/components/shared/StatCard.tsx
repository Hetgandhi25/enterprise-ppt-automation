import { ReactNode } from "react";
import { motion } from "framer-motion";
import { cn } from "../../utils/cn";

interface StatCardProps {
  title: string;
  value: string | number;
  icon: ReactNode;
  trend?: {
    value: string;
    isPositive: boolean;
  };
  className?: string;
}

export function StatCard({ title, value, icon, trend, className }: StatCardProps) {
  return (
    <motion.div
      whileHover={{ y: -2 }}
      className={cn("bg-card rounded-2xl p-6 shadow-sm flex flex-col justify-between", className)}
    >
      <div className="flex items-center justify-between mb-2">
        <h3 className="text-sm font-semibold text-muted-foreground">{title}</h3>
        {/* Optional icon if needed, though KimiDesk sometimes omits them in top metrics. We keep it soft. */}
        {icon && <div className="text-muted-foreground/50">{icon}</div>}
      </div>
      
      <div className="flex items-center gap-3 my-2">
        <h2 className="text-4xl font-bold text-foreground tracking-tight">{value}</h2>
        {trend && (
          <span
            className={cn(
              "text-xs font-semibold px-2 py-1 rounded-md flex items-center gap-1",
              trend.isPositive
                ? "text-primary bg-primary/10"
                : "text-destructive bg-destructive/10"
            )}
          >
            {trend.isPositive ? "↑" : "↓"} {trend.value}
          </span>
        )}
      </div>
      
      <p className="text-xs text-muted-foreground/80 mt-1">Compare to last month</p>
    </motion.div>
  );
}
