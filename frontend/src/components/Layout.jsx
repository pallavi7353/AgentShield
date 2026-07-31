import { NavLink, useNavigate } from "react-router-dom";
import {
  LayoutDashboard,
  ScanSearch,
  History,
  BellRing,
  ScrollText,
  Users,
  LogOut,
  ShieldHalf,
} from "lucide-react";
import { useAuth } from "../context/AuthContext";
import { hasPermission } from "../lib/jwt";

const NAV_ITEMS = [
  { to: "/", label: "Dashboard", icon: LayoutDashboard, permission: "VIEW_DASHBOARD" },
  { to: "/analyze", label: "AI Analyze", icon: ScanSearch, permission: "EXECUTE_AI_AGENT" },
  { to: "/threats", label: "Threat History", icon: History, permission: "READ_LOGS" },
  { to: "/alerts", label: "Alerts", icon: BellRing, permission: "VIEW_DASHBOARD" },
  { to: "/audit", label: "Audit Logs", icon: ScrollText, permission: "READ_LOGS" },
  { to: "/users", label: "Users & Roles", icon: Users, permission: "MANAGE_USERS" },
];

export default function Layout({ children }) {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  async function handleLogout() {
    await logout();
    navigate("/login");
  }

  return (
    <div className="min-h-screen flex">
      <aside className="w-64 shrink-0 border-r border-ink-700/70 bg-ink-950/60 flex flex-col">
        <div className="px-5 py-6 flex items-center gap-2.5 border-b border-ink-700/70">
          <div className="w-9 h-9 rounded-lg bg-teal-glow/10 border border-teal-glow/40 flex items-center justify-center">
            <ShieldHalf size={18} className="text-teal-glow" />
          </div>
          <div>
            <p className="font-display font-semibold text-sm leading-tight">CYBR-03</p>
            <p className="text-[11px] text-slate-500 leading-tight">Agent Security Platform</p>
          </div>
        </div>

        <nav className="flex-1 px-3 py-4 space-y-1">
          {NAV_ITEMS.filter((item) => hasPermission(user?.role, item.permission)).map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.to === "/"}
              className={({ isActive }) => `nav-link ${isActive ? "active" : ""}`}
            >
              <item.icon size={17} />
              {item.label}
            </NavLink>
          ))}
        </nav>

        <div className="px-3 py-4 border-t border-ink-700/70">
          <div className="px-3 py-2.5 mb-2 rounded-lg bg-ink-800/70">
            <p className="text-sm font-medium truncate">{user?.username}</p>
            <p className="text-[11px] text-teal-glow">{user?.role}</p>
          </div>
          <button onClick={handleLogout} className="nav-link w-full text-alert-high">
            <LogOut size={17} />
            Sign out
          </button>
        </div>
      </aside>

      <main className="flex-1 min-w-0">
        <div className="max-w-6xl mx-auto px-8 py-8">{children}</div>
      </main>
    </div>
  );
}
