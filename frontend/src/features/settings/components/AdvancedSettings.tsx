import { useState } from "react";
import { DownloadCloud, UploadCloud, RefreshCcw, Trash2 } from "lucide-react";
import { ResetDialog } from "./ResetDialog";
import { ImportExportDialog } from "./ImportExportDialog";
import { toast } from "sonner";

export function AdvancedSettings() {
  const [resetOpen, setResetOpen] = useState(false);
  const [importExportOpen, setImportExportOpen] = useState(false);
  const [importExportMode, setImportExportMode] = useState<"import" | "export">("export");

  const openImportExport = (mode: "import" | "export") => {
    setImportExportMode(mode);
    setImportExportOpen(true);
  };

  const handleClearCache = () => {
    toast.success("Local application cache cleared successfully.");
  };

  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-medium text-foreground">Advanced Settings</h3>
        <p className="text-sm text-muted-foreground">Manage data, reset settings, and import/export configurations.</p>
      </div>

      <div className="space-y-6 max-w-xl">
        
        {/* Import / Export */}
        <div className="p-4 border border-border bg-card rounded-lg space-y-4">
          <div>
            <h4 className="text-sm font-medium text-foreground">Configuration Portability</h4>
            <p className="text-xs text-muted-foreground mt-1">Export your settings to a JSON file to share with team members or import an existing configuration.</p>
          </div>
          <div className="flex gap-3">
            <button 
              onClick={() => openImportExport("export")}
              className="flex-1 py-2 bg-muted hover:bg-muted/80 border border-border rounded-md text-sm font-medium text-foreground flex items-center justify-center gap-2 transition-colors"
            >
              <DownloadCloud size={16} /> Export Settings
            </button>
            <button 
              onClick={() => openImportExport("import")}
              className="flex-1 py-2 bg-muted hover:bg-muted/80 border border-border rounded-md text-sm font-medium text-foreground flex items-center justify-center gap-2 transition-colors"
            >
              <UploadCloud size={16} /> Import Settings
            </button>
          </div>
        </div>

        {/* Clear Cache */}
        <div className="p-4 border border-border bg-card rounded-lg flex items-center justify-between gap-4">
          <div>
            <h4 className="text-sm font-medium text-foreground">Clear Local Cache</h4>
            <p className="text-xs text-muted-foreground mt-1">Remove temporary UI state and cached API responses.</p>
          </div>
          <button 
            onClick={handleClearCache}
            className="px-4 py-2 bg-background border border-border rounded-md text-sm font-medium text-foreground hover:bg-muted transition-colors shrink-0"
          >
            Clear Cache
          </button>
        </div>

        {/* Factory Reset */}
        <div className="p-4 border border-destructive/30 bg-destructive/5 rounded-lg flex items-center justify-between gap-4">
          <div>
            <h4 className="text-sm font-medium text-destructive">Factory Reset</h4>
            <p className="text-xs text-destructive/80 mt-1">Reset all preferences to default values. This action cannot be undone.</p>
          </div>
          <button 
            onClick={() => setResetOpen(true)}
            className="px-4 py-2 bg-destructive text-destructive-foreground rounded-md text-sm font-medium hover:bg-destructive/90 transition-colors flex items-center gap-2 shrink-0"
          >
            <RefreshCcw size={16} /> Reset
          </button>
        </div>
      </div>

      <ResetDialog isOpen={resetOpen} onClose={() => setResetOpen(false)} />
      <ImportExportDialog isOpen={importExportOpen} onClose={() => setImportExportOpen(false)} mode={importExportMode} />
    </div>
  );
}
