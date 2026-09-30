import { IReportService } from "../interfaces";
import { Report } from "../../types/report";

const delay = (ms: number) => new Promise((res) => setTimeout(res, ms));

export class MockReportService implements IReportService {
  private reports: Report[] = Array.from({ length: 200 }).map((_, i) => ({
    id: `REP-${1000 + i}`,
    jobId: `JOB-${1000 + i}`,
    customerName: ["ASG India", "Sun Pharma", "Tata Motors", "HDFC Bank"][
      Math.floor(Math.random() * 4)
    ],
    reportMonth: "2026-07",
    generatedAt: new Date(Date.now() - Math.random() * 10000000).toISOString(),
    runtimeMs: Math.random() * 500 + 400,
    pptPath: `C:/reports/output_${i}.pptx`,
    fileSizeKb: Math.random() * 5000 + 1000,
  }));

  async getReports(): Promise<Report[]> {
    await delay(600);
    return [...this.reports];
  }

  async getReport(id: string): Promise<Report> {
    await delay(300);
    const report = this.reports.find((r) => r.id === id);
    if (!report) throw new Error("Report not found");
    return report;
  }

  async deleteReport(id: string): Promise<void> {
    await delay(500);
    this.reports = this.reports.filter((r) => r.id !== id);
  }
}
