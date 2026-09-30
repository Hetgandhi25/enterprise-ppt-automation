import { z } from "zod";

export const generateFormSchema = z.object({
  customerName: z.string().min(1, "Customer name is required"),
  reportMonth: z.string().min(1, "Report month is required"),
  outputFolder: z.string().min(1, "Output folder is required"),
  selectedServiceIds: z.array(z.string()).min(1, "At least one service must be selected"),
  
  // Advanced Options
  headless: z.boolean(),
  retryCount: z.number().min(0).max(5),
  
  // Feature Flags
  enableCharts: z.boolean(),
  enablePpt: z.boolean(),
  enableMetrics: z.boolean(),
  enableLogging: z.boolean(),
  enableNotifications: z.boolean(),
  enableCleanup: z.boolean(),
});

export type GenerateFormValues = z.infer<typeof generateFormSchema>;
