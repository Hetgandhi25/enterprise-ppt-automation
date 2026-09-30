import { Report } from "../../../types/report";
import { ReportCard } from "./ReportCard";

interface Props {
  reports: Report[];
  onReportClick: (r: Report) => void;
}

export function ReportsGrid({ reports, onReportClick }: Props) {
  if (reports.length === 0) {
    return (
      <div className="py-12 text-center text-muted-foreground">
        No reports found matching the current filters.
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 xl:grid-cols-5 2xl:grid-cols-6 gap-4">
      {reports.map((report) => (
        <ReportCard key={report.id} report={report} onClick={onReportClick} />
      ))}
    </div>
  );
}
