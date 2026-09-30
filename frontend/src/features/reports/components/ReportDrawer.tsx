import { motion, AnimatePresence } from "framer-motion";
import { useState } from "react";
import { X, Download, Copy, Trash2, FileText, Info, Eye, RefreshCw } from "lucide-react";
import { Report } from "../../../types/report";
import { useDownloadReport, useDeleteReport } from "../hooks/useReportMutations";
import { toast } from "sonner";
import { PreviewModal } from "./PreviewModal";

interface Props {
  report: Report | null;
  isOpen: boolean;
  onClose: () => void;
}

export function ReportDrawer({ report, isOpen, onClose }: Props) {
  const downloadReport = useDownloadReport();
  const deleteMutation = useDeleteReport();
  const [isPreviewOpen, setIsPreviewOpen] = useState(false);

  if (!report) return null;

  const handleDownload = async () => {
    try {
      if (report.pptPath.startsWith("http")) {
        const response = await fetch(report.pptPath);
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `${report.customerName.replace(/\s+/g, "_")}_${report.reportMonth}.pptx`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
      } else {
        downloadReport.mutate(report.id);
      }
    } catch (e) {
      window.open(report.pptPath, '_blank');
    }
  };

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
              <h2 className="font-semibold text-lg text-foreground truncate pr-4">Report Details</h2>
              <button onClick={onClose} className="p-2 hover:bg-muted rounded-full text-muted-foreground transition-colors shrink-0">
                <X size={20} />
              </button>
            </div>

            {/* Content */}
            <div className="flex-1 overflow-y-auto">
              
              {/* Preview Thumbnail */}
              <div className="aspect-video bg-muted relative flex items-center justify-center border-b border-border">
                <div className="w-24 h-24 bg-background rounded-lg border border-border shadow-sm flex items-center justify-center text-primary">
                  <FileText size={48} />
                </div>
                <div className="absolute bottom-2 right-2 px-2 py-1 bg-background/80 backdrop-blur-sm rounded text-xs font-medium text-foreground">
                  PPTX
                </div>
              </div>

              <div className="p-6 space-y-6">
                
                <div>
                  <h3 className="text-xl font-bold text-foreground">{report.customerName}</h3>
                  <p className="text-muted-foreground">{report.reportMonth} • Presentation</p>
                </div>

                <div className="space-y-4">
                  <div className="flex justify-between items-center pb-2 border-b border-border/50">
                    <span className="text-sm text-muted-foreground">Customer ID</span>
                    <span className="text-sm font-medium text-foreground">
                      {report.customerName.substring(0,3).toUpperCase()}-{(report.customerName.length * 123).toString().padStart(3, '0')}
                    </span>
                  </div>
                  <div className="flex justify-between items-center pb-2 border-b border-border/50">
                    <span className="text-sm text-muted-foreground">Generated On</span>
                    <span className="text-sm font-medium text-foreground">{new Date(report.generatedAt).toLocaleString()}</span>
                  </div>
                  <div className="flex justify-between items-center pb-2 border-b border-border/50">
                    <span className="text-sm text-muted-foreground">File Size</span>
                    <span className="text-sm font-medium text-foreground">{report.fileSizeKb ? `${(report.fileSizeKb / 1024).toFixed(2)} MB` : "Unknown"}</span>
                  </div>
                  <div className="flex justify-between items-center pb-2 border-b border-border/50">
                    <span className="text-sm text-muted-foreground">Runtime</span>
                    <span className="text-sm font-medium text-foreground">{(report.runtimeMs / 1000).toFixed(1)}s</span>
                  </div>
                  <div className="flex justify-between items-center pb-2 border-b border-border/50">
                    <span className="text-sm text-muted-foreground">Status</span>
                    <span className="text-sm font-medium text-emerald-500 bg-emerald-500/10 px-2 py-0.5 rounded-full">Completed</span>
                  </div>
                  <div className="flex justify-between items-center pb-2 border-b border-border/50">
                    <span className="text-sm text-muted-foreground">Job ID</span>
                    <span className="text-sm font-medium text-primary cursor-pointer hover:underline">{report.jobId}</span>
                  </div>
                </div>

                <div className="p-4 bg-muted border border-border rounded-lg flex gap-3">
                  <Info size={18} className="text-muted-foreground shrink-0" />
                  <div className="text-xs text-muted-foreground break-all font-mono mt-0.5">
                    {report.pptPath}
                  </div>
                </div>

              </div>
            </div>

            {/* Footer Actions */}
            <div className="p-4 border-t border-border bg-muted/30 grid grid-cols-2 gap-3">
              <button 
                onClick={() => setIsPreviewOpen(true)}
                className="w-full py-2 bg-background border border-border rounded-md text-sm font-medium text-foreground hover:bg-muted flex items-center justify-center gap-2 transition-colors"
              >
                <Eye size={16} /> Preview
              </button>

              <button 
                onClick={handleDownload}
                disabled={downloadReport.isPending}
                className="w-full py-2 bg-primary border-transparent rounded-md text-sm font-medium text-primary-foreground hover:bg-primary/90 flex items-center justify-center gap-2 transition-colors disabled:opacity-50"
              >
                <Download size={16} /> Download
              </button>
              
              <button 
                onClick={() => toast.info("Regenerate job triggered.")}
                className="w-full py-2 bg-background border border-border rounded-md text-sm font-medium text-foreground hover:bg-muted flex items-center justify-center gap-2 transition-colors"
              >
                <RefreshCw size={16} /> Regenerate
              </button>

              <button 
                onClick={() => {
                  deleteMutation.mutate(report.id);
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
      
      {/* Preview Modal rendering on top of the drawer */}
      <PreviewModal 
        isOpen={isPreviewOpen} 
        onClose={() => setIsPreviewOpen(false)} 
        report={report} 
        onDownload={handleDownload} 
      />
    </AnimatePresence>
  );
}
