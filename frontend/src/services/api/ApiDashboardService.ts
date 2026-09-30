import { IDashboardService } from "../interfaces";
import { DashboardData } from "../../types/dashboard";
import { ApiClient } from "./ApiClient";

export class ApiDashboardService implements IDashboardService {
  async getStats(): Promise<DashboardData> {
    const response = await ApiClient.fetch("/dashboard/stats");
    if (!response.ok) {
      throw new Error(`Failed to fetch dashboard stats: ${response.statusText}`);
    }
    return response.json();
  }
}
