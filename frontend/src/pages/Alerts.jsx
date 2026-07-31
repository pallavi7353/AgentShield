import { useEffect, useState } from "react";
import { BellRing } from "lucide-react";
import api from "../lib/api";
import { Spinner, EmptyState, SeverityBadge } from "../components/ui";

const STATUS_OPTIONS = ["open", "acknowledged", "resolved"];

const STATUS_STYLES = {
  open: "text-alert-critical bg-alert-critical/10 border-alert-critical/30",
  acknowledged: "text-alert-medium bg-alert-medium/10 border-alert-medium/30",
  resolved: "text-teal-glow bg-teal-glow/10 border-teal-glow/30",
};

export default function Alerts() {
  const [alerts, setAlerts] = useState(null);
  const [error, setError] = useState("");
  const [updatingId, setUpdatingId] = useState(null);

  useEffect(() => {
    load();
  }, []);

  function load() {
    api
      .get("/alerts")
      .then((r) => setAlerts(r.data))
      .catch(() => setError("Could not load alerts."));
  }

  async function updateStatus(id, status) {
    setUpdatingId(id);
    try {
      const { data } = await api.put(`/alerts/${id}`, { status });
      setAlerts((prev) => prev.map((a) => (a.id === id ? data : a)));
    } catch {
      setError("Could not update alert status.");
    } finally {
      setUpdatingId(null);
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="font-display text-2xl font-semibold flex items-center gap-2">
          <BellRing size={20} className="text-teal-glow" />
          Alerts
        </h1>
        <p className="text-sm text-slate-500 mt-1">
          Security-team-facing alerts raised by the threat and AI detection engines.
        </p>
      </div>

      {error && <p className="text-alert-critical text-sm">{error}</p>}
      {!alerts && !error && <Spinner />}
      {alerts && alerts.length === 0 && (
        <EmptyState title="No alerts" sub="Nothing has triggered the security team yet." />
      )}

      {alerts && alerts.length > 0 && (
        <div className="space-y-3">
          {alerts.map((a) => (
            <div key={a.id} className="card p-4 flex items-start justify-between gap-4">
              <div className="min-w-0 flex-1">
                <div className="flex items-center gap-2 mb-1.5">
                  <SeverityBadge severity={a.severity} />
                  <span className="text-[11px] text-slate-500">
                    {new Date(a.timestamp).toLocaleString()}
                  </span>
                </div>
                <p className="text-sm font-medium text-slate-200">{a.title}</p>
                {a.description && <p className="text-xs text-slate-500 mt-1 leading-relaxed">{a.description}</p>}
              </div>

              <select
                value={a.status}
                disabled={updatingId === a.id}
                onChange={(e) => updateStatus(a.id, e.target.value)}
                className={`shrink-0 text-xs font-medium rounded-md border px-2.5 py-1.5 bg-transparent capitalize cursor-pointer ${STATUS_STYLES[a.status]}`}
              >
                {STATUS_OPTIONS.map((s) => (
                  <option key={s} value={s} className="bg-ink-900 text-slate-100">
                    {s}
                  </option>
                ))}
              </select>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
