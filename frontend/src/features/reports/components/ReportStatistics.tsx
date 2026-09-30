import { Report } from "../../../types/report";
import { FileText, HardDrive, Calendar, Star } from "lucide-react";
import { motion } from "framer-motion";

interface Props {
  reports: Report[];
}

export function ReportStatistics({ reports }: Props) {
  const total = reports.length;
  const today = new Date().toISOString().split("T")[0];
  const todaysReports = reports.filter(r => r.generatedAt.startsWith(today)).length;
  
  const totalSizeKb = reports.reduce((acc, r) => acc + (r.fileSizeKb || 0), 0);
  const sizeGb = (totalSizeKb / 1024 / 1024).toFixed(2);

  const customerCounts = reports.reduce((acc, r) => {
    acc[r.customerName] = (acc[r.customerName] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);
  
  const mostActive = Object.entries(customerCounts).sort((a, b) => b[1] - a[1])[0]?.[0] || "None";

  const stats = [
    { title: "Total Reports", value: total, icon: <FileText size={18} className="text-blue-500" />, bg: "bg-blue-500/10" },
    { title: "Generated Today", value: todaysReports, icon: <Calendar size={18} className="text-emerald-500" />, bg: "bg-emerald-500/10" },
    { title: "Storage Used", value: `${sizeGb} GB`, icon: <HardDrive size={18} className="text-purple-500" />, bg: "bg-purple-500/10" },
    { title: "Most Active", value: mostActive, icon: <Star size={18} className="text-amber-500" />, bg: "bg-amber-500/10" },
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
          <div className="overflow-hidden">
            <p className="text-xs text-muted-foreground font-medium truncate">{stat.title}</p>
            <p className="text-2xl font-bold text-foreground truncate">{stat.value}</p>
          </div>
        </motion.div>
      ))}
    </div>
  );
}
