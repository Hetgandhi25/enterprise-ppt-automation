import { IDashboardService } from "../interfaces";
import { DashboardData } from "../../types/dashboard";

const delay = (ms: number) => new Promise((res) => setTimeout(res, ms));

export class MockDashboardService implements IDashboardService {
  async getStats(): Promise<DashboardData> {
    await delay(800); // Simulate network latency

    return {
      stats: {
        totalReports: 1250,
        todaysReports: 24,
        monthlyReports: 342,
        successRate: 98.5,
        failedJobs: 3,
        avgRuntimeMs: 512,
      },
      health: {
        storageUsedGb: 45.2,
        storageTotalGb: 100,
        memoryUsedMb: 1240,
        memoryTotalMb: 4096,
        queueStatus: "processing",
        activeWorkers: 4,
      },
      charts: {
        reportsTrend: [
          { name: "Mon", value: 12 },
          { name: "Tue", value: 18 },
          { name: "Wed", value: 15 },
          { name: "Thu", value: 25 },
          { name: "Fri", value: 22 },
          { name: "Sat", value: 5 },
          { name: "Sun", value: 8 },
        ],
        customerDistribution: [
          { name: "ASG India", value: 45 },
          { name: "Sun Pharma", value: 30 },
          { name: "Tata Motors", value: 15 },
          { name: "HDFC Bank", value: 10 },
        ],
        runtimeTrend: [
          { name: "Week 1", value: 580 },
          { name: "Week 2", value: 540 },
          { name: "Week 3", value: 520 },
          { name: "Week 4", value: 512 },
        ],
      },
    };
  }
}
