import { useFormContext } from "react-hook-form";
import { GenerateFormValues } from "../validation";
import { MOCK_CUSTOMERS } from "../mockData";
import { useAuthStore } from "../../../stores/useAuthStore";
import { motion, AnimatePresence } from "framer-motion";
import { Server, MapPin, Activity } from "lucide-react";
import { cn } from "../../../utils/cn";
import { useMemo } from "react";

export function ServiceSelectionTable() {
  const { watch, setValue } = useFormContext<GenerateFormValues>();
  const customerName = watch("customerName");
  const selectedServiceIds = watch("selectedServiceIds") || [];
  const { user } = useAuthStore();

  const allowedCustomers = useMemo(() => {
    if (!user || user.role === "admin") return MOCK_CUSTOMERS;
    if (user.live_sync) return user.customers as typeof MOCK_CUSTOMERS;
    return MOCK_CUSTOMERS.filter(c => user.customers.includes(c.name));
  }, [user]);

  const customer = allowedCustomers.find(c => c.name === customerName);

  if (!customerName || !customer) return null;

  const allSelected = customer.services.length > 0 && selectedServiceIds.length === customer.services.length;
  const someSelected = selectedServiceIds.length > 0 && selectedServiceIds.length < customer.services.length;

  const toggleAll = () => {
    if (allSelected) {
      setValue("selectedServiceIds", []);
    } else {
      setValue("selectedServiceIds", customer.services.map(s => s.id));
    }
  };

  const toggleService = (id: string) => {
    if (selectedServiceIds.includes(id)) {
      setValue("selectedServiceIds", selectedServiceIds.filter(s => s !== id));
    } else {
      setValue("selectedServiceIds", [...selectedServiceIds, id]);
    }
  };

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0, height: 0, marginTop: 0 }}
        animate={{ opacity: 1, height: "auto", marginTop: 24 }}
        exit={{ opacity: 0, height: 0, marginTop: 0 }}
        className="overflow-hidden"
      >
        <div className="bg-card border border-border rounded-xl shadow-sm overflow-hidden">
          <div className="p-4 border-b border-border bg-muted/30 flex items-center justify-between">
            <h3 className="font-semibold text-foreground flex items-center gap-2">
              <Server size={18} className="text-primary" />
              Active Services for {customerName}
            </h3>
            <span className="text-sm text-muted-foreground bg-background px-2 py-1 rounded-md border border-border">
              {selectedServiceIds.length} of {customer.services.length} Selected
            </span>
          </div>
          
          <div className="overflow-x-auto">
            <table className="w-full text-sm text-left">
              <thead className="text-xs text-muted-foreground bg-muted/10 border-b border-border">
                <tr>
                  <th className="px-4 py-3 w-12 text-center">
                    <input 
                      type="checkbox" 
                      className="rounded border-border text-primary focus:ring-primary/20 cursor-pointer"
                      checked={allSelected}
                      ref={input => {
                        if (input) input.indeterminate = someSelected;
                      }}
                      onChange={toggleAll}
                    />
                  </th>
                  <th className="px-4 py-3 font-medium">Service ID</th>
                  <th className="px-4 py-3 font-medium">Type</th>
                  <th className="px-4 py-3 font-medium">Location</th>
                  <th className="px-4 py-3 font-medium">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border">
                {customer.services.map((service, idx) => (
                  <motion.tr 
                    key={service.id}
                    initial={{ opacity: 0, x: -10 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: idx * 0.05 }}
                    className={cn(
                      "hover:bg-muted/30 transition-colors cursor-pointer",
                      selectedServiceIds.includes(service.id) ? "" : "opacity-60 bg-muted/10"
                    )}
                    onClick={() => toggleService(service.id)}
                  >
                    <td className="px-4 py-3 text-center" onClick={(e) => e.stopPropagation()}>
                      <input 
                        type="checkbox" 
                        className="rounded border-border text-primary focus:ring-primary/20 cursor-pointer"
                        checked={selectedServiceIds.includes(service.id)}
                        onChange={() => toggleService(service.id)}
                      />
                    </td>
                    <td className="px-4 py-3 font-medium text-foreground">{service.id}</td>
                    <td className="px-4 py-3">
                      <span className="bg-primary/10 text-primary px-2 py-1 rounded-full text-xs font-medium">
                        {service.type}
                      </span>
                    </td>
                    <td className="px-4 py-3">
                      <div className="flex items-center gap-1.5 text-muted-foreground">
                        <MapPin size={14} />
                        {service.location}
                      </div>
                    </td>
                    <td className="px-4 py-3">
                      <div className="flex items-center gap-1.5">
                        <Activity size={14} className={service.status === 'Active' ? 'text-green-500' : 'text-amber-500'} />
                        <span className={service.status === 'Active' ? 'text-foreground' : 'text-muted-foreground'}>
                          {service.status}
                        </span>
                      </div>
                    </td>
                  </motion.tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </motion.div>
    </AnimatePresence>
  );
}
