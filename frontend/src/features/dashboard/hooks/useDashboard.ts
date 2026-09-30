import { useQuery } from "@tanstack/react-query";
import { dashboardService } from "../../../services/ServiceProvider";

export function useDashboard() {
  return useQuery({
    queryKey: ["dashboard-stats"],
    queryFn: () => dashboardService.getStats(),
    staleTime: 60000,
  });
}
