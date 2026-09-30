import { useQuery } from "@tanstack/react-query";
import { reportService } from "../../../services/ServiceProvider";

export function useRecentReports(limit = 5) {
  return useQuery({
    queryKey: ["recent-reports", limit],
    queryFn: async () => {
      const reports = await reportService.getReports();
      return reports
        .sort((a, b) => new Date(b.generatedAt).getTime() - new Date(a.generatedAt).getTime())
        .slice(0, limit);
    },
    staleTime: 30000,
  });
}
