import { IJobService } from "../interfaces";
import { Job } from "../../types/job";
import { TaskStatusEnum } from "../../types/taskStatus";

// Simulated delay helper
const delay = (ms: number) => new Promise((res) => setTimeout(res, ms));

export class MockJobService implements IJobService {
  private jobs: Job[] = Array.from({ length: 100 }).map((_, i) => ({
    id: `JOB-${1000 + i}`,
    customerName: ["ASG India", "Sun Pharma", "Tata Motors", "HDFC Bank"][
      Math.floor(Math.random() * 4)
    ],
    reportMonth: "2026-07",
    status: Math.random() > 0.1 ? TaskStatusEnum.COMPLETED : TaskStatusEnum.FAILED,
    progressPercentage: 100,
    startTime: new Date(Date.now() - Math.random() * 10000000).toISOString(),
    runtimeMs: Math.random() * 500 + 400,
    warnings: [],
  }));

  async getJobs(): Promise<Job[]> {
    await delay(500);
    return [...this.jobs];
  }

  async getJob(id: string): Promise<Job> {
    await delay(300);
    const job = this.jobs.find((j) => j.id === id);
    if (!job) throw new Error("Job not found");
    return job;
  }

  async generateReport(payload: { customerName: string; reportMonth: string; [key: string]: any }): Promise<Job> {
    await delay(800);
    const newJob: Job = {
      id: `JOB-${1000 + this.jobs.length}`,
      customerName: payload.customerName,
      reportMonth: payload.reportMonth,
      status: TaskStatusEnum.PENDING,
      progressPercentage: 0,
      startTime: new Date().toISOString(),
      warnings: [],
    };
    this.jobs.unshift(newJob);
    return newJob;
  }

  async cancelJob(id: string): Promise<void> {
    await delay(400);
    const job = this.jobs.find((j) => j.id === id);
    if (job) {
      job.status = TaskStatusEnum.FAILED;
      job.error = "Cancelled by user";
    }
  }

  async deleteJob(id: string): Promise<void> {
    await delay(400);
    this.jobs = this.jobs.filter(j => j.id !== id);
  }
}
