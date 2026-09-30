import { useMemo } from "react";
import { ColumnDef } from "@tanstack/react-table";
import { Job } from "../../../types/job";
import { DataTable } from "../../../components/shared/DataTable";
import { StatusBadge } from "../../../components/shared/StatusBadge";
import { TaskStatusEnum } from "../../../types/taskStatus";
import { FileText, MoreHorizontal, Eye, XCircle, Trash2 } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { useState, useRef, useEffect } from "react";

import { useCancelJob, useDeleteJob } from "../hooks/useJobMutations";

function ActionMenu({ job, onView }: { job: Job, onView: () => void }) {
  const [isOpen, setIsOpen] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);
  const cancelJob = useCancelJob();
  const deleteJob = useDeleteJob();

  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(e.target as Node)) {
        setIsOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const isFailed = job.status === TaskStatusEnum.FAILED;
  const isCompleted = job.status === TaskStatusEnum.COMPLETED;
  const isRunning = !isFailed && !isCompleted;

  return (
    <div className="relative" ref={menuRef} onClick={(e) => e.stopPropagation()}>
      <button 
        className="p-1 hover:bg-muted text-muted-foreground rounded transition-colors" 
        onClick={() => setIsOpen(!isOpen)}
      >
        <MoreHorizontal size={16} />
      </button>

      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, scale: 0.95, y: -10 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: -10 }}
            transition={{ duration: 0.15 }}
            className="absolute right-0 top-full mt-1 w-36 bg-popover border border-border rounded-md shadow-md z-50 overflow-hidden"
          >
            <button 
              className="w-full text-left px-3 py-2 text-sm text-foreground hover:bg-muted flex items-center gap-2 transition-colors"
              onClick={() => {
                onView();
                setIsOpen(false);
              }}
            >
              <Eye size={14} /> View Details
            </button>
            {isRunning ? (
              <button 
                className="w-full text-left px-3 py-2 text-sm text-orange-500 hover:bg-orange-500/10 flex items-center gap-2 transition-colors"
                onClick={() => {
                  cancelJob.mutate(job.id);
                  setIsOpen(false);
                }}
              >
                <XCircle size={14} /> Cancel Job
              </button>
            ) : (
              <button 
                className="w-full text-left px-3 py-2 text-sm text-destructive hover:bg-destructive/10 flex items-center gap-2 transition-colors"
                onClick={() => {
                  deleteJob.mutate(job.id);
                  setIsOpen(false);
                }}
              >
                <Trash2 size={14} /> Delete
              </button>
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}


interface Props {
  jobs: Job[];
  onRowClick: (job: Job) => void;
  globalFilter?: string;
}

export function JobsTable({ jobs, onRowClick, globalFilter }: Props) {
  
  const columns = useMemo<ColumnDef<Job>[]>(
    () => [
      {
        accessorKey: "id",
        header: "Job ID",
        cell: ({ row }) => <span className="font-mono text-xs text-muted-foreground">{row.original.id}</span>,
      },
      {
        accessorKey: "customerName",
        header: "Customer",
        cell: ({ row }) => <span className="font-medium text-foreground">{row.original.customerName}</span>,
      },
      {
        accessorKey: "status",
        header: "Status",
        cell: ({ row }) => <StatusBadge status={row.original.status} />,
      },
      {
        accessorKey: "progressPercentage",
        header: "Progress",
        cell: ({ row }) => {
          const progress = row.original.progressPercentage;
          const status = row.original.status;
          const isFailed = status === TaskStatusEnum.FAILED;
          const isCompleted = status === TaskStatusEnum.COMPLETED;
          
          return (
            <div className="w-24">
              <div className="flex justify-between text-xs mb-1">
                <span className={isFailed ? "text-destructive" : isCompleted ? "text-emerald-500" : "text-primary"}>
                  {progress}%
                </span>
              </div>
              <div className="h-1.5 w-full bg-muted rounded-full overflow-hidden">
                <div 
                  className={`h-full ${isFailed ? "bg-destructive" : isCompleted ? "bg-emerald-500" : "bg-primary"}`} 
                  style={{ width: `${progress}%` }} 
                />
              </div>
            </div>
          );
        },
      },
      {
        accessorKey: "startTime",
        header: "Started",
        cell: ({ row }) => <span className="text-sm text-muted-foreground">{new Date(row.original.startTime).toLocaleString()}</span>,
      },
      {
        accessorKey: "runtimeMs",
        header: "Duration",
        cell: ({ row }) => {
          const ms = row.original.runtimeMs;
          return <span className="text-sm text-muted-foreground">{ms ? `${(ms / 1000).toFixed(1)}s` : "-"}</span>;
        },
      },
      {
        id: "actions",
        cell: ({ row }) => <ActionMenu job={row.original} onView={() => onRowClick(row.original)} />,
      }
    ],
    []
  );

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
      <DataTable 
        columns={columns} 
        data={jobs} 
        onRowClick={onRowClick}
        globalFilter={globalFilter}
      />
    </motion.div>
  );
}
