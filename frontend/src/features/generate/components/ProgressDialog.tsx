import { motion, AnimatePresence } from "framer-motion";
import { Loader2, CheckCircle2, Circle } from "lucide-react";
import { TaskStatusEnum } from "../../../types/taskStatus";
import { Job } from "../../../types/job";

interface Props {
  job: Job | null;
  isOpen: boolean;
}

const STAGES = [
  { id: TaskStatusEnum.PENDING, label: "Initializing Job" },
  { id: TaskStatusEnum.DOWNLOADING, label: "Downloading Reports from CRM" },
  { id: TaskStatusEnum.PROCESSING_INVENTORY, label: "Processing Excel Data" },
  { id: TaskStatusEnum.GENERATING_CHARTS, label: "Generating Analytics Charts" },
  { id: TaskStatusEnum.GENERATING_PPT, label: "Building PowerPoint" },
  { id: TaskStatusEnum.CLEANUP, label: "Cleaning up Temporary Files" }
];

export function ProgressDialog({ job, isOpen }: Props) {
  if (!isOpen || !job) return null;

  const currentStageIndex = STAGES.findIndex(s => s.id === job.status);
  
  // Simulated elapsed time (for UI realism)
  const startTime = new Date(job.startTime).getTime();
  const elapsedSeconds = Math.floor((Date.now() - startTime) / 1000);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-background/80 backdrop-blur-sm">
      <motion.div 
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="w-full max-w-lg bg-card border border-border shadow-2xl rounded-2xl p-6"
      >
        <div className="text-center mb-8">
          <h2 className="text-xl font-bold text-foreground">Generating Presentation</h2>
          <p className="text-sm text-muted-foreground mt-1">Please wait while we assemble your report for {job.customerName}</p>
        </div>

        <div className="space-y-6">
          {STAGES.map((stage, index) => {
            const isCompleted = currentStageIndex > index || job.status === TaskStatusEnum.COMPLETED;
            const isCurrent = currentStageIndex === index;
            const isPending = currentStageIndex < index && job.status !== TaskStatusEnum.COMPLETED;

            return (
              <div key={stage.id} className="flex items-center gap-4">
                <div className="shrink-0 relative flex items-center justify-center w-6 h-6">
                  {isCompleted && <CheckCircle2 className="text-emerald-500" size={24} />}
                  {isCurrent && <Loader2 className="text-primary animate-spin" size={24} />}
                  {isPending && <Circle className="text-muted-foreground/30" size={24} />}
                  
                  {index < STAGES.length - 1 && (
                    <div className={`absolute top-6 left-1/2 -translate-x-1/2 w-0.5 h-6 ${isCompleted ? 'bg-emerald-500' : 'bg-muted-foreground/20'}`} />
                  )}
                </div>
                <div className="flex-1">
                  <p className={`font-medium ${isCompleted ? 'text-foreground' : isCurrent ? 'text-primary' : 'text-muted-foreground'}`}>
                    {stage.label}
                  </p>
                </div>
              </div>
            );
          })}
        </div>

        <div className="mt-8 pt-6 border-t border-border flex items-center justify-between text-sm">
          <span className="text-muted-foreground">Overall Progress</span>
          <span className="font-bold text-foreground">{job.progressPercentage}%</span>
        </div>
        <div className="w-full h-2 bg-muted rounded-full overflow-hidden mt-2">
          <motion.div 
            className="h-full bg-primary"
            initial={{ width: 0 }}
            animate={{ width: `${job.progressPercentage}%` }}
          />
        </div>
      </motion.div>
    </div>
  );
}
