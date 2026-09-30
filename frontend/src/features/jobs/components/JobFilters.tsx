import { Job } from "../../../types/job";
import { TaskStatusEnum } from "../../../types/taskStatus";
import { useAuthStore } from "../../../stores/useAuthStore";
import { MOCK_CUSTOMERS } from "../../generate/mockData";

interface Props {
  statusFilter: string;
  setStatusFilter: (v: string) => void;
  customerFilter: string;
  setCustomerFilter: (v: string) => void;
}

export function JobFilters({ statusFilter, setStatusFilter, customerFilter, setCustomerFilter }: Props) {
  const { user } = useAuthStore();
  
  const allowedCustomers = user?.role === "admin" 
    ? MOCK_CUSTOMERS.map(c => c.name) 
    : (user?.customers || []).map(c => typeof c === 'string' ? c : c.name);

  return (
    <div className="flex flex-wrap items-center gap-4">
      <select
        value={statusFilter}
        onChange={(e) => setStatusFilter(e.target.value)}
        className="h-9 px-3 bg-card border border-border rounded-md text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-primary/20"
      >
        <option value="ALL">All Statuses</option>
        {Object.values(TaskStatusEnum).map(status => (
          <option key={status} value={status}>{status.replace(/_/g, ' ')}</option>
        ))}
      </select>

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
    </div>
  );
}
