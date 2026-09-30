import { useState, useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Search, FilePlus, LayoutDashboard, List, FileText, Settings, ScrollText, HelpCircle, User } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { useSettingsStore } from "../../stores/useSettingsStore";

export function CommandPalette() {
  const [isOpen, setIsOpen] = useState(false);
  const [search, setSearch] = useState("");
  const inputRef = useRef<HTMLInputElement>(null);
  const navigate = useNavigate();
  const { setTheme, theme } = useSettingsStore();

  useEffect(() => {
    const down = (e: KeyboardEvent) => {
      if (e.key === "k" && (e.metaKey || e.ctrlKey)) {
        e.preventDefault();
        setIsOpen((open) => !open);
      }
      if (e.key === "Escape") {
        setIsOpen(false);
      }
    };
    document.addEventListener("keydown", down);
    return () => document.removeEventListener("keydown", down);
  }, []);

  useEffect(() => {
    if (isOpen) {
      setTimeout(() => inputRef.current?.focus(), 50);
      setSearch("");
    }
  }, [isOpen]);

  const actions = [
    { id: "dashboard", label: "Go to Dashboard", icon: <LayoutDashboard size={16} />, onSelect: () => navigate("/") },
    { id: "generate", label: "Generate New Report", icon: <FilePlus size={16} />, onSelect: () => navigate("/generate") },
    { id: "jobs", label: "View Jobs", icon: <List size={16} />, onSelect: () => navigate("/jobs") },
    { id: "reports", label: "View Reports", icon: <FileText size={16} />, onSelect: () => navigate("/reports") },
    { id: "settings", label: "Open Settings", icon: <Settings size={16} />, onSelect: () => navigate("/settings") },
    { id: "logs", label: "View Logs", icon: <ScrollText size={16} />, onSelect: () => navigate("/logs") },
    { id: "theme", label: `Toggle Theme (Current: ${theme})`, icon: <User size={16} />, onSelect: () => setTheme(theme === "dark" ? "light" : "dark") },
  ];

  const filteredActions = actions.filter(a => a.label.toLowerCase().includes(search.toLowerCase()));

  const handleSelect = (action: typeof actions[0]) => {
    action.onSelect();
    setIsOpen(false);
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 z-50 flex items-start justify-center pt-[15vh] px-4">
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={() => setIsOpen(false)}
            className="absolute inset-0 bg-background/80 backdrop-blur-sm"
          />
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            transition={{ duration: 0.15 }}
            className="w-full max-w-2xl bg-card border border-border rounded-xl shadow-2xl relative overflow-hidden flex flex-col"
          >
            <div className="flex items-center p-4 border-b border-border">
              <Search className="text-muted-foreground mr-3 shrink-0" size={20} />
              <input
                ref={inputRef}
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Type a command or search..."
                className="w-full bg-transparent border-none focus:outline-none focus:ring-0 text-foreground text-lg placeholder:text-muted-foreground/60"
              />
              <div className="flex items-center gap-1 text-xs text-muted-foreground bg-muted px-2 py-1 rounded shrink-0">
                <kbd>ESC</kbd> to close
              </div>
            </div>
            
            <div className="max-h-[60vh] overflow-y-auto p-2">
              {filteredActions.length === 0 ? (
                <div className="p-8 text-center text-muted-foreground">
                  No results found.
                </div>
              ) : (
                <div className="space-y-1">
                  {filteredActions.map((action, i) => (
                    <button
                      key={action.id}
                      onClick={() => handleSelect(action)}
                      className="w-full flex items-center gap-3 px-4 py-3 rounded-md text-sm text-foreground hover:bg-primary hover:text-primary-foreground transition-colors group"
                      tabIndex={0}
                    >
                      <div className="text-muted-foreground group-hover:text-primary-foreground/80">
                        {action.icon}
                      </div>
                      {action.label}
                    </button>
                  ))}
                </div>
              )}
            </div>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
}
