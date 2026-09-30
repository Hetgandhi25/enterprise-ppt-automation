import { motion, AnimatePresence } from "framer-motion";
import { AlertTriangle, X } from "lucide-react";
import { useSettingsStore } from "../../../stores/useSettingsStore";
import { toast } from "sonner";

interface Props {
  isOpen: boolean;
  onClose: () => void;
}

export function ResetDialog({ isOpen, onClose }: Props) {
  const { resetSettings } = useSettingsStore();

  const handleReset = () => {
    resetSettings();
    toast.success("Settings have been reset to default values.");
    onClose();
  };

  if (!isOpen) return null;

  return (
    <AnimatePresence>
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-background/80 backdrop-blur-sm p-4">
        <motion.div 
          initial={{ opacity: 0, scale: 0.95, y: 20 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          exit={{ opacity: 0, scale: 0.95 }}
          className="w-full max-w-md bg-card border border-border shadow-2xl rounded-2xl overflow-hidden"
        >
          <div className="flex items-center justify-between p-4 border-b border-border bg-muted/30">
            <h2 className="font-semibold text-lg text-foreground flex items-center gap-2">
              <AlertTriangle size={18} className="text-destructive" />
              Reset Settings
            </h2>
            <button onClick={onClose} className="p-2 hover:bg-muted rounded-full text-muted-foreground transition-colors">
              <X size={20} />
            </button>
          </div>

          <div className="p-6">
            <p className="text-sm text-foreground mb-4">
              Are you sure you want to restore all settings to their default values?
            </p>
            <p className="text-xs text-muted-foreground">
              This will clear your recent customers, reset paths, restore the demo application mode, and disable all experimental features. This action cannot be undone.
            </p>
          </div>

          <div className="p-4 bg-muted/30 border-t border-border flex justify-end gap-3">
            <button onClick={onClose} className="px-4 py-2 bg-background border border-border text-foreground rounded-md text-sm font-medium hover:bg-muted transition-colors">
              Cancel
            </button>
            <button onClick={handleReset} className="px-4 py-2 bg-destructive text-destructive-foreground rounded-md text-sm font-medium hover:bg-destructive/90 transition-colors">
              Yes, Reset Settings
            </button>
          </div>
        </motion.div>
      </div>
    </AnimatePresence>
  );
}
