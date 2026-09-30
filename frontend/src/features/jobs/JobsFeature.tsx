import { useState, useMemo } from "react";
import { Link } from "react-router-dom";
import { Plus, RefreshCcw } from "lucide-react";
import { useJobs } from "./hooks/useJobs";
import { PageHeader } from "../../components/shared/Headers";
import { SearchInput } from "../../components/shared/SearchInput";
import { JobStatistics } from "./components/JobStatistics";
import { JobFilters } from "./components/JobFilters";
import { JobsTable } from "./components/JobsTable";
import { JobDrawer } from "./components/JobDrawer";
import { Skeleton } from "../../components/shared/Skeleton";
import { EmptyState } from "../../components/shared/EmptyState";
import { Job } from "../../types/job";
import { motion } from "framer-motion";

export function JobsFeature() {
  const { data: jobs, isLoading, isError, refetch, isFetching } = useJobs();
  
  const [globalSearch, setGlobalSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState("ALL");
  const [customerFilter, setCustomerFilter] = useState("ALL");
  
  const [selectedJob, setSelectedJob] = useState<Job | null>(null);

  const filteredJobs = useMemo(() => {
    if (!jobs) return [];
    return jobs.filter(job => {
      if (statusFilter !== "ALL" && job.status !== statusFilter) return false;
      if (customerFilter !== "ALL" && job.customerName !== customerFilter) return false;
      return true;
    });
  }, [jobs, statusFilter, customerFilter]);

  if (isError) {
    return (
      <EmptyState 
        title="Failed to load jobs" 
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
        title="Job Executions" 
        description="Monitor, manage, and debug presentation generation pipelines." 
        action={
          <div className="flex items-center gap-3">
            <button 
              onClick={() => refetch()} 
              disabled={isFetching}
              className="p-2 border border-border bg-card hover:bg-muted text-foreground rounded-md transition-colors disabled:opacity-50"
              title="Refresh Jobs"
            >
              <RefreshCcw size={18} className={isFetching ? "animate-spin" : ""} />
            </button>
            <Link 
              to="/generate" 
              className="px-4 py-2 bg-primary text-primary-foreground rounded-md font-medium text-sm flex items-center gap-2 hover:bg-primary/90 transition-colors shadow-sm"
            >
              <Plus size={16} /> New Report
            </Link>
          </div>
        }
      />

      {isLoading ? (
        <div className="space-y-6">
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
            {[...Array(4)].map((_, i) => <Skeleton key={i} className="h-24 rounded-xl" />)}
          </div>
          <Skeleton className="h-[400px] rounded-xl" />
        </div>
      ) : (
        <>
          {jobs && <JobStatistics jobs={jobs} />}
          
          <div className="bg-card border border-border rounded-xl p-6 shadow-sm space-y-4">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <JobFilters 
                statusFilter={statusFilter}
                setStatusFilter={setStatusFilter}
                customerFilter={customerFilter}
                setCustomerFilter={setCustomerFilter}
              />
              <div className="w-full sm:w-64">
                <SearchInput 
                  value={globalSearch} 
                  onChange={setGlobalSearch} 
                  placeholder="Search jobs..." 
                />
              </div>
            </div>

            <JobsTable 
              jobs={filteredJobs} 
              onRowClick={setSelectedJob}
              globalFilter={globalSearch}
            />
          </div>
        </>
      )}

      {/* Drawer */}
      <JobDrawer 
        isOpen={!!selectedJob} 
        job={jobs?.find(j => j.id === selectedJob?.id) || selectedJob} // Bind to live data from query if possible
        onClose={() => setSelectedJob(null)} 
      />
    </div>
  );
}
