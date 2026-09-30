import { useState } from "react";
import { useForm, FormProvider } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { generateFormSchema, GenerateFormValues } from "./validation";
import { PageHeader } from "../../components/shared/Headers";
import { CustomerSelector } from "./components/CustomerSelector";
import { MonthSelector } from "./components/MonthSelector";
import { OutputFolderSelector } from "./components/OutputFolderSelector";
import { AdvancedOptions } from "./components/AdvancedOptions";
import { GenerateSummaryCard } from "./components/GenerateSummaryCard";
import { ServiceSelectionTable } from "./components/ServiceSelectionTable";
import { ProgressDialog } from "./components/ProgressDialog";
import { SuccessDialog } from "./components/SuccessDialog";
import { FailureDialog } from "./components/FailureDialog";
import { useGenerateReport } from "./hooks/useGenerateReport";
import { useSettingsStore } from "../../stores/useSettingsStore";
import { Job } from "../../types/job";
import { TaskStatusEnum } from "../../types/taskStatus";
import { motion } from "framer-motion";

export function GenerateFeature() {
  const { outputFolder, headless, retryCount, featureFlags } = useSettingsStore();
  const generateMutation = useGenerateReport();

  const methods = useForm<GenerateFormValues>({
    resolver: zodResolver(generateFormSchema),
    defaultValues: {
      customerName: "",
      reportMonth: "",
      outputFolder: outputFolder,
      headless: headless,
      retryCount: retryCount,
      enableCharts: featureFlags.enableCharts,
      enablePpt: featureFlags.enablePpt,
      enableMetrics: featureFlags.enableMetrics,
      enableLogging: featureFlags.enableLogging,
      enableNotifications: featureFlags.enableNotifications,
      enableCleanup: featureFlags.enableCleanup,
    }
  });

  const [activeJob, setActiveJob] = useState<Job | null>(null);
  const [dialogState, setDialogState] = useState<"none" | "progress" | "success" | "failure">("none");

  const onSubmit = async (data: GenerateFormValues) => {
    let interval: NodeJS.Timeout | undefined;
    try {
      // 1. Open progress dialog with generating state
      setActiveJob({
        id: "generating",
        customerName: data.customerName,
        reportMonth: data.reportMonth,
        status: TaskStatusEnum.PENDING,
        progressPercentage: 5,
        startTime: new Date().toISOString()
      } as Job);
      setDialogState("progress");

      // Simulate progression while waiting for the synchronous backend call
      interval = setInterval(() => {
        setActiveJob(prev => {
          if (!prev) return prev;
          let newPct = prev.progressPercentage + 8;
          if (newPct > 95) newPct = 95; // cap at 95% until complete
          
          let newStatus = prev.status;
          if (newPct >= 20) newStatus = TaskStatusEnum.DOWNLOADING;
          if (newPct >= 40) newStatus = TaskStatusEnum.PROCESSING_INVENTORY;
          if (newPct >= 60) newStatus = TaskStatusEnum.GENERATING_CHARTS;
          if (newPct >= 80) newStatus = TaskStatusEnum.GENERATING_PPT;
          if (newPct >= 90) newStatus = TaskStatusEnum.CLEANUP;
          
          return { ...prev, status: newStatus, progressPercentage: newPct };
        });
      }, 1000);

      // 2. Trigger the mutation to create the job in the real backend
      const job = await generateMutation.mutateAsync(data);
      clearInterval(interval);
      
      // 3. Success
      setActiveJob(job);
      setDialogState("success");
    } catch (e: any) {
      clearInterval(interval);
      setActiveJob({
        id: "failed",
        customerName: data.customerName,
        reportMonth: data.reportMonth,
        status: TaskStatusEnum.FAILED,
        progressPercentage: 0,
        startTime: new Date().toISOString(),
        error: e.message || "An error occurred."
      } as Job);
      setDialogState("failure");
    }
  };

  const resetForm = () => {
    methods.reset({ ...methods.getValues(), customerName: "", reportMonth: "" });
    setDialogState("none");
    setActiveJob(null);
  };

  return (
    <div className="max-w-6xl mx-auto space-y-8 pb-8">
      <PageHeader 
        title="Generate Report" 
        description="Configure and launch a new presentation generation job." 
      />

      <FormProvider {...methods}>
        <form onSubmit={methods.handleSubmit(onSubmit)} className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          
          <div className="lg:col-span-2 space-y-6">
            <motion.div 
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-card border border-border rounded-xl p-6 shadow-sm space-y-6"
            >
              <h2 className="text-lg font-semibold text-foreground border-b border-border pb-4">Target Information</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <CustomerSelector />
                <MonthSelector />
              </div>
            </motion.div>

            <ServiceSelectionTable />

          </div>

          <div className="lg:col-span-1">
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.3 }}
            >
              <GenerateSummaryCard />
            </motion.div>
          </div>
        </form>
      </FormProvider>

      <ProgressDialog 
        isOpen={dialogState === "progress"} 
        job={activeJob} 
      />
      
      <SuccessDialog 
        isOpen={dialogState === "success"} 
        job={activeJob} 
        onClose={resetForm}
      />
      
      <FailureDialog 
        isOpen={dialogState === "failure"} 
        job={activeJob} 
        onClose={resetForm}
        onRetry={() => {
          setDialogState("progress");
          if (activeJob) {
             setActiveJob({ ...activeJob, status: TaskStatusEnum.PENDING, progressPercentage: 0, startTime: new Date().toISOString() });
          }
        }}
      />
    </div>
  );
}
