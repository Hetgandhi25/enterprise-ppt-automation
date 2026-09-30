import { useMutation, useQueryClient } from "@tanstack/react-query";
import { reportService } from "../../../services/ServiceProvider";
import { toast } from "sonner";

export function useDeleteReport() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => reportService.deleteReport(id),
    onSuccess: (_, id) => {
      queryClient.invalidateQueries({ queryKey: ["reports"] });
      queryClient.invalidateQueries({ queryKey: ["dashboard-stats"] });
      toast.success(`Report ${id} deleted successfully.`);
    },
    onError: () => toast.error("Failed to delete report.")
  });
}

import { dummyPptxBase64 } from "./dummyPptx";

export function useDownloadReport() {
  return useMutation({
    mutationFn: async (id: string) => {
      // Mock download logic
      const report = await reportService.getReport(id);
      return new Promise<void>((resolve) => {
        setTimeout(() => {
          const byteCharacters = atob(dummyPptxBase64);
          const byteNumbers = new Array(byteCharacters.length);
          for (let i = 0; i < byteCharacters.length; i++) {
            byteNumbers[i] = byteCharacters.charCodeAt(i);
          }
          const byteArray = new Uint8Array(byteNumbers);
          const blob = new Blob([byteArray], { type: "application/vnd.openxmlformats-officedocument.presentationml.presentation" });
          const url = window.URL.createObjectURL(blob);
          const a = document.createElement("a");
          a.href = url;
          a.download = `${report.customerName.replace(/\s+/g, "_")}_${report.reportMonth}.pptx`;
          document.body.appendChild(a);
          a.click();
          window.URL.revokeObjectURL(url);
          document.body.removeChild(a);
          resolve();
        }, 800);
      });
    },
    onSuccess: () => {
      toast.success("Download started successfully.");
    },
    onError: () => toast.error("Failed to download report.")
  });
}
