import { useMemo } from "react";
import { Report } from "../../../types/report";
import { FileText, Clock, HardDrive, MoreVertical } from "lucide-react";
import { motion } from "framer-motion";

interface Props {
  report: Report;
  onClick: (r: Report) => void;
}

export function ReportCard({ report, onClick }: Props) {
  const sizeMb = report.fileSizeKb ? (report.fileSizeKb / 1024).toFixed(1) : "Unknown";

  return (
    <motion.div 
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      whileHover={{ y: -4 }}
      onClick={() => onClick(report)}
      className="bg-card border border-border rounded-xl overflow-hidden cursor-pointer shadow-sm hover:shadow-md transition-all group"
    >
      <div className="aspect-video bg-muted relative flex items-center justify-center border-b border-border group-hover:bg-primary/5 transition-colors">
        {/* Mock PPT Thumbnail */}
        <div className="w-16 h-16 bg-background rounded-lg border border-border shadow-sm flex items-center justify-center text-primary group-hover:scale-110 transition-transform">
          <FileText size={32} />
        </div>
        <div className="absolute top-2 right-2 p-1 rounded-md bg-background/50 hover:bg-background text-muted-foreground transition-colors opacity-0 group-hover:opacity-100">
          <MoreVertical size={16} />
        </div>
      </div>
      
      <div className="p-4 space-y-3">
        <div>
          <h3 className="font-semibold text-foreground truncate text-sm" title={`${report.customerName} - ${report.reportMonth}`}>
            {report.customerName}
          </h3>
          <p className="text-xs text-muted-foreground">Month: {report.reportMonth}</p>
        </div>

        <div className="grid grid-cols-2 gap-2 text-xs text-muted-foreground">
          <div className="flex items-center gap-1.5">
            <Clock size={12} />
            <span>{new Date(report.generatedAt).toLocaleDateString()}</span>
          </div>
          <div className="flex items-center gap-1.5">
            <HardDrive size={12} />
            <span>{sizeMb} MB</span>
          </div>
        </div>
      </div>
    </motion.div>
  );
}
