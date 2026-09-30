import { useSettingsStore } from "../../../stores/useSettingsStore";
import { Folder } from "lucide-react";

export function OutputSettings() {
  const { outputFolder, templateFolder, chartFolder, tempFolder, updateSettings } = useSettingsStore();

  const directories = [
    { id: "outputFolder", label: "Default Output Folder", val: outputFolder, desc: "Where final PPTs are saved." },
    { id: "templateFolder", label: "Template Folder", val: templateFolder, desc: "Where PPT templates are located." },
    { id: "chartFolder", label: "Chart Export Folder", val: chartFolder, desc: "Where intermediate charts are stored." },
    { id: "tempFolder", label: "Temporary Folder", val: tempFolder, desc: "Used for transient Excel downloads." },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-medium text-foreground">Output Directories</h3>
        <p className="text-sm text-muted-foreground">Configure paths for templates, temporary data, and final reports.</p>
      </div>

      <div className="space-y-6 max-w-2xl">
        {directories.map((dir) => (
          <div key={dir.id} className="space-y-2">
            <label className="text-sm font-medium text-foreground block">{dir.label}</label>
            <div className="flex gap-2">
              <div className="relative flex-1">
                <Folder size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground" />
                <input 
                  type="text"
                  value={dir.val}
                  onChange={(e) => updateSettings({ [dir.id]: e.target.value })}
                  className="w-full h-10 pl-9 pr-4 bg-background border border-border rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-primary/20"
                />
              </div>
              <button className="px-4 h-10 bg-muted hover:bg-muted/80 text-foreground text-sm font-medium rounded-md border border-border transition-colors">
                Browse
              </button>
            </div>
            <p className="text-xs text-muted-foreground">{dir.desc}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
