import { useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { ShieldHalf, Lock, User, AlertCircle } from "lucide-react";
import { useAuth } from "../context/AuthContext";

const DEMO_ACCOUNTS = [
  { role: "Admin", username: "admin", password: "Admin@12345" },
  { role: "Security Analyst", username: "analyst", password: "Analyst@12345" },
  { role: "Employee", username: "employee", password: "Employee@12345" },
  { role: "AI Agent", username: "agent_service", password: "Agent@12345" },
];

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await login(username, password);
      navigate(location.state?.from || "/", { replace: true });
    } catch (err) {
      setError(err.response?.data?.detail || "Invalid username or password.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center px-4">
      <div className="w-full max-w-md">
        <div className="flex flex-col items-center mb-8">
          <div className="w-14 h-14 rounded-2xl bg-teal-glow/10 border border-teal-glow/40 flex items-center justify-center mb-4 shadow-glow">
            <ShieldHalf size={26} className="text-teal-glow" />
          </div>
          <h1 className="font-display text-2xl font-semibold">AI Agent Security Platform</h1>
          <p className="text-sm text-slate-500 mt-1">CYBR-03 &middot; Sign in to the security console</p>
        </div>

        <form onSubmit={handleSubmit} className="card p-6 space-y-4">
          {error && (
            <div className="flex items-center gap-2 text-sm text-alert-critical bg-alert-critical/10 border border-alert-critical/30 rounded-lg px-3 py-2.5">
              <AlertCircle size={15} />
              {error}
            </div>
          )}

          <div>
            <label className="text-xs font-medium text-slate-400 mb-1.5 block">Username</label>
            <div className="relative">
              <User size={15} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" />
              <input
                className="input-field pl-9"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="admin"
                autoFocus
                required
              />
            </div>
          </div>

          <div>
            <label className="text-xs font-medium text-slate-400 mb-1.5 block">Password</label>
            <div className="relative">
              <Lock size={15} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" />
              <input
                type="password"
                className="input-field pl-9"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                required
              />
            </div>
          </div>

          <button type="submit" disabled={loading} className="btn-primary w-full">
            {loading ? "Signing in…" : "Sign in"}
          </button>
        </form>

        <div className="card p-4 mt-4">
          <p className="text-[11px] uppercase tracking-wide text-slate-500 font-medium mb-2.5">
            Demo accounts (from seed.py)
          </p>
          <div className="grid grid-cols-2 gap-2">
            {DEMO_ACCOUNTS.map((acc) => (
              <button
                key={acc.username}
                type="button"
                onClick={() => {
                  setUsername(acc.username);
                  setPassword(acc.password);
                }}
                className="text-left px-2.5 py-2 rounded-lg border border-ink-600 hover:border-teal-glow/50 transition text-xs"
              >
                <p className="font-medium text-slate-200">{acc.role}</p>
                <p className="text-slate-500 font-mono">{acc.username}</p>
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
