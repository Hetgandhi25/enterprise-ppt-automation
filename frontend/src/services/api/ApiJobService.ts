import { IJobService } from "../interfaces";
import { Job } from "../../types/job";
import { TaskStatusEnum } from "../../types/taskStatus";
import { ApiClient } from "./ApiClient";

export class ApiJobService implements IJobService {
  async getJobs(): Promise<Job[]> {
    const res = await ApiClient.fetch(`/jobs`);
    if (!res.ok) throw new Error("Failed to fetch jobs");
    return res.json();
  }

  async getJob(id: string): Promise<Job> {
    return {} as Job; // Not fully implemented yet
  }

  async generateReport(payload: { customerName: string; reportMonth: string; [key: string]: any }): Promise<Job> {
    const res = await ApiClient.fetch(`/generate`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        customerName: payload.customerName,
        reportMonth: payload.reportMonth,
        demoMode: true,
      }),
    });
    
    if (!res.ok) {
      const errorData = await res.json().catch(() => null);
      throw new Error(errorData?.detail || "Generation failed from backend.");
    }
    
    return res.json();
  }

  async cancelJob(id: string): Promise<void> {
    const res = await ApiClient.fetch(`/jobs/${id}/cancel`, {
      method: "POST"
    });
    if (!res.ok) throw new Error("Failed to cancel job");
  }

  async deleteJob(id: string): Promise<void> {
    const res = await ApiClient.fetch(`/jobs/${id}`, {
      method: "DELETE"
    });
    if (!res.ok) throw new Error("Failed to delete job");
  }
}
