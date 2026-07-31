import { useEffect, useState } from "react";
import { History } from "lucide-react";
import api from "../lib/api";
import { Spinner, EmptyState, DecisionBadge } from "../components/ui";

export default function ThreatHistory() {
  const [threats, setThreats] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    api
      .get("/threat-history")
      .then((r) => setThreats(r.data))
      .catch(() => setError("Could not load threat history."));
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="font-display text-2xl font-semibold flex items-center gap-2">
          <History size={20} className="text-teal-glow" />
          Threat History
        </h1>
        <p className="text-sm text-slate-500 mt-1">
          Every prompt/response run through the detection engine (rule-based + Gemma).
        </p>
      </div>

      {error && <p className="text-alert-critical text-sm">{error}</p>}
      {!threats && !error && <Spinner />}
      {threats && threats.length === 0 && (
        <EmptyState title="No threat records yet" sub="Analyzed prompts will show up here." />
      )}

      {threats && threats.length > 0 && (
        <div className="card overflow-hidden">
          <table className="w-full text-sm">
            <thead>
              <tr className="text-left text-xs uppercase tracking-wide text-slate-500 border-b border-ink-700/70">
                <th className="px-5 py-3 font-medium">Prompt / Text</th>
                <th className="px-5 py-3 font-medium">Attack Type</th>
                <th className="px-5 py-3 font-medium">Risk</th>
                <th className="px-5 py-3 font-medium">Decision</th>
                <th className="px-5 py-3 font-medium">Timestamp</th>
              </tr>
            </thead>
            <tbody>
              {threats.map((t) => (
                <tr key={t.id} className="border-b border-ink-700/40 last:border-0 hover:bg-ink-700/20">
                  <td className="px-5 py-3 font-mono text-xs text-slate-300 max-w-md truncate">{t.prompt}</td>
                  <td className="px-5 py-3 text-slate-400">{t.attack_type || "NONE"}</td>
                  <td className="px-5 py-3 font-mono font-semibold">{t.risk_score}</td>
                  <td className="px-5 py-3">
                    <DecisionBadge decision={t.blocked ? "BLOCK" : "ALLOW"} />
                  </td>
                  <td className="px-5 py-3 text-slate-500 text-xs">
                    {new Date(t.timestamp).toLocaleString()}
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
