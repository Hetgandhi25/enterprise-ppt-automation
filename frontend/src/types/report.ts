export interface Report {
  id: string;
  jobId: string;
  customerName: string;
  reportMonth: string;
  generatedAt: string;
  runtimeMs: number;
  pptPath: string;
  fileSizeKb?: number;
}
