import { Link, useLocation } from "react-router-dom";
import { cn } from "../utils/cn";
import { LayoutDashboard, FilePlus, List, FileText, Settings, ScrollText, HelpCircle, ChevronLeft, ChevronRight, LogOut } from "lucide-react";
import { useSettingsStore } from "../stores/useSettingsStore";
import { useAuthStore } from "../stores/useAuthStore";
import { motion } from "framer-motion";

const navItems = [
  { name: "Dashboard", path: "/", icon: LayoutDashboard, roles: ["admin", "csm"] },
  { name: "Generate", path: "/generate", icon: FilePlus, roles: ["admin", "csm"] },
  { name: "Jobs", path: "/jobs", icon: List, roles: ["admin", "csm"] },
  { name: "Reports", path: "/reports", icon: FileText, roles: ["admin", "csm"] },
  { name: "Logs", path: "/logs", icon: ScrollText, roles: ["admin"] },
  { name: "Settings", path: "/settings", icon: Settings, roles: ["admin"] },
  { name: "Help", path: "/help", icon: HelpCircle, roles: ["admin"] },
];

export function Sidebar() {
  const location = useLocation();
  const { sidebarCollapsed, toggleSidebar } = useSettingsStore();
  const { user, logout } = useAuthStore();

  return (
    <motion.aside
      initial={false}
      animate={{ width: sidebarCollapsed ? "5rem" : "16rem" }}
      className="h-screen bg-card flex flex-col relative z-20 shadow-sm"
    >
      <div className="p-4 flex items-center justify-between h-20">
        {!sidebarCollapsed && <span className="font-bold text-xl text-foreground whitespace-nowrap px-2">Ishan Insights</span>}
        <button onClick={toggleSidebar} className="p-2 rounded-md hover:bg-muted ml-auto">
          {sidebarCollapsed ? <ChevronRight size={18} /> : <ChevronLeft size={18} />}
        </button>
      </div>

      <nav className="flex-1 overflow-y-auto py-4 flex flex-col gap-2 px-2">
        {navItems
          .filter(item => !user || item.roles.includes(user.role))
          .map((item) => {
            const isActive = location.pathname === item.path;
          return (
            <Link
              key={item.path}
              to={item.path}
              className={cn(
                "flex items-center gap-3 px-3 py-3 rounded-xl transition-all duration-200",
                isActive 
                  ? "bg-primary/10 text-primary font-semibold" 
                  : "text-muted-foreground hover:bg-muted hover:text-foreground font-medium"
              )}
            >
              <item.icon size={20} className="shrink-0" />
              {!sidebarCollapsed && <span className="font-medium whitespace-nowrap">{item.name}</span>}
            </Link>
          );
        })}
      </nav>

      <div className="p-4 border-t border-border">
        <div className="flex items-center gap-3 mb-4 px-2">
          <div className="w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center shrink-0">
            <span className="text-primary font-medium text-xs">
              {user?.name?.charAt(0) || "U"}
            </span>
          </div>
          {!sidebarCollapsed && (
            <div className="flex flex-col overflow-hidden">
              <span className="text-sm font-medium truncate">{user?.name}</span>
              <span className="text-xs text-muted-foreground truncate capitalize">{user?.role}</span>
            </div>
          )}
        </div>
        
        <button
          onClick={logout}
          className="flex items-center gap-3 px-3 py-2 text-sm text-destructive hover:bg-destructive/10 rounded-md transition-colors w-full"
        >
          <LogOut size={20} />
          {!sidebarCollapsed && <span className="font-medium">Sign out</span>}
        </button>
      </div>
    </motion.aside>
  );
}
