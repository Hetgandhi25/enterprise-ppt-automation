import { motion, AnimatePresence } from "framer-motion";
import { X, Download, Play } from "lucide-react";
import { Report } from "../../../types/report";

interface Props {
  isOpen: boolean;
  onClose: () => void;
  report: Report | null;
  onDownload: () => void;
}

const SLIDES = [
  { id: 1, title: "Title Slide", type: "title" },
  { id: 2, title: "Executive Summary", type: "text" },
  { id: 3, title: "Service Desk SLA", type: "chart" },
  { id: 4, title: "Incident Trends", type: "chart" }
];

export function PreviewModal({ isOpen, onClose, report, onDownload }: Props) {
  if (!isOpen || !report) return null;

  // Office Online Viewer requires a public URL. 
  // For localhost, it will show an error, but this is the exact implementation needed for production.
  const isLocalhost = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
  const pptPublicUrl = report.pptPath.startsWith('http') 
    ? report.pptPath 
    : `http://localhost:8000/output/presentations/${report.pptPath.split('/').pop()}`;

  const viewerUrl = `https://view.officeapps.live.com/op/embed.aspx?src=${encodeURIComponent(pptPublicUrl)}`;

  return (
    <AnimatePresence>
      <div className="fixed inset-0 z-[100] flex items-center justify-center bg-background/90 backdrop-blur-md">
        <motion.div 
          initial={{ opacity: 0, scale: 0.95, y: 20 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          exit={{ opacity: 0, scale: 0.95, y: 20 }}
          className="w-[95vw] h-[95vh] max-w-7xl bg-card border border-border shadow-2xl rounded-xl flex flex-col overflow-hidden"
        >
          {/* Header */}
          <div className="flex items-center justify-between p-4 border-b border-border bg-muted/30">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-primary/10 text-primary rounded">
                <Play size={18} />
              </div>
              <div>
                <h3 className="font-semibold text-foreground">{report.customerName} - {report.reportMonth}</h3>
                <p className="text-xs text-muted-foreground">Original Presentation Preview</p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <button 
                onClick={onDownload}
                className="px-4 py-2 bg-primary text-primary-foreground hover:bg-primary/90 text-sm font-medium rounded-md transition-colors flex items-center gap-2"
              >
                <Download size={16} /> Download PPTX
              </button>
              <button 
                onClick={onClose}
                className="p-2 hover:bg-muted text-muted-foreground hover:text-foreground rounded-full transition-colors"
              >
                <X size={20} />
              </button>
            </div>
          </div>

          {/* Viewer Area */}
          <div className="flex flex-1 overflow-hidden relative bg-muted/20">
            {isLocalhost && (
              <div className="absolute inset-x-0 top-0 bg-yellow-500/10 border-b border-yellow-500/20 p-3 text-center text-yellow-600 text-sm font-medium z-10 flex items-center justify-center gap-2">
                ⚠️ Microsoft Office Viewer cannot access 'localhost'. The preview will display correctly once deployed to a public server.
              </div>
            )}
            
            <iframe 
              src={viewerUrl} 
              className="w-full h-full border-none"
              title="Presentation Preview"
              allowFullScreen
            />
          </div>
        </motion.div>
      </div>
    </AnimatePresence>
  );
}
