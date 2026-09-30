export interface ChartData {
  name: string;
  value: number;
}

export interface DashboardStats {
  totalReports: number;
  todaysReports: number;
  monthlyReports: number;
  successRate: number;
  failedJobs: number;
  avgRuntimeMs: number;
}

export interface SystemHealth {
  storageUsedGb: number;
  storageTotalGb: number;
  memoryUsedMb: number;
  memoryTotalMb: number;
  queueStatus: "idle" | "processing" | "congested";
  activeWorkers: number;
}

export interface DashboardData {
  stats: DashboardStats;
  health: SystemHealth;
  charts: {
    reportsTrend: ChartData[];
    customerDistribution: ChartData[];
    runtimeTrend: ChartData[];
  };
}
