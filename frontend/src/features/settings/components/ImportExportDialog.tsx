import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { X, Copy, Download, Upload, CheckCircle2 } from "lucide-react";
import { useSettingsStore } from "../../../stores/useSettingsStore";
import { toast } from "sonner";

interface Props {
  isOpen: boolean;
  onClose: () => void;
  mode: "import" | "export";
}

export function ImportExportDialog({ isOpen, onClose, mode }: Props) {
  const store = useSettingsStore();
  const [importText, setImportText] = useState("");

  const exportData = () => {
    // Exclude functions and non-serializable state
    const { updateSettings, updateFeatureFlags, setTheme, setAppMode, toggleSidebar, setReportsViewMode, resetSettings, importSettings, ...serializable } = store;
    return JSON.stringify(serializable, null, 2);
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(exportData());
    toast.success("Settings copied to clipboard");
  };

  const handleImport = () => {
    const success = store.importSettings(importText);
    if (success) {
      toast.success("Settings imported successfully");
      onClose();
    } else {
      toast.error("Invalid settings JSON format");
    }
  };

  if (!isOpen) return null;

  return (
    <AnimatePresence>
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-background/80 backdrop-blur-sm p-4">
        <motion.div 
          initial={{ opacity: 0, scale: 0.95, y: 20 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          exit={{ opacity: 0, scale: 0.95 }}
          className="w-full max-w-2xl bg-card border border-border shadow-2xl rounded-2xl overflow-hidden flex flex-col"
        >
          <div className="flex items-center justify-between p-4 border-b border-border bg-muted/30">
            <h2 className="font-semibold text-lg text-foreground flex items-center gap-2">
              {mode === "export" ? <Download size={18} /> : <Upload size={18} />}
              {mode === "export" ? "Export Settings" : "Import Settings"}
            </h2>
            <button onClick={onClose} className="p-2 hover:bg-muted rounded-full text-muted-foreground transition-colors">
              <X size={20} />
            </button>
          </div>

          <div className="p-6">
            {mode === "export" ? (
              <div className="space-y-4">
                <p className="text-sm text-muted-foreground">Copy the JSON below to share your configuration, or save it as a backup.</p>
                <div className="relative">
                  <textarea 
                    readOnly 
                    value={exportData()} 
                    className="w-full h-64 p-4 bg-muted border border-border rounded-md text-xs font-mono text-foreground focus:outline-none resize-none"
                  />
                  <button 
                    onClick={handleCopy}
                    className="absolute top-2 right-2 p-2 bg-background/80 hover:bg-background border border-border rounded text-foreground transition-colors"
                    title="Copy to clipboard"
                  >
                    <Copy size={14} />
                  </button>
                </div>
              </div>
            ) : (
              <div className="space-y-4">
                <p className="text-sm text-muted-foreground">Paste a valid settings JSON payload below to apply it to your current environment.</p>
                <textarea 
                  value={importText}
                  onChange={(e) => setImportText(e.target.value)}
                  placeholder="Paste JSON here..."
                  className="w-full h-64 p-4 bg-background border border-border rounded-md text-xs font-mono text-foreground focus:outline-none focus:ring-2 focus:ring-primary/20 resize-none"
                />
              </div>
            )}
          </div>

          <div className="p-4 bg-muted/30 border-t border-border flex justify-end gap-3">
            <button onClick={onClose} className="px-4 py-2 bg-background border border-border text-foreground rounded-md text-sm font-medium hover:bg-muted transition-colors">
              Close
            </button>
            {mode === "import" && (
              <button onClick={handleImport} className="px-4 py-2 bg-primary text-primary-foreground rounded-md text-sm font-medium hover:bg-primary/90 transition-colors flex items-center gap-2">
                <CheckCircle2 size={16} /> Apply Settings
              </button>
            )}
          </div>
        </motion.div>
      </div>
    </AnimatePresence>
  );
}
