import { BrowserRouter, Routes, Route } from "react-router-dom";
import { ThemeProvider } from "./components/ThemeProvider";
import { AppLayout } from "./layouts/AppLayout";
import { Toaster } from "sonner";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import ErrorBoundary from "./components/shared/ErrorBoundary";

// Features
import { DashboardFeature } from "./features/dashboard/DashboardFeature";
import { GenerateFeature } from "./features/generate/GenerateFeature";
import { JobsFeature } from "./features/jobs/JobsFeature";
import { ReportsFeature } from "./features/reports/ReportsFeature";
import { SettingsFeature } from "./features/settings/SettingsFeature";
import { LogsFeature } from "./features/logs/LogsFeature";
import { HelpFeature } from "./features/help/HelpFeature";
import { LoginFeature } from "./features/auth/LoginFeature";
import { ProtectedRoute } from "./components/auth/ProtectedRoute";
import { RoleRoute } from "./components/auth/RoleRoute";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});

export default function App() {
  return (
    <ErrorBoundary>
      <QueryClientProvider client={queryClient}>
        <ThemeProvider>
          <BrowserRouter>
            <Routes>
              {/* Public route */}
              <Route path="/login" element={<LoginFeature />} />

              {/* Protected routes */}
              <Route element={<ProtectedRoute />}>
                <Route element={<AppLayout />}>
                  <Route path="/" element={<DashboardFeature />} />
                  <Route path="/generate" element={<GenerateFeature />} />
                  <Route path="/jobs" element={<JobsFeature />} />
                  <Route path="/reports" element={<ReportsFeature />} />
                  <Route path="/help" element={<HelpFeature />} />
                  
                  {/* Admin Only Routes */}
                  <Route element={<RoleRoute allowedRoles={["admin"]} />}>
                    <Route path="/logs" element={<LogsFeature />} />
                    <Route path="/settings" element={<SettingsFeature />} />
                  </Route>
                </Route>
              </Route>
            </Routes>
          </BrowserRouter>
          <Toaster position="top-right" theme="system" richColors />
        </ThemeProvider>
      </QueryClientProvider>
    </ErrorBoundary>
  );
}
