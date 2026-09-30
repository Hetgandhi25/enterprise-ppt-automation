import { useQuery } from "@tanstack/react-query";
import { jobService } from "../../../services/ServiceProvider";

export function useJobs() {
  return useQuery({
    queryKey: ["jobs"],
    queryFn: () => jobService.getJobs(),
    refetchInterval: 3000, // Poll every 3 seconds for live updates
  });
}

export function useJob(id: string) {
  return useQuery({
    queryKey: ["job", id],
    queryFn: () => jobService.getJob(id),
    refetchInterval: (query) => {
      // Stop polling if completed or failed
      const status = query.state.data?.status;
      if (status === "COMPLETED" || status === "FAILED") return false;
      return 3000;
    },
    enabled: !!id,
  });
}
