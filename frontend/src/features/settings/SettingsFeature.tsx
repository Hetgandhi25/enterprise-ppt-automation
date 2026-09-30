import { useState } from "react";
import { PageHeader } from "../../components/shared/Headers";
import { GeneralSettings } from "./components/GeneralSettings";
import { AppearanceSettings } from "./components/AppearanceSettings";
import { AutomationSettings } from "./components/AutomationSettings";
import { OutputSettings } from "./components/OutputSettings";
import { NotificationSettings } from "./components/NotificationSettings";
import { FeatureFlagsPanel } from "./components/FeatureFlagsPanel";
import { AdvancedSettings } from "./components/AdvancedSettings";
import { About } from "./components/About";
import { ChevronDown, ShieldAlert } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

export function SettingsFeature() {
  const [advancedOpen, setAdvancedOpen] = useState(false);

  return (
    <div className="max-w-4xl mx-auto space-y-8 pb-12">
      <PageHeader 
        title="Settings" 
        description="Manage your application preferences and workspace configuration." 
      />

      <div className="space-y-8">
        
        {/* Core Settings Rendered Flat */}
        <section className="bg-card border border-border rounded-xl p-6 shadow-sm">
          <AppearanceSettings />
        </section>

        <section className="bg-card border border-border rounded-xl p-6 shadow-sm">
          <AutomationSettings />
        </section>

        <section className="bg-card border border-border rounded-xl p-6 shadow-sm">
          <OutputSettings />
        </section>

        <section className="bg-card border border-border rounded-xl p-6 shadow-sm">
          <GeneralSettings />
        </section>

        {/* Collapsible Advanced Settings */}
        <div className="pt-8">
          <button 
            onClick={() => setAdvancedOpen(!advancedOpen)}
            className="w-full flex items-center justify-between p-4 bg-muted/30 border border-border rounded-lg hover:bg-muted transition-colors group"
          >
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded-full bg-destructive/10 text-destructive flex items-center justify-center">
                <ShieldAlert size={16} />
              </div>
              <div className="text-left">
                <h3 className="text-sm font-medium text-foreground">Advanced Settings</h3>
                <p className="text-xs text-muted-foreground mt-0.5">Feature flags, data management, and dangerous actions.</p>
              </div>
            </div>
            <ChevronDown size={20} className={`text-muted-foreground transition-transform ${advancedOpen ? 'rotate-180' : ''}`} />
          </button>

          <AnimatePresence>
            {advancedOpen && (
              <motion.div 
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: "auto" }}
                exit={{ opacity: 0, height: 0 }}
                className="overflow-hidden"
              >
                <div className="pt-6 space-y-6">
                  <section className="bg-card border border-border rounded-xl p-6 shadow-sm">
                    <FeatureFlagsPanel />
                  </section>
                  <section className="bg-card border border-border rounded-xl p-6 shadow-sm">
                    <NotificationSettings />
                  </section>
                  <section className="bg-card border border-border rounded-xl p-6 shadow-sm">
                    <AdvancedSettings />
                  </section>
                  <section className="bg-card border border-border rounded-xl p-6 shadow-sm">
                    <About />
                  </section>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>

      </div>
    </div>
  );
}
