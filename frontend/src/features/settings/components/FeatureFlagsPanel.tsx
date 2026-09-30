import { useSettingsStore } from "../../../stores/useSettingsStore";

export function FeatureFlagsPanel() {
  const { featureFlags, updateFeatureFlags } = useSettingsStore();

  const flags = [
    { id: "enableCharts", label: "Charts Generation", desc: "Generate image charts using Recharts/Matplotlib." },
    { id: "enablePpt", label: "PPT Compilation", desc: "Build the final .pptx presentation." },
    { id: "enableMetrics", label: "Performance Metrics", desc: "Calculate runtime statistics per pipeline stage." },
    { id: "enableLogging", label: "Detailed Logging", desc: "Emit verbose debug logs to file system." },
    { id: "enableCleanup", label: "Auto Cleanup", desc: "Automatically delete downloaded Excel files." },
    { id: "experimentalFeatures", label: "Experimental Features", desc: "Enable beta UI capabilities and layouts." },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-medium text-foreground">Feature Flags</h3>
        <p className="text-sm text-muted-foreground">Toggle internal capabilities for debugging or development.</p>
      </div>

      <div className="space-y-4 max-w-xl">
        {flags.map(flag => (
          <label key={flag.id} className="flex items-start justify-between gap-4 p-4 rounded-lg border border-border bg-card hover:bg-muted/50 cursor-pointer transition-colors group">
            <div>
              <p className="text-sm font-medium text-foreground group-hover:text-primary transition-colors">{flag.label}</p>
              <p className="text-xs text-muted-foreground">{flag.desc}</p>
            </div>
            <div className="relative inline-block w-10 h-6 rounded-full shrink-0">
              <input 
                type="checkbox" 
                checked={(featureFlags as any)[flag.id]}
                onChange={(e) => updateFeatureFlags({ [flag.id]: e.target.checked })}
                className="peer sr-only"
              />
              <div className="w-10 h-6 bg-muted peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary"></div>
            </div>
          </label>
        ))}
      </div>
    </div>
  );
}
