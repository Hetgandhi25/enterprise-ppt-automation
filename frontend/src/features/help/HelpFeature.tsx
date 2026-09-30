import { PageHeader } from "../../components/shared/Headers";
import { BookOpen, Server, Zap, Shield, HelpCircle, Code, Briefcase, ChevronRight } from "lucide-react";

export function HelpFeature() {
  return (
    <div className="max-w-4xl mx-auto space-y-8 pb-12">
      <PageHeader 
        title="Documentation & Help" 
        description="Learn how the PPT Automation engine works and explore its architecture." 
      />

      <div className="space-y-6">
        
        {/* Project Overview */}
        <section className="bg-card border border-border rounded-xl p-6 shadow-sm">
          <h2 className="text-lg font-semibold text-foreground flex items-center gap-2 mb-4">
            <BookOpen size={20} className="text-primary" />
            Project Overview
          </h2>
          <div className="prose prose-sm dark:prose-invert max-w-none text-muted-foreground">
            <p>
              This dashboard is the frontend interface for an automated enterprise PowerPoint generation engine. 
              It is designed to eliminate the manual, repetitive task of logging into a CRM, downloading monthly 
              inventory and incident SLA reports, manipulating the Excel data, plotting charts, and copy-pasting 
              them into a corporate presentation template.
            </p>
            <p className="mt-2">
              With a single click, the backend engine automatically performs all these tasks, generating a 
              publication-ready presentation in seconds.
            </p>
          </div>
        </section>

        {/* Architecture */}
        <section className="bg-card border border-border rounded-xl p-6 shadow-sm">
          <h2 className="text-lg font-semibold text-foreground flex items-center gap-2 mb-4">
            <Server size={20} className="text-blue-500" />
            Architecture
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="p-4 bg-muted/50 rounded-lg border border-border">
              <h3 className="font-medium text-foreground mb-2 flex items-center gap-2"><Code size={16}/> Frontend (React)</h3>
              <ul className="space-y-1 text-sm text-muted-foreground">
                <li className="flex items-start gap-2"><ChevronRight size={14} className="mt-0.5 shrink-0"/> React 19 + TypeScript + Vite</li>
                <li className="flex items-start gap-2"><ChevronRight size={14} className="mt-0.5 shrink-0"/> Tailwind CSS 4 + shadcn/ui</li>
                <li className="flex items-start gap-2"><ChevronRight size={14} className="mt-0.5 shrink-0"/> Zustand (Client State) + React Query (Server State)</li>
                <li className="flex items-start gap-2"><ChevronRight size={14} className="mt-0.5 shrink-0"/> Framer Motion (Animations)</li>
              </ul>
            </div>
            <div className="p-4 bg-muted/50 rounded-lg border border-border">
              <h3 className="font-medium text-foreground mb-2 flex items-center gap-2"><Briefcase size={16}/> Backend (FastAPI Python)</h3>
              <ul className="space-y-1 text-sm text-muted-foreground">
                <li className="flex items-start gap-2"><ChevronRight size={14} className="mt-0.5 shrink-0"/> Playwright (Browser Automation)</li>
                <li className="flex items-start gap-2"><ChevronRight size={14} className="mt-0.5 shrink-0"/> Pandas (Data Processing)</li>
                <li className="flex items-start gap-2"><ChevronRight size={14} className="mt-0.5 shrink-0"/> Matplotlib / Seaborn (Chart Generation)</li>
                <li className="flex items-start gap-2"><ChevronRight size={14} className="mt-0.5 shrink-0"/> python-pptx (Presentation Building)</li>
              </ul>
            </div>
          </div>
        </section>

        {/* Workflow */}
        <section className="bg-card border border-border rounded-xl p-6 shadow-sm">
          <h2 className="text-lg font-semibold text-foreground flex items-center gap-2 mb-4">
            <Zap size={20} className="text-amber-500" />
            Execution Workflow
          </h2>
          <div className="space-y-4">
            {[
              { title: "Initialization", desc: "The job is queued and context is prepared." },
              { title: "Data Extraction", desc: "Playwright logs into the CRM and downloads the required Excel files." },
              { title: "Processing", desc: "Pandas cleans, aggregates, and validates the raw Excel sheets." },
              { title: "Analytics", desc: "Statistical charts are generated and exported as PNGs." },
              { title: "Compilation", desc: "Dataframes and Charts are injected into the Master PPT Template." },
              { title: "Cleanup", desc: "Temporary Excel files and intermediate charts are deleted." },
            ].map((step, i) => (
              <div key={i} className="flex gap-4">
                <div className="flex flex-col items-center">
                  <div className="w-6 h-6 rounded-full bg-primary/10 text-primary flex items-center justify-center text-xs font-bold border border-primary/20 shrink-0">
                    {i + 1}
                  </div>
                  {i < 5 && <div className="w-px h-full bg-border mt-2 mb-2" />}
                </div>
                <div className="pb-4">
                  <h4 className="text-sm font-medium text-foreground">{step.title}</h4>
                  <p className="text-sm text-muted-foreground">{step.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* FAQ */}
        <section className="bg-card border border-border rounded-xl p-6 shadow-sm">
          <h2 className="text-lg font-semibold text-foreground flex items-center gap-2 mb-4">
            <HelpCircle size={20} className="text-emerald-500" />
            Frequently Asked Questions
          </h2>
          <div className="space-y-4 text-sm">
            <div className="space-y-1">
              <h4 className="font-medium text-foreground">Where does this run?</h4>
              <p className="text-muted-foreground">In a production environment, the frontend is hosted statically (e.g., Vercel) while the backend API runs on a containerized instance (e.g., AWS ECS or Render) due to the Playwright system dependencies.</p>
            </div>
            <div className="space-y-1">
              <h4 className="font-medium text-foreground">Why mock services?</h4>
              <p className="text-muted-foreground">The application implements an Interface-driven Service Factory pattern. By switching `AppMode` in the settings, the UI instantly swaps out the Mock Services for the FastAPI Services without changing any React components.</p>
            </div>
          </div>
        </section>

      </div>
    </div>
  );
}
