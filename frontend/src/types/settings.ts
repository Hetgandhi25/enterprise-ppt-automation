import { FeatureFlags } from "./featureFlags";

export enum AppMode {
  DEMO = "demo",
  PRODUCTION = "production",
}

export interface Settings {
  // General
  appMode: AppMode;
  language: string;
  timezone: string;
  recentCustomers: string[];

  // Appearance
  theme: "light" | "dark" | "system";
  sidebarCollapsed: boolean;
  compactDensity: boolean;
  reduceMotion: boolean;
  reportsViewMode: "grid" | "table";

  // Automation
  headless: boolean;
  retryCount: number;
  screenshot: boolean;
  parallelJobs: number;

  // Output
  outputFolder: string;
  templateFolder: string;
  chartFolder: string;
  tempFolder: string;

  // Notifications
  enableNotifications: boolean;
  successToasts: boolean;
  failureToasts: boolean;
  desktopNotifications: boolean;

  // Feature Flags
  featureFlags: FeatureFlags;
}
