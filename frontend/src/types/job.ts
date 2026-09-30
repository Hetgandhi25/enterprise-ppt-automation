import { TaskStatusEnum } from "./taskStatus";

export interface Job {
  id: string;
  customerName: string;
  reportMonth: string;
  status: TaskStatusEnum;
  progressPercentage: number;
  startTime: string;
  endTime?: string;
  runtimeMs?: number;
  error?: string;
  warnings: string[];
  outputPath?: string;
}
