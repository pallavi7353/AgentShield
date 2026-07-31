import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { ShieldAlert, Activity, Ban, ScanSearch, ArrowUpRight } from "lucide-react";
import api from "../lib/api";
import { useAuth } from "../context/AuthContext";
import { hasPermission } from "../lib/jwt";
import { StatCard, SeverityBadge, Spinner, EmptyState } from "../components/ui";

export default function Dashboard() {
  const { user } = useAuth();
  const [threats, setThreats] = useState(null);
  const [alerts, setAlerts] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;
    async function load() {
      const requests = [];
      requests.push(
        hasPermission(user?.role, "READ_LOGS")
          ? api.get("/threat-history").then((r) => r.data)
          : Promise.resolve([])
      );
      requests.push(
        hasPermission(user?.role, "VIEW_DASHBOARD")
          ? api.get("/alerts").then((r) => r.data)
          : Promise.resolve([])
      );
      const [t, a] = await Promise.all(requests);
      if (!cancelled) {
        setThreats(t);
        setAlerts(a);
        setLoading(false);
      }
    }
    load();
    return () => {
      cancelled = true;
    };
  }, [user]);

  if (loading) return <Spinner />;

  const totalScanned = threats?.length || 0;
  const blockedCount = threats?.filter((t) => t.blocked).length || 0;
  const openAlerts = alerts?.filter((a) => a.status === "open").length || 0;
  const avgRisk = totalScanned
    ? Math.round(threats.reduce((sum, t) => sum + t.risk_score, 0) / totalScanned)
    : 0;

  return (
    <div className="space-y-6">
      <div className="flex items-end justify-between">
        <div>
          <h1 className="font-display text-2xl font-semibold">Security Overview</h1>
          <p className="text-sm text-slate-500 mt-1">
            Welcome back, <span className="text-slate-300">{user?.username}</span> ·{" "}
            <span className="text-teal-glow">{user?.role}</span>
          </p>
        </div>
        {hasPermission(user?.role, "EXECUTE_AI_AGENT") && (
          <Link to="/analyze" className="btn-primary">
            <ScanSearch size={16} />
            Run analysis
          </Link>
        )}
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard label="Prompts Scanned" value={totalScanned} icon={Activity} tint="bg-teal-glow" />
        <StatCard label="Blocked" value={blockedCount} icon={Ban} tint="bg-alert-critical" />
        <StatCard label="Open Alerts" value={openAlerts} icon={ShieldAlert} tint="bg-alert-medium" />
        <StatCard label="Avg. Risk Score" value={avgRisk} icon={Activity} tint="bg-alert-high" sub="0–100 scale" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card p-5">
          <div className="flex items-center justify-between mb-4">
            <h2 className="font-display font-semibold text-sm">Recent Threat Scans</h2>
            {hasPermission(user?.role, "READ_LOGS") && (
              <Link to="/threats" className="text-xs text-teal-glow flex items-center gap-1 hover:underline">
                View all <ArrowUpRight size={12} />
              </Link>
            )}
          </div>
          {!threats?.length ? (
            <EmptyState title="No scans yet" sub="Run a prompt through AI Analyze to populate this feed." />
          ) : (
            <div className="space-y-2">
              {threats.slice(0, 5).map((t) => (
                <div key={t.id} className="flex items-center justify-between py-2 border-b border-ink-700/60 last:border-0">
                  <div className="min-w-0 flex-1 pr-4">
                    <p className="text-sm text-slate-300 truncate font-mono">{t.prompt}</p>
                    <p className="text-[11px] text-slate-500 mt-0.5">
                      {new Date(t.timestamp).toLocaleString()}
                    </p>
                  </div>
                  <span className="text-xs font-mono font-semibold text-slate-400 shrink-0">
                    {t.risk_score}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="card p-5">
          <div className="flex items-center justify-between mb-4">
            <h2 className="font-display font-semibold text-sm">Latest Alerts</h2>
            <Link to="/alerts" className="text-xs text-teal-glow flex items-center gap-1 hover:underline">
              View all <ArrowUpRight size={12} />
            </Link>
          </div>
          {!alerts?.length ? (
            <EmptyState title="No alerts" sub="Nothing has triggered the security team yet." />
          ) : (
            <div className="space-y-2">
              {alerts.slice(0, 5).map((a) => (
                <div key={a.id} className="flex items-center justify-between py-2 border-b border-ink-700/60 last:border-0">
                  <div className="min-w-0 flex-1 pr-4">
                    <p className="text-sm text-slate-300 truncate">{a.title}</p>
                    <p className="text-[11px] text-slate-500 mt-0.5">
                      {new Date(a.timestamp).toLocaleString()}
                    </p>
                  </div>
                  <SeverityBadge severity={a.severity} />
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
