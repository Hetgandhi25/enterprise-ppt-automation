import { cn } from "../../../utils/cn";
import { Settings, Layout, Zap, Folder, Bell, Flag, Sliders, Info } from "lucide-react";

export type SettingsTab = "general" | "appearance" | "automation" | "output" | "notifications" | "features" | "advanced" | "about";

interface Props {
  activeTab: SettingsTab;
  setActiveTab: (tab: SettingsTab) => void;
}

export function SettingsNavigation({ activeTab, setActiveTab }: Props) {
  const tabs = [
    { id: "general", label: "General", icon: <Settings size={16} /> },
    { id: "appearance", label: "Appearance", icon: <Layout size={16} /> },
    { id: "automation", label: "Automation", icon: <Zap size={16} /> },
    { id: "output", label: "Output", icon: <Folder size={16} /> },
    { id: "notifications", label: "Notifications", icon: <Bell size={16} /> },
    { id: "features", label: "Feature Flags", icon: <Flag size={16} /> },
    { id: "advanced", label: "Advanced", icon: <Sliders size={16} /> },
    { id: "about", label: "About", icon: <Info size={16} /> },
  ];

  return (
    <nav className="w-full md:w-64 shrink-0 space-y-1">
      {tabs.map((tab) => (
        <button
          key={tab.id}
          onClick={() => setActiveTab(tab.id as SettingsTab)}
          className={cn(
            "w-full flex items-center gap-3 px-3 py-2 text-sm font-medium rounded-md transition-colors",
            activeTab === tab.id
              ? "bg-primary/10 text-primary"
              : "text-muted-foreground hover:bg-muted hover:text-foreground"
          )}
        >
          {tab.icon}
          {tab.label}
        </button>
      ))}
    </nav>
  );
}
