import { Job } from "../types/job";
import { Report } from "../types/report";

export interface IJobService {
  getJobs(): Promise<Job[]>;
  getJob(id: string): Promise<Job>;
  generateReport(payload: { customerName: string; reportMonth: string; [key: string]: any }): Promise<Job>;
  cancelJob(id: string): Promise<void>;
  deleteJob(id: string): Promise<void>;
}

export interface IReportService {
  getReports(): Promise<Report[]>;
  getReport(id: string): Promise<Report>;
  deleteReport(id: string): Promise<void>;
}

import { DashboardData } from "../types/dashboard";

export interface IDashboardService {
  getStats(): Promise<DashboardData>;
}
