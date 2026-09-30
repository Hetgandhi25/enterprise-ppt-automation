import { useFormContext, useWatch } from "react-hook-form";
import { GenerateFormValues } from "../validation";
import { FileText, Clock, AlertTriangle } from "lucide-react";
import { useSettingsStore } from "../../../stores/useSettingsStore";
import { cn } from "../../../utils/cn";

export function GenerateSummaryCard() {
  const { control } = useFormContext<GenerateFormValues>();
  const values = useWatch({ control });
  const { appMode } = useSettingsStore();

  const isReady = values.customerName && values.reportMonth && values.selectedServiceIds && values.selectedServiceIds.length > 0;

  return (
    <div className="bg-card border border-border rounded-xl p-6 shadow-sm sticky top-24">
      <h3 className="text-lg font-semibold text-foreground mb-4">Job Summary</h3>
      
      <div className="space-y-4 text-sm">
        <div className="flex justify-between items-center py-2 border-b border-border/50">
          <span className="text-muted-foreground">Target Customer</span>
          <span className="font-medium text-foreground">{values.customerName || "Not Selected"}</span>
        </div>
        
        <div className="flex justify-between items-center py-2 border-b border-border/50">
          <span className="text-muted-foreground">Report Month</span>
          <span className="font-medium text-foreground">{values.reportMonth || "Not Selected"}</span>
        </div>

        <div className="flex justify-between items-center py-2 border-b border-border/50">
          <span className="text-muted-foreground">App Mode</span>
          <span className={cn("font-medium capitalize", appMode === "production" ? "text-destructive" : "text-emerald-500")}>
            {appMode}
          </span>
        </div>

        <div className="flex justify-between items-center py-2 border-b border-border/50">
          <span className="text-muted-foreground">Est. Runtime</span>
          <span className="font-medium text-foreground flex items-center gap-1">
            <Clock size={14} /> ~45 seconds
          </span>
        </div>
      </div>

      <div className="mt-8">
        <button
          type="submit"
          disabled={!isReady}
          className={cn(
            "w-full py-3 rounded-lg font-medium flex items-center justify-center gap-2 transition-all",
            isReady 
              ? "bg-primary text-primary-foreground hover:bg-primary/90 shadow-md"
              : "bg-muted text-muted-foreground cursor-not-allowed"
          )}
        >
          <FileText size={18} />
          Generate PPT
        </button>
      </div>

      {appMode === "demo" && (
        <div className="mt-4 p-3 bg-blue-500/10 text-blue-700 dark:text-blue-400 rounded-md flex gap-2 items-start text-xs">
          <AlertTriangle size={14} className="shrink-0 mt-0.5" />
          <p>Running in DEMO mode. No real CRM connection will be established. Dummy data will be used.</p>
        </div>
      )}
    </div>
  );
}
