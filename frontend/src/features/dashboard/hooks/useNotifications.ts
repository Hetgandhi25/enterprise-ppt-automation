import { useMemo } from "react";
import { useAuthStore } from "../../../stores/useAuthStore";
import { useSettingsStore } from "../../../stores/useSettingsStore";
import { useRecentJobs } from "./useRecentJobs";
import { TaskStatusEnum } from "../../../types/taskStatus";
import { Bell, CheckCircle2, XCircle, ShieldAlert, Activity, Server, Clock } from "lucide-react";

export type NotificationItem = {
  id: string;
  type: "system" | "job_success" | "job_failed" | "alert";
  title: string;
  message: string;
  timestamp: Date;
  icon?: any;
  link?: string;
  isNew?: boolean;
};

export function useNotifications() {
  const { user } = useAuthStore();
  const { appMode } = useSettingsStore();
  const { data: recentJobs } = useRecentJobs(10); // Fetch a few more to filter

  const notifications = useMemo(() => {
    const notifs: NotificationItem[] = [];
    const now = new Date();

    // 1. System / Login Context
    if (user) {
      notifs.push({
        id: "sys-login",
        type: "system",
        title: "Session Active",
        message: `Welcome back, ${user.name}. You are logged in as ${user.role.toUpperCase()}.`,
        timestamp: new Date(now.getTime() - 1000 * 60 * 60), // 1 hour ago
        icon: Activity,
      });

      if (user.live_sync) {
        notifs.push({
          id: "sys-live",
          type: "system",
          title: "Live CRM Connection",
          message: "Secure connection to UAT Portal established successfully.",
          timestamp: new Date(now.getTime() - 1000 * 60 * 55),
          icon: Server,
        });
      } else {
        notifs.push({
          id: "sys-demo",
          type: "alert",
          title: "Demo Mode Active",
          message: "Live CRM sync is disabled. Showing mock data only.",
          timestamp: new Date(now.getTime() - 1000 * 60 * 55),
          icon: ShieldAlert,
        });
      }
    }

    // 2. Data Insights (computed from user customers)
    if (user?.customers && typeof user.customers[0] === 'object') {
      let activeServicesCount = 0;
      let inactiveServicesCount = 0;
      
      const complexCustomers = user.customers as any[];
      complexCustomers.forEach(c => {
        if (c.services && Array.isArray(c.services)) {
          c.services.forEach((s: any) => {
            if (s.status === "Active") activeServicesCount++;
            else inactiveServicesCount++;
          });
        }
      });

      notifs.push({
        id: "sys-insight",
        type: "system",
        title: "Portfolio Summary",
        message: `You are tracking ${activeServicesCount} Active and ${inactiveServicesCount} Inactive services.`,
        timestamp: new Date(now.getTime() - 1000 * 60 * 50),
        icon: Bell,
      });
    }

    // 3. Meaningful Job Alerts
    // We don't just dump all jobs. We specifically alert on FAILED jobs, or very recent COMPLETED jobs.
    if (recentJobs) {
      recentJobs.forEach(job => {
        const jobDate = new Date(job.startTime);
        const ageMs = now.getTime() - jobDate.getTime();
        const ageHours = ageMs / (1000 * 60 * 60);

        if (job.status === TaskStatusEnum.FAILED && ageHours < 24) {
          notifs.push({
            id: `job-${job.id}`,
            type: "job_failed",
            title: "Report Generation Failed",
            message: `Failed to generate report for ${job.customerName}.`,
            timestamp: jobDate,
            icon: XCircle,
            isNew: true,
          });
        } else if (job.status === TaskStatusEnum.COMPLETED && ageHours < 12) {
          notifs.push({
            id: `job-${job.id}`,
            type: "job_success",
            title: "Report Ready",
            message: `Presentation for ${job.customerName} is ready to download.`,
            timestamp: jobDate,
            icon: CheckCircle2,
            link: job.outputPath,
            isNew: ageHours < 1, // Considered "new" if generated in the last hour
          });
        } else if (job.status === TaskStatusEnum.PENDING || job.status === TaskStatusEnum.GENERATING_PPT) {
          notifs.push({
            id: `job-${job.id}`,
            type: "system",
            title: "Generation in Progress",
            message: `Currently rendering PPT for ${job.customerName}...`,
            timestamp: jobDate,
            icon: Clock,
            isNew: true,
          });
        }
      });
    }

    // Sort by timestamp descending
    return notifs.sort((a, b) => b.timestamp.getTime() - a.timestamp.getTime());
  }, [user, appMode, recentJobs]);

  return { data: notifications };
}
