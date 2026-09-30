import { create } from "zustand";
import { persist } from "zustand/middleware";
import { AppMode, Settings } from "../types/settings";

const defaultSettings: Settings = {
  appMode: AppMode.DEMO,
  language: "en-US",
  timezone: "UTC",
  recentCustomers: [],
  theme: "system",
  sidebarCollapsed: false,
  compactDensity: false,
  reduceMotion: false,
  reportsViewMode: "grid",
  headless: true,
  retryCount: 3,
  screenshot: true,
  parallelJobs: 2,
  outputFolder: "output/presentations",
  templateFolder: "templates",
  chartFolder: "output/charts",
  tempFolder: "tmp",
  enableNotifications: true,
  successToasts: true,
  failureToasts: true,
  desktopNotifications: false,
  featureFlags: {
    enableCharts: true,
    enablePpt: true,
    enableMetrics: true,
    enableLogging: true,
    enableNotifications: true,
    enableCleanup: true,
    experimentalFeatures: false,
  }
};

interface SettingsState extends Settings {
  updateSettings: (partial: Partial<Settings>) => void;
  updateFeatureFlags: (partial: Partial<Settings["featureFlags"]>) => void;
  
  // Shortcuts
  setTheme: (theme: "light" | "dark" | "system") => void;
  setAppMode: (mode: AppMode) => void;
  toggleSidebar: () => void;
  setReportsViewMode: (mode: "grid" | "table") => void;
  
  // Advanced
  resetSettings: () => void;
  importSettings: (json: string) => boolean;
}

export const useSettingsStore = create<SettingsState>()(
  persist(
    (set) => ({
      ...defaultSettings,

      updateSettings: (partial) => set((state) => ({ ...state, ...partial })),
      updateFeatureFlags: (partial) => set((state) => ({ 
        featureFlags: { ...state.featureFlags, ...partial } 
      })),

      setTheme: (theme) => set({ theme }),
      setAppMode: (appMode) => set({ appMode }),
      toggleSidebar: () => set((state) => ({ sidebarCollapsed: !state.sidebarCollapsed })),
      setReportsViewMode: (reportsViewMode) => set({ reportsViewMode }),

      resetSettings: () => set(defaultSettings),
      importSettings: (json: string) => {
        try {
          const parsed = JSON.parse(json);
          // Very basic validation - in production use Zod to validate the JSON payload completely
          if (parsed && typeof parsed === "object") {
             set((state) => ({ ...state, ...parsed }));
             return true;
          }
          return false;
        } catch {
          return false;
        }
      }
    }),
    {
      name: "ppt-automation-settings",
    }
  )
);
