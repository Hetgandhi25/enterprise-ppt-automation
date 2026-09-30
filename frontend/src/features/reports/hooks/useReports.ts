import { useQuery } from "@tanstack/react-query";
import { reportService } from "../../../services/ServiceProvider";

export function useReports() {
  return useQuery({
    queryKey: ["reports"],
    queryFn: () => reportService.getReports(),
  });
}

export function useReport(id: string) {
  return useQuery({
    queryKey: ["report", id],
    queryFn: () => reportService.getReport(id),
    enabled: !!id,
  });
}
