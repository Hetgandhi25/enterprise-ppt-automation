import { useQuery } from "@tanstack/react-query";
import { jobService } from "../../../services/ServiceProvider";

export function useRecentJobs(limit = 5) {
  return useQuery({
    queryKey: ["recent-jobs", limit],
    queryFn: async () => {
      const jobs = await jobService.getJobs();
      // Sort by start time descending and slice
      return jobs
        .sort((a, b) => new Date(b.startTime).getTime() - new Date(a.startTime).getTime())
        .slice(0, limit);
    },
    staleTime: 30000,
  });
}
