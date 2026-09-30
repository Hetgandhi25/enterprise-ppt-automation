import { useSettingsStore } from "../../../stores/useSettingsStore";
import { AppMode } from "../../../types/settings";

export function GeneralSettings() {
  const { appMode, language, timezone, setAppMode, updateSettings } = useSettingsStore();

  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-medium text-foreground">General Settings</h3>
        <p className="text-sm text-muted-foreground">Manage your application mode and localization.</p>
      </div>

      <div className="space-y-4 max-w-xl">
        <div className="space-y-2">
          <label className="text-sm font-medium text-foreground block">Application Mode</label>
          <div className="flex bg-muted p-1 rounded-md">
            <button 
              onClick={() => setAppMode(AppMode.DEMO)}
              className={`flex-1 py-1.5 text-sm font-medium rounded ${appMode === AppMode.DEMO ? 'bg-background shadow text-foreground' : 'text-muted-foreground hover:text-foreground'}`}
            >
              Demo (Mock)
            </button>
            <button 
              onClick={() => setAppMode(AppMode.PRODUCTION)}
              className={`flex-1 py-1.5 text-sm font-medium rounded ${appMode === AppMode.PRODUCTION ? 'bg-background shadow text-foreground' : 'text-muted-foreground hover:text-foreground'}`}
            >
              Production (FastAPI)
            </button>
          </div>
        </div>

        <div className="space-y-2">
          <label className="text-sm font-medium text-foreground block">Language</label>
          <select 
            value={language}
            onChange={(e) => updateSettings({ language: e.target.value })}
            className="w-full h-10 px-3 bg-background border border-border rounded-md text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-primary/20"
          >
            <option value="en-US">English (US)</option>
            <option value="en-GB">English (UK)</option>
            <option value="fr-FR">French</option>
            <option value="de-DE">German</option>
          </select>
        </div>

        <div className="space-y-2">
          <label className="text-sm font-medium text-foreground block">Timezone</label>
          <select 
            value={timezone}
            onChange={(e) => updateSettings({ timezone: e.target.value })}
            className="w-full h-10 px-3 bg-background border border-border rounded-md text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-primary/20"
          >
            <option value="UTC">UTC (Coordinated Universal Time)</option>
            <option value="America/New_York">Eastern Time (ET)</option>
            <option value="Europe/London">Greenwich Mean Time (GMT)</option>
            <option value="Asia/Kolkata">India Standard Time (IST)</option>
          </select>
        </div>
      </div>
    </div>
  );
}
