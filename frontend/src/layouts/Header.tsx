import { Search, Bell, User, CheckCircle2, XCircle, Clock, AlertCircle } from "lucide-react";
import { useLocation, Link } from "react-router-dom";
import { useSettingsStore } from "../stores/useSettingsStore";
import { Moon, Sun } from "lucide-react";
import { useState, useRef, useEffect } from "react";
import { useNotifications, NotificationItem } from "../features/dashboard/hooks/useNotifications";
import { useNotificationStore } from "../stores/useNotificationStore";
import { cn } from "../utils/cn";

export function Header() {
  const location = useLocation();
  const { theme, setTheme } = useSettingsStore();
  const [showNotifications, setShowNotifications] = useState(false);
  const notifRef = useRef<HTMLDivElement>(null);
  const { data: notifications } = useNotifications();
  const { readIds, markAsRead, markAllAsRead } = useNotificationStore();

  const unreadCount = notifications?.filter(n => !readIds.includes(n.id)).length || 0;

  useEffect(() => {
    const handleOutsideClick = (e: MouseEvent) => {
      if (notifRef.current && !notifRef.current.contains(e.target as Node)) {
        setShowNotifications(false);
      }
    };
    document.addEventListener("mousedown", handleOutsideClick);
    return () => document.removeEventListener("mousedown", handleOutsideClick);
  }, []);

  const getPageTitle = () => {
    switch (location.pathname) {
      case "/": return "Dashboard";
      case "/generate": return "Generate Report";
      case "/jobs": return "Jobs & Activity";
      case "/reports": return "Generated Reports";
      case "/logs": return "System Logs";
      case "/settings": return "Settings";
      case "/help": return "Help & Documentation";
      default: return "";
    }
  };

  return (
    <header className="h-20 bg-background/50 backdrop-blur-md px-8 flex items-center justify-between sticky top-0 z-10">
      <h1 className="text-2xl font-bold text-foreground tracking-tight">{getPageTitle()}</h1>
      
      <div className="flex items-center gap-6">
        {/* Search Placeholder */}
        <div className="relative hidden md:block w-64">
          <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground" />
          <input 
            type="text" 
            placeholder="Search..." 
            className="w-full h-9 pl-9 pr-4 bg-muted border border-border rounded-full text-sm focus:outline-none focus:ring-2 focus:ring-primary/20 transition-all"
          />
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
            className="p-2 text-muted-foreground hover:text-foreground rounded-full hover:bg-muted transition-colors"
            title="Toggle Theme"
          >
            {theme === "dark" ? <Sun size={20} /> : <Moon size={20} />}
          </button>
          
          <div className="relative" ref={notifRef}>
            <button 
              onClick={() => setShowNotifications(!showNotifications)}
              className={cn("p-2 text-muted-foreground hover:text-foreground rounded-full hover:bg-muted transition-colors relative", showNotifications && "bg-muted text-foreground")} 
              title="Notifications"
            >
              <Bell size={20} />
              {unreadCount > 0 && (
                <span className="absolute top-2 right-2 w-2 h-2 bg-destructive rounded-full border-2 border-card" />
              )}
            </button>
            
            {showNotifications && (
              <div className="absolute right-0 mt-2 w-80 bg-card border border-border rounded-xl shadow-lg z-50 overflow-hidden flex flex-col max-h-[28rem]">
                <div className="p-4 border-b border-border flex items-center justify-between bg-muted/30">
                  <h3 className="font-semibold text-foreground">Notifications</h3>
                  <div className="flex items-center gap-2">
                    {unreadCount > 0 && (
                      <button 
                        onClick={() => {
                          if (notifications) markAllAsRead(notifications.map(n => n.id));
                        }}
                        className="text-[10px] text-muted-foreground hover:text-primary transition-colors uppercase font-medium"
                      >
                        Mark all read
                      </button>
                    )}
                    {unreadCount > 0 && (
                      <span className="text-xs text-muted-foreground bg-background px-2 py-0.5 rounded-full border border-border">
                        {unreadCount} New
                      </span>
                    )}
                  </div>
                </div>
                
                <div className="overflow-y-auto flex-1">
                  {!notifications || notifications.length === 0 ? (
                    <div className="p-6 text-center text-muted-foreground text-sm flex flex-col items-center gap-2">
                      <Bell size={24} className="text-muted-foreground/50" />
                      No recent notifications
                    </div>
                  ) : (
                    <div className="divide-y divide-border">
                      {notifications.map((notif: NotificationItem) => {
                        const isRead = readIds.includes(notif.id);
                        return (
                        <div 
                          key={notif.id} 
                          onClick={() => markAsRead(notif.id)}
                          className={cn(
                            "p-4 transition-colors flex gap-3 cursor-pointer", 
                            isRead ? "opacity-60 bg-transparent hover:bg-muted/50" : "bg-primary/5 hover:bg-primary/10"
                          )}
                        >
                          <div className="shrink-0 mt-0.5">
                            {notif.icon && <notif.icon size={16} className={cn(
                              notif.type === "job_success" ? "text-emerald-500" :
                              notif.type === "job_failed" ? "text-destructive" :
                              notif.type === "alert" ? "text-amber-500" :
                              "text-primary"
                            )} />}
                          </div>
                          <div className="flex-1 min-w-0">
                            <p className="text-sm font-medium text-foreground truncate">
                              {notif.title}
                            </p>
                            <p className="text-xs text-muted-foreground mt-0.5 leading-snug">
                              {notif.message}
                            </p>
                            <p className="text-[10px] text-muted-foreground/70 mt-1 uppercase font-medium">
                              {notif.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                            </p>
                          </div>
                          {notif.link && (
                            <a 
                              href={notif.link} 
                              target="_blank" 
                              rel="noreferrer" 
                              onClick={(e) => { e.stopPropagation(); markAsRead(notif.id); }}
                              className="text-xs text-primary hover:underline whitespace-nowrap self-center font-medium"
                            >
                              View
                            </a>
                          )}
                        </div>
                      )})}
                    </div>
                  )}
                </div>
                
                <div className="p-2 border-t border-border bg-muted/10 text-center">
                  <Link to="/jobs" onClick={() => setShowNotifications(false)} className="text-xs text-primary font-medium hover:underline p-2 block w-full">
                    View all activity
                  </Link>
                </div>
              </div>
            )}
          </div>
          
          <button className="w-9 h-9 rounded-full bg-primary/10 border border-primary/20 flex items-center justify-center text-primary font-medium hover:bg-primary/20 transition-colors" title="User Menu">
            <User size={18} />
          </button>
        </div>
      </div>
    </header>
  );
}
