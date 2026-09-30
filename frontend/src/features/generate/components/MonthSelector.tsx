import { useFormContext } from "react-hook-form";
import { GenerateFormValues } from "../validation";
import { Calendar } from "lucide-react";

export function MonthSelector() {
  const { register, formState: { errors } } = useFormContext<GenerateFormValues>();

  const getRecentMonths = () => {
    const months = [];
    const now = new Date();
    for (let i = 0; i < 6; i++) {
      const d = new Date(now.getFullYear(), now.getMonth() - i, 1);
      const val = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}`;
      const label = d.toLocaleString('default', { month: 'long', year: 'numeric' });
      months.push({ value: val, label });
    }
    return months;
  };

  return (
    <div className="space-y-2">
      <label className="text-sm font-medium text-foreground">Report Month</label>
      <div className="relative">
        <Calendar size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground" />
        <select 
          {...register("reportMonth")}
          className="w-full h-10 pl-9 pr-4 bg-background border border-border rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-primary/20 appearance-none"
        >
          <option value="">Select month...</option>
          {getRecentMonths().map(m => (
            <option key={m.value} value={m.value}>{m.label}</option>
          ))}
        </select>
      </div>
      {errors.reportMonth && <p className="text-xs text-destructive">{errors.reportMonth.message}</p>}
    </div>
  );
}
