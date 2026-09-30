import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { X, RefreshCcw, StopCircle, Trash2, CheckCircle2, Circle, Loader2, ChevronDown } from "lucide-react";
import { Job } from "../../../types/job";
import { TaskStatusEnum } from "../../../types/taskStatus";
import { StatusBadge } from "../../../components/shared/StatusBadge";
import { useCancelJob, useDeleteJob } from "../hooks/useJobMutations";

interface Props {
  job: Job | null;
  isOpen: boolean;
  onClose: () => void;
}

const STAGES = [
  { id: TaskStatusEnum.PENDING, label: "Initializing Job" },
  { id: TaskStatusEnum.DOWNLOADING, label: "Downloading Data" },
  { id: TaskStatusEnum.PROCESSING_INVENTORY, label: "Processing Excel" },
  { id: TaskStatusEnum.GENERATING_CHARTS, label: "Generating Analytics" },
  { id: TaskStatusEnum.GENERATING_PPT, label: "Building Presentation" },
  { id: TaskStatusEnum.CLEANUP, label: "Cleanup" }
];

export function JobDrawer({ job, isOpen, onClose }: Props) {
  const cancelJob = useCancelJob();
  const deleteJob = useDeleteJob();
  const [detailsOpen, setDetailsOpen] = useState(false);

  if (!job) return null;

  const currentStageIndex = STAGES.findIndex(s => s.id === job.status);
  const isRunning = ![TaskStatusEnum.COMPLETED, TaskStatusEnum.FAILED].includes(job.status);
  
  return (
    <AnimatePresence>
      {isOpen && (
        <>
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-background/60 backdrop-blur-sm z-40"
            onClick={onClose}
          />
          <motion.div
            initial={{ x: "100%" }}
            animate={{ x: 0 }}
            exit={{ x: "100%" }}
            transition={{ type: "spring", damping: 25, stiffness: 200 }}
            className="fixed inset-y-0 right-0 w-full max-w-md bg-card border-l border-border shadow-2xl z-50 flex flex-col overflow-hidden"
          >
            {/* Header */}
            <div className="flex items-center justify-between p-4 border-b border-border bg-muted/30">
              <div>
                <h2 className="font-semibold text-lg text-foreground">Job Summary</h2>
                <p className="text-xs text-muted-foreground font-mono">{job.id}</p>
              </div>
              <button onClick={onClose} className="p-2 hover:bg-muted rounded-full text-muted-foreground transition-colors">
                <X size={20} />
              </button>
            </div>

            {/* Content */}
            <div className="flex-1 overflow-y-auto p-6 space-y-8">
              
              <div className="space-y-4">
                <div className="flex justify-between items-center pb-2 border-b border-border/50">
                  <span className="text-sm text-muted-foreground">Customer</span>
                  <span className="text-sm font-medium text-foreground">{job.customerName}</span>
                </div>
                <div className="flex justify-between items-center pb-2 border-b border-border/50">
                  <span className="text-sm text-muted-foreground">Status</span>
                  <StatusBadge status={job.status} />
                </div>
                {job.error && (
                  <div className="p-3 bg-destructive/10 border border-destructive/20 rounded-md">
                    <h4 className="text-xs font-semibold text-destructive mb-1">Execution Error</h4>
                    <p className="text-xs text-destructive/80 font-mono break-all">{job.error}</p>
                  </div>
                )}
              </div>

              {/* Progress Bar */}
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="font-medium text-foreground">Execution Progress</span>
                  <span className="font-medium text-primary">{job.progressPercentage}%</span>
                </div>
                <div className="h-2 w-full bg-muted rounded-full overflow-hidden">
                  <motion.div 
                    className="h-full bg-primary"
                    initial={{ width: 0 }}
                    animate={{ width: `${job.progressPercentage}%` }}
                    transition={{ duration: 0.5 }}
                  />
                </div>
              </div>

              {/* Expandable Details */}
              <div className="pt-4 border-t border-border">
                <button 
                  onClick={() => setDetailsOpen(!detailsOpen)}
                  className="w-full flex items-center justify-between py-2 text-sm font-medium text-foreground hover:text-primary transition-colors"
                >
                  View Execution Details
                  <ChevronDown size={16} className={`transition-transform ${detailsOpen ? 'rotate-180' : ''}`} />
                </button>

                <AnimatePresence>
                  {detailsOpen && (
                    <motion.div 
                      initial={{ opacity: 0, height: 0 }}
                      animate={{ opacity: 1, height: "auto" }}
                      exit={{ opacity: 0, height: 0 }}
                      className="overflow-hidden"
                    >
                      <div className="pt-4 space-y-6">
                        <div className="space-y-4">
                          <div className="flex justify-between items-center pb-2 border-b border-border/50">
                            <span className="text-sm text-muted-foreground">Started</span>
                            <span className="text-sm font-medium text-foreground">{new Date(job.startTime).toLocaleString()}</span>
                          </div>
                          {job.runtimeMs && (
                            <div className="flex justify-between items-center pb-2 border-b border-border/50">
                              <span className="text-sm text-muted-foreground">Duration</span>
                              <span className="text-sm font-medium text-foreground">{(job.runtimeMs / 1000).toFixed(1)}s</span>
                            </div>
                          )}
                        </div>

                        {/* Pipeline Timeline */}
                        <div>
                          <h3 className="text-xs font-semibold uppercase text-muted-foreground mb-4 tracking-wider">Pipeline Stages</h3>
                          <div className="space-y-4">
                            {STAGES.map((stage, index) => {
                              const isCompleted = currentStageIndex > index || job.status === TaskStatusEnum.COMPLETED;
                              const isCurrent = currentStageIndex === index;
                              
                              return (
                                <div key={stage.id} className="flex gap-4">
                                  <div className="relative flex flex-col items-center">
                                    <div className={`w-5 h-5 rounded-full flex items-center justify-center shrink-0 border-2 ${
                                      isCompleted ? 'bg-emerald-500 border-emerald-500 text-white' : 
                                      isCurrent ? 'border-primary bg-background text-primary' : 
                                      'border-muted bg-background text-muted-foreground'
                                    }`}>
                                      {isCompleted ? <CheckCircle2 size={12} /> : 
                                       isCurrent ? <Loader2 size={12} className="animate-spin" /> : 
                                       <Circle size={12} />}
                                    </div>
                                    {index < STAGES.length - 1 && (
                                      <div className={`w-0.5 h-full absolute top-5 ${isCompleted ? 'bg-emerald-500' : 'bg-border'}`} />
                                    )}
                                  </div>
                                  <div className="pb-3">
                                    <p className={`text-xs font-medium ${isCompleted ? 'text-foreground' : isCurrent ? 'text-primary' : 'text-muted-foreground'}`}>
                                      {stage.label}
                                    </p>
                                  </div>
                                </div>
                              );
                            })}
                          </div>
                        </div>
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>

            </div>

            {/* Footer Actions */}
            <div className="p-4 border-t border-border bg-muted/30 grid grid-cols-2 gap-3">
              {isRunning ? (
                <button 
                  onClick={() => {
                    cancelJob.mutate(job.id);
                    onClose();
                  }}
                  className="w-full py-2 bg-background border border-border rounded-md text-sm font-medium text-destructive hover:bg-destructive/10 flex items-center justify-center gap-2"
                >
                  <StopCircle size={16} /> Cancel
                </button>
              ) : (
                <button className="w-full py-2 bg-background border border-border rounded-md text-sm font-medium text-foreground hover:bg-muted flex items-center justify-center gap-2">
                  <RefreshCcw size={16} /> Retry
                </button>
              )}
              
              <button 
                onClick={() => {
                  deleteJob.mutate(job.id);
                  onClose();
                }}
                className="w-full py-2 bg-background border border-border rounded-md text-sm font-medium text-foreground hover:bg-destructive hover:text-destructive-foreground hover:border-destructive flex items-center justify-center gap-2 transition-colors"
              >
                <Trash2 size={16} /> Delete
              </button>
            </div>

          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}
