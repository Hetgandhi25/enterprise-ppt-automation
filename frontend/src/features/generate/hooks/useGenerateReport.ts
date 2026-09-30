import { useMutation, useQueryClient } from "@tanstack/react-query";
import { jobService } from "../../../services/ServiceProvider";
import { GenerateFormValues } from "../validation";
import { toast } from "sonner";

export function useGenerateReport() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (payload: GenerateFormValues) => jobService.generateReport(payload),
    onSuccess: () => {
      // Invalidate relevant queries to keep dashboard fresh
      queryClient.invalidateQueries({ queryKey: ["dashboard-stats"] });
      queryClient.invalidateQueries({ queryKey: ["recent-jobs"] });
      queryClient.invalidateQueries({ queryKey: ["recent-reports"] });
    },
    onError: (error) => {
      toast.error(error.message || "Failed to initialize generation job.");
    }
  });
}
