import { IJobService, IReportService, IDashboardService } from "./interfaces";
import { ApiJobService } from "./api/ApiJobService";
import { ApiDashboardService } from "./api/ApiDashboardService";
import { ApiReportService } from "./api/ApiReportService";

/**
 * Service Factory
 * In the future, this factory will return FastAPIService instances based on AppMode or env vars.
 */
class ServiceFactory {
  static getJobService(): IJobService {
    return new ApiJobService();
  }

  static getReportService(): IReportService {
    return new ApiReportService();
  }

  static getDashboardService(): IDashboardService {
    return new ApiDashboardService();
  }
}

// Export pre-instantiated services for UI use
export const jobService = ServiceFactory.getJobService();
export const reportService = ServiceFactory.getReportService();
export const dashboardService = ServiceFactory.getDashboardService();
