import { useState, useRef, useEffect, useMemo } from "react";
import Fuse from "fuse.js";
import { useFormContext } from "react-hook-form";
import { GenerateFormValues } from "../validation";
import { User, Search, Check, ChevronDown, X } from "lucide-react";
import { cn } from "../../../utils/cn";
import { MOCK_CUSTOMERS } from "../mockData";
import { useAuthStore } from "../../../stores/useAuthStore";

export function CustomerSelector() {
  const { register, setValue, watch, formState: { errors } } = useFormContext<GenerateFormValues>();
  const { user } = useAuthStore();
  const [isOpen, setIsOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const containerRef = useRef<HTMLDivElement>(null);
  
  const selectedValue = watch("customerName");
  
  const allowedCustomers = useMemo(() => {
    if (!user || user.role === "admin") return MOCK_CUSTOMERS;
    
    if (user.live_sync) {
      // The backend now returns a deep structure matching the expected format!
      return user.customers as typeof MOCK_CUSTOMERS;
    }
    
    return MOCK_CUSTOMERS.filter(c => user.customers.includes(c.name));
  }, [user]);

  const fuse = useMemo(() => new Fuse(allowedCustomers, {
    keys: [
      { name: 'name', weight: 0.5 },
      { name: 'id', weight: 0.3 },
      { name: 'services.id', weight: 0.2 }
    ],
    threshold: 0.4, // Allows for spelling mistakes
    ignoreLocation: true,
    includeMatches: true,
  }), [allowedCustomers]);

  const filteredCustomers = useMemo(() => {
    if (!searchQuery.trim()) {
      return allowedCustomers.map(c => ({ item: c, matches: [] }));
    }
    return fuse.search(searchQuery);
  }, [searchQuery, fuse, allowedCustomers]);

  // Handle clicking outside to close dropdown
  useEffect(() => {
    const handleOutsideClick = (e: MouseEvent) => {
      if (containerRef.current && !containerRef.current.contains(e.target as Node)) {
        setIsOpen(false);
      }
    };
    document.addEventListener("mousedown", handleOutsideClick);
    return () => document.removeEventListener("mousedown", handleOutsideClick);
  }, []);

  return (
    <div className="space-y-2 relative" ref={containerRef}>
      <label className="text-sm font-medium text-foreground">Customer</label>
      
      {/* Hidden input to maintain react-hook-form integration */}
      <input type="hidden" {...register("customerName")} />
      
      {/* Combobox Trigger */}
      <div 
        onClick={() => setIsOpen(true)}
        className={cn(
          "w-full min-h-10 px-3 bg-background border rounded-md text-sm flex items-center justify-between cursor-text transition-all",
          isOpen ? "border-primary ring-2 ring-primary/20" : "border-border",
          errors.customerName ? "border-destructive" : ""
        )}
      >
        <div className="flex items-center gap-2 flex-1">
          <Search size={16} className="text-muted-foreground shrink-0" />
          <input
            type="text"
            className="w-full bg-transparent focus:outline-none text-foreground placeholder:text-muted-foreground"
            placeholder="Search by name, CustID, or Service ID..."
            value={isOpen ? searchQuery : (selectedValue || "")}
            onChange={(e) => {
              setSearchQuery(e.target.value);
              setIsOpen(true);
              if (!e.target.value) {
                setValue("customerName", "");
                setValue("selectedServiceIds", []);
              }
            }}
            onFocus={() => setIsOpen(true)}
          />
        </div>
        
        {/* Clear Button or Chevron */}
        {(searchQuery || selectedValue) ? (
          <button
            type="button"
            onClick={(e) => {
              e.stopPropagation();
              setSearchQuery("");
              setValue("customerName", "", { shouldValidate: true });
              setValue("selectedServiceIds", []);
              setIsOpen(true); // Keep it open after clearing so they can select a new one
            }}
            className="p-1 rounded-md hover:bg-muted text-muted-foreground hover:text-foreground transition-colors shrink-0"
          >
            <X size={16} />
          </button>
        ) : (
          <ChevronDown size={16} className="text-muted-foreground shrink-0" />
        )}
      </div>

      {/* Dropdown Menu */}
      {isOpen && (
        <div className="absolute top-full left-0 right-0 mt-1 bg-card border border-border rounded-lg shadow-lg max-h-60 overflow-y-auto z-50 p-1">
          {filteredCustomers.length === 0 ? (
            <div className="p-3 text-sm text-muted-foreground text-center">No customers found.</div>
          ) : (
            filteredCustomers.map(result => {
              const c = result.item;
              const matches = result.matches || [];
              const serviceMatch = matches.find(m => m.key === "services.id");
              const matchedServiceId = serviceMatch?.value;

              return (
                <div 
                  key={c.id}
                  onClick={() => {
                    setValue("customerName", c.name, { shouldValidate: true });
                    // Default to selecting all services for the new customer
                    setValue("selectedServiceIds", c.services.map(s => s.id));
                    setSearchQuery(c.name);
                    setIsOpen(false);
                  }}
                  className={cn(
                    "flex flex-col p-2 rounded-md cursor-pointer transition-colors",
                    selectedValue === c.name ? "bg-primary/10 text-primary" : "hover:bg-muted"
                  )}
                >
                  <div className="flex items-center justify-between">
                    <span className="font-medium">{c.name}</span>
                    {selectedValue === c.name && <Check size={16} />}
                  </div>
                  <div className="flex flex-col gap-1 mt-1 text-xs text-muted-foreground">
                    <div className="flex items-center gap-2">
                      <span className="bg-background px-1.5 py-0.5 rounded border border-border">ID: {c.id}</span>
                      {!matchedServiceId && (
                        <span className="opacity-80">({c.services.length} Active Services)</span>
                      )}
                    </div>
                    
                    {matchedServiceId && (
                      <div className="text-primary font-medium bg-primary/5 px-2 py-1 rounded w-fit mt-0.5">
                        🎯 Matched Service: {matchedServiceId}
                      </div>
                    )}
                  </div>
                </div>
              );
            })
          )}
        </div>
      )}
      
      {errors.customerName && <p className="text-xs text-destructive">{errors.customerName.message}</p>}
    </div>
  );
}
