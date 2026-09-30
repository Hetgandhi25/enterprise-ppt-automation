import { useMutation, useQueryClient } from "@tanstack/react-query";
import { jobService } from "../../../services/ServiceProvider";
import { toast } from "sonner";

export function useCancelJob() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => jobService.cancelJob(id),
    onSuccess: (_, id) => {
      queryClient.invalidateQueries({ queryKey: ["jobs"] });
      queryClient.invalidateQueries({ queryKey: ["job", id] });
      toast.success(`Job ${id} cancelled successfully.`);
    },
    onError: () => toast.error("Failed to cancel job.")
  });
}

export function useDeleteJob() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => jobService.deleteJob(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["jobs"] });
      toast.success(`Job deleted successfully.`);
    },
    onError: () => toast.error("Failed to delete job.")
  });
}
