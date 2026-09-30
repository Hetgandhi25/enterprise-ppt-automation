import { motion } from "framer-motion";
import { CheckCircle, Download, FileText, X } from "lucide-react";
import { Job } from "../../../types/job";
import { Link } from "react-router-dom";

interface Props {
  job: Job | null;
  isOpen: boolean;
  onClose: () => void;
}


export function SuccessDialog({ job, isOpen, onClose }: Props) {
  if (!isOpen || !job) return null;

  const handleDownload = () => {
    if (job.outputPath) {
      window.open(job.outputPath, '_blank');
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-background/80 backdrop-blur-sm p-4">
      <motion.div 
        initial={{ opacity: 0, scale: 0.95, y: 20 }}
        animate={{ opacity: 1, scale: 1, y: 0 }}
        className="w-full max-w-md bg-card border border-border shadow-2xl rounded-2xl overflow-hidden"
      >
        <div className="bg-emerald-500/10 p-6 flex flex-col items-center justify-center border-b border-emerald-500/20">
          <div className="w-16 h-16 bg-emerald-500 text-white rounded-full flex items-center justify-center mb-4 shadow-lg shadow-emerald-500/30">
            <CheckCircle size={32} />
          </div>
          <h2 className="text-xl font-bold text-emerald-700 dark:text-emerald-400">Generation Complete!</h2>
          <p className="text-sm text-emerald-600/80 dark:text-emerald-400/80 mt-1 text-center">
            Successfully generated report for {job.customerName}
          </p>
        </div>

        <div className="p-6 space-y-4">
          <div className="flex justify-between items-center text-sm">
            <span className="text-muted-foreground">Job ID</span>
            <span className="font-medium text-foreground">{job.id}</span>
          </div>
          <div className="flex justify-between items-center text-sm">
            <span className="text-muted-foreground">Runtime</span>
            <span className="font-medium text-foreground">{job.runtimeMs ? `${(job.runtimeMs / 1000).toFixed(1)}s` : '-'}</span>
          </div>
          <div className="flex justify-between items-center text-sm">
            <span className="text-muted-foreground">Output Path</span>
            <span className="font-medium text-foreground truncate max-w-[200px]" title={job.outputPath}>{job.outputPath || '/output/presentations/...'}</span>
          </div>
        </div>

        <div className="p-6 bg-muted/30 border-t border-border flex flex-col gap-3">
          <button 
            onClick={handleDownload}
            className="w-full py-2.5 bg-primary text-primary-foreground rounded-lg font-medium flex items-center justify-center gap-2 hover:bg-primary/90 transition-colors"
          >
            <Download size={18} />
            Download PPT
          </button>
          
          <div className="flex gap-3">
            <button onClick={onClose} className="flex-1 py-2.5 bg-background border border-border text-foreground rounded-lg font-medium hover:bg-muted transition-colors">
              Close
            </button>
            <Link to="/reports" className="flex-1 py-2.5 bg-background border border-border text-foreground rounded-lg font-medium flex items-center justify-center gap-2 hover:bg-muted transition-colors">
              <FileText size={18} />
              View Reports
            </Link>
          </div>
        </div>
      </motion.div>
    </div>
  );
}
