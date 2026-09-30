import { TaskStatusEnum } from "../../types/taskStatus";
import { cn } from "../../utils/cn";

export function StatusBadge({ status }: { status: TaskStatusEnum }) {
  const getStyles = () => {
    switch (status) {
      case TaskStatusEnum.COMPLETED:
        return "bg-emerald-500/10 text-emerald-700 dark:text-emerald-400 border-emerald-500/20";
      case TaskStatusEnum.FAILED:
        return "bg-destructive/10 text-destructive dark:text-red-400 border-destructive/20";
      case TaskStatusEnum.PENDING:
        return "bg-muted text-muted-foreground border-border";
      default:
        return "bg-primary/10 text-primary border-primary/20";
    }
  };

  const getLabel = () => {
    return status.replace(/_/g, " ").toLowerCase();
  };

  return (
    <span
      className={cn(
        "px-2.5 py-0.5 rounded-full text-xs font-medium border capitalize whitespace-nowrap",
        getStyles()
      )}
    >
      {getLabel()}
    </span>
  );
}
