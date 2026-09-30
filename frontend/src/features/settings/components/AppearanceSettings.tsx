import { useSettingsStore } from "../../../stores/useSettingsStore";
import { Monitor, Moon, Sun } from "lucide-react";

export function AppearanceSettings() {
  const { theme, setTheme, compactDensity, reduceMotion, updateSettings } = useSettingsStore();

  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-medium text-foreground">Appearance</h3>
        <p className="text-sm text-muted-foreground">Customize the look and feel of the application.</p>
      </div>

      <div className="space-y-6 max-w-xl">
        <div className="space-y-2">
          <label className="text-sm font-medium text-foreground block">Theme</label>
          <div className="grid grid-cols-3 gap-3">
            <button 
              onClick={() => setTheme("light")}
              className={`p-3 flex flex-col items-center gap-2 border rounded-md transition-colors ${theme === 'light' ? 'border-primary bg-primary/5 text-primary' : 'border-border bg-card text-muted-foreground hover:bg-muted'}`}
            >
              <Sun size={20} />
              <span className="text-xs font-medium">Light</span>
            </button>
            <button 
              onClick={() => setTheme("dark")}
              className={`p-3 flex flex-col items-center gap-2 border rounded-md transition-colors ${theme === 'dark' ? 'border-primary bg-primary/5 text-primary' : 'border-border bg-card text-muted-foreground hover:bg-muted'}`}
            >
              <Moon size={20} />
              <span className="text-xs font-medium">Dark</span>
            </button>
            <button 
              onClick={() => setTheme("system")}
              className={`p-3 flex flex-col items-center gap-2 border rounded-md transition-colors ${theme === 'system' ? 'border-primary bg-primary/5 text-primary' : 'border-border bg-card text-muted-foreground hover:bg-muted'}`}
            >
              <Monitor size={20} />
              <span className="text-xs font-medium">System</span>
            </button>
          </div>
        </div>

        <div className="space-y-4 pt-4 border-t border-border">
          <label className="flex items-center gap-3 cursor-pointer group">
            <input 
              type="checkbox" 
              checked={compactDensity}
              onChange={(e) => updateSettings({ compactDensity: e.target.checked })}
              className="rounded text-primary focus:ring-primary w-4 h-4 cursor-pointer"
            />
            <div>
              <p className="text-sm font-medium text-foreground group-hover:text-primary transition-colors">Compact Density</p>
              <p className="text-xs text-muted-foreground">Reduce padding and margins across the interface.</p>
            </div>
          </label>

          <label className="flex items-center gap-3 cursor-pointer group">
            <input 
              type="checkbox" 
              checked={reduceMotion}
              onChange={(e) => updateSettings({ reduceMotion: e.target.checked })}
              className="rounded text-primary focus:ring-primary w-4 h-4 cursor-pointer"
            />
            <div>
              <p className="text-sm font-medium text-foreground group-hover:text-primary transition-colors">Reduce Motion</p>
              <p className="text-xs text-muted-foreground">Disable non-essential animations and transitions.</p>
            </div>
          </label>
        </div>
      </div>
    </div>
  );
}
