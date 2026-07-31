import { useEffect, useState } from "react";
import { ScrollText } from "lucide-react";
import api from "../lib/api";
import { Spinner, EmptyState } from "../components/ui";

const LEVEL_COLOR = {
  none: "text-slate-500",
  low: "text-alert-low",
  medium: "text-alert-medium",
  high: "text-alert-high",
  critical: "text-alert-critical",
};

export default function AuditLogs() {
  const [logs, setLogs] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    api
      .get("/auditlogs")
      .then((r) => setLogs(r.data))
      .catch(() => setError("Could not load audit logs."));
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="font-display text-2xl font-semibold flex items-center gap-2">
          <ScrollText size={20} className="text-teal-glow" />
          Audit Logs
        </h1>
        <p className="text-sm text-slate-500 mt-1">
          Immutable trail of logins, AI requests/responses, and admin actions.
        </p>
      </div>

      {error && <p className="text-alert-critical text-sm">{error}</p>}
      {!logs && !error && <Spinner />}
      {logs && logs.length === 0 && <EmptyState title="No audit entries yet" />}

      {logs && logs.length > 0 && (
        <div className="card overflow-hidden">
          <table className="w-full text-sm">
            <thead>
              <tr className="text-left text-xs uppercase tracking-wide text-slate-500 border-b border-ink-700/70">
                <th className="px-5 py-3 font-medium">Event</th>
                <th className="px-5 py-3 font-medium">User ID</th>
                <th className="px-5 py-3 font-medium">Action</th>
                <th className="px-5 py-3 font-medium">Threat Level</th>
                <th className="px-5 py-3 font-medium">Timestamp</th>
              </tr>
            </thead>
            <tbody>
              {logs.map((log) => (
                <tr key={log.id} className="border-b border-ink-700/40 last:border-0 hover:bg-ink-700/20">
                  <td className="px-5 py-3 font-mono text-xs text-slate-300">{log.event_type}</td>
                  <td className="px-5 py-3 text-slate-400">{log.user_id ?? "system"}</td>
                  <td className="px-5 py-3 text-slate-300">{log.action_taken || "—"}</td>
                  <td className={`px-5 py-3 font-medium capitalize ${LEVEL_COLOR[log.threat_level] || "text-slate-400"}`}>
                    {log.threat_level}
                  </td>
                  <td className="px-5 py-3 text-slate-500 text-xs">
                    {new Date(log.timestamp).toLocaleString()}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
