import { motion } from "framer-motion";
import { Link } from "react-router-dom";
import { FilePlus, FileText, Activity, AlertCircle, HardDrive, Cpu, CheckCircle2, XCircle, Clock } from "lucide-react";
import { useDashboard } from "./hooks/useDashboard";
import { useRecentJobs } from "./hooks/useRecentJobs";
import { useRecentReports } from "./hooks/useRecentReports";
import { PageHeader, SectionHeader } from "../../components/shared/Headers";
import { StatCard } from "../../components/shared/StatCard";
import { Skeleton } from "../../components/shared/Skeleton";
import { EmptyState } from "../../components/shared/EmptyState";
import { StatusBadge } from "../../components/shared/StatusBadge";
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, PieChart, Pie, Cell } from "recharts";
import { useSettingsStore } from "../../stores/useSettingsStore";

const COLORS = ["hsl(var(--primary))", "hsl(var(--chart-2, 160 60% 45%))", "hsl(var(--chart-3, 30 80% 55%))", "hsl(var(--chart-4, 280 65% 60%))"];

export function DashboardFeature() {
  const { data, isLoading, isError, error } = useDashboard();
  const { data: recentJobs } = useRecentJobs(5);
  const { data: recentReports } = useRecentReports(5);
  const { appMode } = useSettingsStore();

  if (isLoading) {
    return (
      <div className="space-y-6">
        <Skeleton className="w-64 h-12" />
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {[...Array(4)].map((_, i) => <Skeleton key={i} className="h-32 rounded-xl" />)}
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <Skeleton className="h-80 rounded-xl" />
          <Skeleton className="h-80 rounded-xl" />
        </div>
      </div>
    );
  }

  if (isError || !data) {
    return (
      <div className="p-12 text-center text-destructive">
        <AlertCircle className="mx-auto mb-4" size={32} />
        <p>Failed to load dashboard data.</p>
        <p className="text-sm opacity-80">{error?.message}</p>
      </div>
    );
  }

  const { stats, charts, health } = data;

  return (
    <div className="space-y-8 pb-8">
      {/* Top Section */}
      <PageHeader
        title="Welcome back!"
        description={`You are running in ${appMode.toUpperCase()} mode.`}
        action={
          <Link
            to="/generate"
            className="flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground rounded-md font-medium hover:bg-primary/90 transition-colors shadow-sm"
          >
            <FilePlus size={18} />
            Quick Generate
          </Link>
        }
      />

      {/* Statistics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="Total Reports"
          value={stats.totalReports.toLocaleString()}
          icon={<FileText size={20} />}
          trend={{ value: "+12% this month", isPositive: true }}
        />
        <StatCard
          title="Today's Reports"
          value={stats.todaysReports}
          icon={<Activity size={20} />}
        />
        <StatCard
          title="Success Rate"
          value={`${stats.successRate}%`}
          icon={<CheckCircle2 size={20} />}
          trend={{ value: stats.successRate >= 95 ? "Healthy" : "Needs Attention", isPositive: stats.successRate >= 95 }}
        />
        <StatCard
          title="Average Runtime"
          value={`${stats.avgRuntimeMs}ms`}
          icon={<Clock size={20} />}
        />
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <motion.div whileHover={{ y: -2 }} className="bg-card rounded-2xl p-6 shadow-sm">
          <SectionHeader title="Reports Generated Trend" description="Last 7 days of activity" />
          <div className="h-64 mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={charts.reportsTrend}>
                <defs>
                  <linearGradient id="colorReports" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="hsl(var(--primary))" stopOpacity={0.3} />
                    <stop offset="95%" stopColor="hsl(var(--primary))" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="hsl(var(--border))" />
                <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{ fill: 'hsl(var(--muted-foreground))', fontSize: 12 }} dy={10} />
                <YAxis axisLine={false} tickLine={false} tick={{ fill: 'hsl(var(--muted-foreground))', fontSize: 12 }} />
                <Tooltip 
                  contentStyle={{ backgroundColor: 'hsl(var(--card))', borderColor: 'hsl(var(--border))', borderRadius: '8px' }}
                  itemStyle={{ color: 'hsl(var(--foreground))' }}
                />
                <Area type="monotone" dataKey="value" stroke="hsl(var(--primary))" strokeWidth={2} fillOpacity={1} fill="url(#colorReports)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </motion.div>

        <motion.div whileHover={{ y: -2 }} className="bg-card rounded-2xl p-6 shadow-sm">
          <SectionHeader title="Customer Distribution" description="Reports by customer" />
          <div className="h-64 mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={charts.customerDistribution}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={80}
                  paddingAngle={5}
                  dataKey="value"
                >
                  {charts.customerDistribution.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip 
                  contentStyle={{ backgroundColor: 'hsl(var(--card))', borderColor: 'hsl(var(--border))', borderRadius: '8px' }}
                  itemStyle={{ color: 'hsl(var(--foreground))' }}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </motion.div>
      </div>

      {/* Bottom Section: Activity & Health */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Recent Jobs */}
        <div className="bg-card rounded-2xl p-6 shadow-sm lg:col-span-3">
          <div className="flex items-center justify-between mb-4">
            <SectionHeader title="Recent Activity" />
          </div>
          <div className="space-y-4">
            {!recentJobs ? (
              <Skeleton className="h-24 w-full" />
            ) : recentJobs.length === 0 ? (
              <div className="text-center py-8 bg-muted/20 border border-dashed border-border rounded-lg text-muted-foreground">
                No recent activity. Start by generating a report!
              </div>
            ) : (
              recentJobs.map(job => (
                <div key={job.id} className="flex items-center justify-between p-3 hover:bg-muted/50 rounded-lg transition-colors border border-transparent hover:border-border">
                  <div>
                    <p className="font-medium text-foreground">{job.customerName}</p>
                    <p className="text-xs text-muted-foreground">ID: {job.id.split('-').pop()} • {new Date(job.startTime).toLocaleString()}</p>
                  </div>
                  <div className="flex items-center gap-4">
                    <span className="text-sm font-medium text-muted-foreground">{job.runtimeMs ? `${job.runtimeMs.toFixed(0)}ms` : '-'}</span>
                    <StatusBadge status={job.status} />
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
