import { motion } from "framer-motion";
import { AlertOctagon, RotateCcw, ScrollText } from "lucide-react";
import { Job } from "../../../types/job";
import { Link } from "react-router-dom";

interface Props {
  job: Job | null;
  isOpen: boolean;
  onClose: () => void;
  onRetry: () => void;
}

export function FailureDialog({ job, isOpen, onClose, onRetry }: Props) {
  if (!isOpen || !job) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-background/80 backdrop-blur-sm p-4">
      <motion.div 
        initial={{ opacity: 0, scale: 0.95, y: 20 }}
        animate={{ opacity: 1, scale: 1, y: 0 }}
        className="w-full max-w-md bg-card border border-border shadow-2xl rounded-2xl overflow-hidden"
      >
        <div className="bg-destructive/10 p-6 flex flex-col items-center justify-center border-b border-destructive/20">
          <div className="w-16 h-16 bg-destructive text-white rounded-full flex items-center justify-center mb-4 shadow-lg shadow-destructive/30">
            <AlertOctagon size={32} />
          </div>
          <h2 className="text-xl font-bold text-destructive">Generation Failed</h2>
          <p className="text-sm text-destructive/80 mt-1 text-center">
            Job {job.id} for {job.customerName} encountered an error.
          </p>
        </div>

        <div className="p-6">
          <label className="text-xs font-semibold uppercase text-muted-foreground mb-2 block">Error Reason</label>
          <div className="p-4 bg-muted rounded-lg border border-border/50 text-sm font-mono text-foreground overflow-x-auto">
            {job.error || "Unknown fatal error occurred during pipeline execution."}
          </div>
        </div>

        <div className="p-6 bg-muted/30 border-t border-border flex flex-col gap-3">
          <button 
            onClick={onRetry}
            className="w-full py-2.5 bg-primary text-primary-foreground rounded-lg font-medium flex items-center justify-center gap-2 hover:bg-primary/90 transition-colors"
          >
            <RotateCcw size={18} />
            Retry Generation
          </button>
          
          <div className="flex gap-3">
            <button onClick={onClose} className="flex-1 py-2.5 bg-background border border-border text-foreground rounded-lg font-medium hover:bg-muted transition-colors">
              Dismiss
            </button>
            <Link to="/logs" className="flex-1 py-2.5 bg-background border border-border text-foreground rounded-lg font-medium flex items-center justify-center gap-2 hover:bg-muted transition-colors">
              <ScrollText size={18} />
              View Logs
            </Link>
          </div>
        </div>
      </motion.div>
    </div>
  );
}
