import { useSettingsStore } from "../../../stores/useSettingsStore";

export function AutomationSettings() {
  const { headless, retryCount, screenshot, parallelJobs, updateSettings } = useSettingsStore();

  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-medium text-foreground">Automation</h3>
        <p className="text-sm text-muted-foreground">Configure Playwright execution behaviors.</p>
      </div>

      <div className="space-y-6 max-w-xl">
        <label className="flex items-start gap-3 cursor-pointer group">
          <input 
            type="checkbox" 
            checked={headless}
            onChange={(e) => updateSettings({ headless: e.target.checked })}
            className="rounded text-primary focus:ring-primary w-4 h-4 mt-0.5"
          />
          <div>
            <p className="text-sm font-medium text-foreground group-hover:text-primary transition-colors">Headless Execution</p>
            <p className="text-xs text-muted-foreground">Run browser automation in the background without visible windows.</p>
          </div>
        </label>

        <label className="flex items-start gap-3 cursor-pointer group">
          <input 
            type="checkbox" 
            checked={screenshot}
            onChange={(e) => updateSettings({ screenshot: e.target.checked })}
            className="rounded text-primary focus:ring-primary w-4 h-4 mt-0.5"
          />
          <div>
            <p className="text-sm font-medium text-foreground group-hover:text-primary transition-colors">Capture Screenshots</p>
            <p className="text-xs text-muted-foreground">Take screenshots on failure to assist with debugging.</p>
          </div>
        </label>

        <div className="space-y-2 pt-4 border-t border-border">
          <label className="text-sm font-medium text-foreground block">Max Retry Count</label>
          <input 
            type="number" 
            min="0"
            max="5"
            value={retryCount}
            onChange={(e) => updateSettings({ retryCount: parseInt(e.target.value) || 0 })}
            className="w-full sm:w-32 h-10 px-3 bg-background border border-border rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-primary/20"
          />
          <p className="text-xs text-muted-foreground">Number of times to retry a failed extraction task.</p>
        </div>

        <div className="space-y-2">
          <label className="text-sm font-medium text-foreground block">Parallel Jobs (Mock)</label>
          <select 
            value={parallelJobs}
            onChange={(e) => updateSettings({ parallelJobs: parseInt(e.target.value) || 1 })}
            className="w-full sm:w-32 h-10 px-3 bg-background border border-border rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-primary/20"
          >
            {[1,2,3,4,5].map(n => <option key={n} value={n}>{n}</option>)}
          </select>
          <p className="text-xs text-muted-foreground">Maximum concurrent jobs to process at once.</p>
        </div>
      </div>
    </div>
  );
}
