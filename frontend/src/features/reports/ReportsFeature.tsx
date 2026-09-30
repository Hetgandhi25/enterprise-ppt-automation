import { useState, useMemo, useEffect } from "react";
import { Link } from "react-router-dom";
import { UploadCloud, RefreshCcw, LayoutGrid, List } from "lucide-react";
import { useReports } from "./hooks/useReports";
import { PageHeader } from "../../components/shared/Headers";
import { SearchInput } from "../../components/shared/SearchInput";
import { ReportStatistics } from "./components/ReportStatistics";
import { ReportFilters } from "./components/ReportFilters";
import { ReportsGrid } from "./components/ReportsGrid";
import { ReportsTable } from "./components/ReportsTable";
import { ReportDrawer } from "./components/ReportDrawer";
import { Skeleton } from "../../components/shared/Skeleton";
import { EmptyState } from "../../components/shared/EmptyState";
import { Report } from "../../types/report";
import { useSettingsStore } from "../../stores/useSettingsStore";

export function ReportsFeature() {
  const { data: reports, isLoading, isError, refetch, isFetching } = useReports();
  const { reportsViewMode, setReportsViewMode } = useSettingsStore();
  
  const [globalSearch, setGlobalSearch] = useState("");
  const [debouncedSearch, setDebouncedSearch] = useState("");
  const [customerFilter, setCustomerFilter] = useState("ALL");
  const [monthFilter, setMonthFilter] = useState("ALL");
  const [statusFilter, setStatusFilter] = useState("ALL");
  const [customDateRange, setCustomDateRange] = useState({ start: "", end: "" });
  const [selectedReport, setSelectedReport] = useState<Report | null>(null);

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedSearch(globalSearch), 300);
    return () => clearTimeout(timer);
  }, [globalSearch]);

  const filteredReports = useMemo(() => {
    if (!reports) return [];
    return reports.filter(r => {
      if (customerFilter !== "ALL" && r.customerName !== customerFilter) return false;
      // Note: Month & Status are mocked since there's no actual data mapped for complex month logic yet, but we allow filtering if exact match
      if (monthFilter !== "ALL") {
        if (monthFilter === "Current Month" && r.reportMonth !== "2026-07") return false;
        
        if (monthFilter === "Custom Month" && customDateRange.start && customDateRange.end) {
          const reportDate = new Date(r.generatedAt).getTime();
          const startDate = new Date(customDateRange.start).getTime();
          // Add 1 day to end date to include the entire end date (up to midnight)
          const endDate = new Date(customDateRange.end).getTime() + 86400000;
          if (reportDate < startDate || reportDate >= endDate) return false;
        }
      }

      // If status filter is applied, assume all current mock reports are 'Completed' unless they have a specific status
      if (statusFilter !== "ALL" && statusFilter !== "Completed") return false; 
      
      if (debouncedSearch) {
        const search = debouncedSearch.toLowerCase();
        if (
          !r.customerName.toLowerCase().includes(search) &&
          !r.reportMonth.toLowerCase().includes(search) &&
          !r.id.toLowerCase().includes(search) &&
          !r.jobId.toLowerCase().includes(search) &&
          !r.pptPath.toLowerCase().includes(search)
        ) {
          return false;
        }
      }
      return true;
    });
  }, [reports, customerFilter, monthFilter, statusFilter, customDateRange, debouncedSearch]);

  if (isError) {
    return (
      <EmptyState 
        title="Failed to load reports" 
        description="There was a problem communicating with the backend services."
        action={
          <button onClick={() => refetch()} className="px-4 py-2 bg-primary text-primary-foreground rounded-md font-medium text-sm">
            Retry Connection
          </button>
        }
      />
    );
  }

  return (
    <div className="max-w-7xl mx-auto space-y-6 pb-8">
      <PageHeader 
        title="Report Repository" 
        description="Browse, preview, and share all generated presentations." 
        action={
          <div className="flex items-center gap-3">
            <button 
              onClick={() => refetch()} 
              disabled={isFetching}
              className="p-2 border border-border bg-card hover:bg-muted text-foreground rounded-md transition-colors disabled:opacity-50"
              title="Refresh Reports"
            >
              <RefreshCcw size={18} className={isFetching ? "animate-spin" : ""} />
            </button>
            <button 
              disabled
              className="px-4 py-2 bg-muted text-muted-foreground border border-border rounded-md font-medium text-sm flex items-center gap-2 cursor-not-allowed opacity-70"
            >
              <UploadCloud size={16} /> Upload External
            </button>
          </div>
        }
      />

      {isLoading ? (
        <div className="space-y-6">
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
            {[...Array(4)].map((_, i) => <Skeleton key={i} className="h-24 rounded-xl" />)}
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 xl:grid-cols-5 gap-4">
            {[...Array(10)].map((_, i) => <Skeleton key={i} className="h-48 rounded-xl" />)}
          </div>
        </div>
      ) : (
        <>
          {reports && <ReportStatistics reports={reports} />}
          
          <div className="space-y-4">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <ReportFilters 
                customerFilter={customerFilter}
                setCustomerFilter={setCustomerFilter}
                monthFilter={monthFilter}
                setMonthFilter={setMonthFilter}
                statusFilter={statusFilter}
                setStatusFilter={setStatusFilter}
                customDateRange={customDateRange}
                setCustomDateRange={setCustomDateRange}
              />
              <div className="flex items-center gap-3 w-full sm:w-auto">
                <div className="w-full sm:w-64">
                  <SearchInput 
                    value={globalSearch} 
                    onChange={setGlobalSearch} 
                    placeholder="Search customer, ID..." 
                  />
                </div>
                <div className="flex items-center bg-card border border-border rounded-md p-1 shrink-0">
                  <button 
                    onClick={() => setReportsViewMode("grid")}
                    className={`p-1.5 rounded ${reportsViewMode === "grid" ? "bg-muted text-foreground" : "text-muted-foreground hover:text-foreground"}`}
                  >
                    <LayoutGrid size={16} />
                  </button>
                  <button 
                    onClick={() => setReportsViewMode("table")}
                    className={`p-1.5 rounded ${reportsViewMode === "table" ? "bg-muted text-foreground" : "text-muted-foreground hover:text-foreground"}`}
                  >
                    <List size={16} />
                  </button>
                </div>
              </div>
            </div>

            <div className="flex items-center justify-between text-sm text-muted-foreground px-1">
              <span>Showing {filteredReports.length} of {reports?.length || 0} Reports</span>
            </div>

            {reportsViewMode === "grid" ? (
              <ReportsGrid 
                reports={filteredReports} 
                onReportClick={setSelectedReport}
              />
            ) : (
              <div className="bg-card border border-border rounded-xl p-4">
                <ReportsTable 
                  reports={filteredReports} 
                  onRowClick={setSelectedReport}
                />
              </div>
            )}
          </div>
        </>
      )}

      {/* Drawer */}
      <ReportDrawer 
        isOpen={!!selectedReport} 
        report={reports?.find(r => r.id === selectedReport?.id) || selectedReport} 
        onClose={() => setSelectedReport(null)} 
      />
    </div>
  );
}
