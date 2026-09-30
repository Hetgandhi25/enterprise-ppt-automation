import { useMemo } from "react";
import { ColumnDef } from "@tanstack/react-table";
import { Report } from "../../../types/report";
import { DataTable } from "../../../components/shared/DataTable";
import { FileText, MoreHorizontal, Download, Trash2 } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { useState, useRef, useEffect } from "react";
import { useDeleteReport, useDownloadReport } from "../hooks/useReportMutations";

function ActionMenu({ report }: { report: Report }) {
  const [isOpen, setIsOpen] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);
  const deleteMutation = useDeleteReport();
  const downloadReport = useDownloadReport();

  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(e.target as Node)) {
        setIsOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

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
        // Fallback for mock data (starts with C:/ or similar)
        downloadReport.mutate(report.id);
      }
    } catch (e) {
      // Fallback if fetch fails (e.g. CORS)
      window.open(report.pptPath, '_blank');
    }
    setIsOpen(false);
  };

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
              onClick={handleDownload}
              className="w-full text-left px-3 py-2 text-sm text-foreground hover:bg-muted flex items-center gap-2 transition-colors"
            >
              <Download size={14} /> Download
            </button>
            <button 
              className="w-full text-left px-3 py-2 text-sm text-destructive hover:bg-destructive/10 flex items-center gap-2 transition-colors disabled:opacity-50"
              disabled={deleteMutation.isPending}
              onClick={() => {
                deleteMutation.mutate(report.id);
                setIsOpen(false);
              }}
            >
              <Trash2 size={14} /> Delete
            </button>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}


interface Props {
  reports: Report[];
  onRowClick: (r: Report) => void;
  globalFilter?: string;
}

export function ReportsTable({ reports, onRowClick, globalFilter }: Props) {
  
  const columns = useMemo<ColumnDef<Report>[]>(
    () => [
      {
        accessorKey: "customerName",
        header: "Customer",
        cell: ({ row }) => (
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded bg-primary/10 text-primary flex items-center justify-center shrink-0">
              <FileText size={16} />
            </div>
            <span className="font-medium text-foreground">{row.original.customerName}</span>
          </div>
        ),
      },
      {
        accessorKey: "reportMonth",
        header: "Month",
        cell: ({ row }) => <span className="text-sm text-foreground">{row.original.reportMonth}</span>,
      },
      {
        accessorKey: "generatedAt",
        header: "Generated Date",
        cell: ({ row }) => <span className="text-sm text-muted-foreground">{new Date(row.original.generatedAt).toLocaleString()}</span>,
      },
      {
        accessorKey: "fileSizeKb",
        header: "Size",
        cell: ({ row }) => {
          const kb = row.original.fileSizeKb;
          return <span className="text-sm text-muted-foreground">{kb ? `${(kb / 1024).toFixed(1)} MB` : "Unknown"}</span>;
        },
      },
      {
        accessorKey: "runtimeMs",
        header: "Runtime",
        cell: ({ row }) => <span className="text-sm text-muted-foreground">{(row.original.runtimeMs / 1000).toFixed(1)}s</span>,
      },
      {
        id: "actions",
        enableSorting: false,
        cell: ({ row }) => <ActionMenu report={row.original} />,
      }
    ],
    []
  );

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
      <DataTable 
        columns={columns} 
        data={reports} 
        onRowClick={onRowClick}
        globalFilter={globalFilter}
      />
    </motion.div>
  );
}
