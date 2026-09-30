import { useAuthStore } from "../../../stores/useAuthStore";
import { MOCK_CUSTOMERS } from "../../generate/mockData";

interface Props {
  customerFilter: string;
  setCustomerFilter: (v: string) => void;
  monthFilter: string;
  setMonthFilter: (v: string) => void;
  statusFilter: string;
  setStatusFilter: (v: string) => void;
  customDateRange: { start: string, end: string };
  setCustomDateRange: (range: { start: string, end: string }) => void;
}

export function ReportFilters({ 
  customerFilter, setCustomerFilter,
  monthFilter, setMonthFilter,
  statusFilter, setStatusFilter,
  customDateRange, setCustomDateRange
}: Props) {
  const { user } = useAuthStore();
  
  const allowedCustomers = user?.role === "admin" 
    ? MOCK_CUSTOMERS.map(c => c.name) 
    : (user?.customers || []).map(c => typeof c === 'string' ? c : c.name);

  return (
    <div className="flex flex-wrap items-center gap-4">
      <select
        value={customerFilter}
        onChange={(e) => setCustomerFilter(e.target.value)}
        className="h-9 px-3 bg-card border border-border rounded-md text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-primary/20"
      >
        <option value="ALL">All Customers</option>
        {allowedCustomers.map(customerName => (
          <option key={customerName} value={customerName}>{customerName}</option>
        ))}
      </select>

      <select
        value={monthFilter}
        onChange={(e) => setMonthFilter(e.target.value)}
        className="h-9 px-3 bg-card border border-border rounded-md text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-primary/20"
      >
        <option value="ALL">All Months</option>
        <option value="Current Month">Current Month</option>
        <option value="Previous Month">Previous Month</option>
        <option value="Last 3 Months">Last 3 Months</option>
        <option value="Custom Month">Custom Month</option>
      </select>

      {monthFilter === "Custom Month" && (
        <div className="flex items-center gap-2">
          <input 
            type="date" 
            value={customDateRange.start}
            onChange={(e) => setCustomDateRange({ ...customDateRange, start: e.target.value })}
            className="h-9 px-3 bg-card border border-border rounded-md text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-primary/20 w-[130px]"
          />
          <span className="text-muted-foreground text-sm">to</span>
          <input 
            type="date" 
            value={customDateRange.end}
            onChange={(e) => setCustomDateRange({ ...customDateRange, end: e.target.value })}
            className="h-9 px-3 bg-card border border-border rounded-md text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-primary/20 w-[130px]"
          />
        </div>
      )}

      <select
        value={statusFilter}
        onChange={(e) => setStatusFilter(e.target.value)}
        className="h-9 px-3 bg-card border border-border rounded-md text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-primary/20"
      >
        <option value="ALL">All Statuses</option>
        <option value="Completed">Completed</option>
        <option value="Generating">Generating</option>
        <option value="Failed">Failed</option>
      </select>
    </div>
  );
}
