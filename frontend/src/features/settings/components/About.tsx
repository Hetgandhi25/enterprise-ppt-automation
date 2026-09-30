import { Server, Shield, Code, Cpu } from "lucide-react";
import { AppMode } from "../../../types/settings";
import { useSettingsStore } from "../../../stores/useSettingsStore";

export function About() {
  const { appMode } = useSettingsStore();

  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-medium text-foreground">About</h3>
        <p className="text-sm text-muted-foreground">Application information and build details.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 max-w-3xl">
        <div className="p-4 bg-card border border-border rounded-xl flex gap-4">
          <div className="w-10 h-10 rounded-full bg-primary/10 text-primary flex items-center justify-center shrink-0">
            <Shield size={20} />
          </div>
          <div>
            <p className="text-sm font-medium text-foreground">PPT Automation Portal</p>
            <p className="text-xs text-muted-foreground">Version 1.0.0 (Build 4920)</p>
          </div>
        </div>

        <div className="p-4 bg-card border border-border rounded-xl flex gap-4">
          <div className="w-10 h-10 rounded-full bg-blue-500/10 text-blue-500 flex items-center justify-center shrink-0">
            <Code size={20} />
          </div>
          <div>
            <p className="text-sm font-medium text-foreground">Frontend Framework</p>
            <p className="text-xs text-muted-foreground">React 19.0.0 • Vite • TypeScript</p>
          </div>
        </div>

        <div className="p-4 bg-card border border-border rounded-xl flex gap-4">
          <div className="w-10 h-10 rounded-full bg-emerald-500/10 text-emerald-500 flex items-center justify-center shrink-0">
            <Server size={20} />
          </div>
          <div>
            <p className="text-sm font-medium text-foreground">Backend Services</p>
            <p className="text-xs text-muted-foreground">{appMode === AppMode.PRODUCTION ? 'FastAPI Connected' : 'Mock Services (Offline)'}</p>
          </div>
        </div>

        <div className="p-4 bg-card border border-border rounded-xl flex gap-4">
          <div className="w-10 h-10 rounded-full bg-purple-500/10 text-purple-500 flex items-center justify-center shrink-0">
            <Cpu size={20} />
          </div>
          <div>
            <p className="text-sm font-medium text-foreground">Environment</p>
            <p className="text-xs text-muted-foreground">Development / local</p>
          </div>
        </div>
      </div>
    </div>
  );
}
