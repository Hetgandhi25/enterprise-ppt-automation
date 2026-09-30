import { useState } from "react";
import { useFormContext } from "react-hook-form";
import { GenerateFormValues } from "../validation";
import { ChevronDown, ChevronRight, Settings } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

export function AdvancedOptions() {
  const { register } = useFormContext<GenerateFormValues>();
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="border border-border rounded-xl bg-card overflow-hidden">
      <button 
        type="button" 
        onClick={() => setIsOpen(!isOpen)}
        className="w-full flex items-center justify-between p-4 bg-muted/30 hover:bg-muted/50 transition-colors"
      >
        <div className="flex items-center gap-2 font-medium text-foreground text-sm">
          <Settings size={16} />
          Advanced Options & Feature Flags
        </div>
        {isOpen ? <ChevronDown size={16} /> : <ChevronRight size={16} />}
      </button>

      <AnimatePresence>
        {isOpen && (
          <motion.div 
            initial={{ height: 0 }}
            animate={{ height: "auto" }}
            exit={{ height: 0 }}
            className="overflow-hidden"
          >
            <div className="p-6 grid grid-cols-1 sm:grid-cols-2 gap-6 border-t border-border">
              
              {/* Automation Settings */}
              <div className="space-y-4">
                <h4 className="text-xs font-semibold uppercase text-muted-foreground tracking-wider mb-2">Automation Options</h4>
                
                <label className="flex items-center gap-3">
                  <input type="checkbox" {...register("headless")} className="rounded text-primary focus:ring-primary w-4 h-4" />
                  <span className="text-sm text-foreground">Headless Mode (Background)</span>
                </label>
                
                <label className="flex items-center gap-3">
                  <span className="text-sm text-foreground w-24">Retry Count:</span>
                  <input type="number" {...register("retryCount", { valueAsNumber: true })} className="w-16 h-8 px-2 bg-background border border-border rounded-md text-sm" />
                </label>
              </div>

              {/* Feature Flags */}
              <div className="space-y-4">
                <h4 className="text-xs font-semibold uppercase text-muted-foreground tracking-wider mb-2">Feature Flags</h4>
                
                <label className="flex items-center gap-3">
                  <input type="checkbox" {...register("enableCharts")} className="rounded text-primary focus:ring-primary w-4 h-4" />
                  <span className="text-sm text-foreground">Generate Charts</span>
                </label>

                <label className="flex items-center gap-3">
                  <input type="checkbox" {...register("enablePpt")} className="rounded text-primary focus:ring-primary w-4 h-4" />
                  <span className="text-sm text-foreground">Generate PPT Output</span>
                </label>
                
                <label className="flex items-center gap-3">
                  <input type="checkbox" {...register("enableCleanup")} className="rounded text-primary focus:ring-primary w-4 h-4" />
                  <span className="text-sm text-foreground">Clean temporary files</span>
                </label>
              </div>

            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
