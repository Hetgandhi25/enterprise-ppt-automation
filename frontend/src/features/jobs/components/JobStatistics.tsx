import { Job } from "../../../types/job";
import { TaskStatusEnum } from "../../../types/taskStatus";
import { CheckCircle2, Clock, PlayCircle, Loader2, StopCircle, RefreshCcw, XCircle, Trash2 } from "lucide-react";
import { motion } from "framer-motion";

interface Props {
  jobs: Job[];
}

export function JobStatistics({ jobs }: Props) {
  const running = jobs.filter(j => ![TaskStatusEnum.COMPLETED, TaskStatusEnum.FAILED].includes(j.status)).length;
  const completed = jobs.filter(j => j.status === TaskStatusEnum.COMPLETED).length;
  const failed = jobs.filter(j => j.status === TaskStatusEnum.FAILED).length;
  
  const runtimes = jobs.filter(j => j.runtimeMs).map(j => j.runtimeMs!);
  const avgRuntime = runtimes.length ? (runtimes.reduce((a,b) => a+b, 0) / runtimes.length / 1000).toFixed(1) : 0;

  const stats = [
    { title: "Running Jobs", value: running, icon: <RefreshCcw size={18} className="text-blue-500" />, bg: "bg-blue-500/10" },
    { title: "Completed", value: completed, icon: <CheckCircle2 size={18} className="text-emerald-500" />, bg: "bg-emerald-500/10" },
    { title: "Failed", value: failed, icon: <XCircle size={18} className="text-destructive" />, bg: "bg-destructive/10" },
    { title: "Avg. Runtime", value: `${avgRuntime}s`, icon: <Clock size={18} className="text-purple-500" />, bg: "bg-purple-500/10" },
  ];

  return (
    <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
      {stats.map((stat, i) => (
        <motion.div 
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: i * 0.1 }}
          key={stat.title} 
          className="bg-card border border-border rounded-xl p-4 flex items-center gap-4"
        >
          <div className={`w-10 h-10 rounded-full flex items-center justify-center ${stat.bg}`}>
            {stat.icon}
          </div>
          <div>
            <p className="text-xs text-muted-foreground font-medium">{stat.title}</p>
            <p className="text-2xl font-bold text-foreground">{stat.value}</p>
          </div>
        </motion.div>
      ))}
    </div>
  );
}
