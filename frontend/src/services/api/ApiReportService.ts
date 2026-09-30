import { IReportService } from "../interfaces";
import { Report } from "../../types/report";
import { ApiClient } from "./ApiClient";

export class ApiReportService implements IReportService {
  async getReports(): Promise<Report[]> {
    const res = await ApiClient.fetch(`/reports`);
    if (!res.ok) throw new Error("Failed to fetch reports");
    return res.json();
  }

  async getReport(id: string): Promise<Report> {
    return {} as Report; // Not fully implemented
  }

  async deleteReport(id: string): Promise<void> {
    const res = await ApiClient.fetch(`/reports/${id}`, {
      method: "DELETE"
    });
    if (!res.ok) throw new Error("Failed to delete report");
  }
}
