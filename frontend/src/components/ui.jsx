export function StatCard({ label, value, icon: Icon, tint = "bg-teal-glow", sub }) {
  return (
    <div className="card p-5 relative overflow-hidden">
      <div className={`absolute -top-8 -right-8 w-24 h-24 rounded-full opacity-20 blur-2xl ${tint}`} />
      <div className="flex items-center justify-between mb-3">
        <p className="text-xs uppercase tracking-wide text-slate-500 font-medium">{label}</p>
        {Icon && <Icon size={16} className="text-slate-500" />}
      </div>
      <p className="font-display text-3xl font-semibold">{value}</p>
      {sub && <p className="text-xs text-slate-500 mt-1">{sub}</p>}
    </div>
  );
}

const SEVERITY_STYLES = {
  low: "text-alert-low bg-alert-low/10 border-alert-low/30",
  medium: "text-alert-medium bg-alert-medium/10 border-alert-medium/30",
  high: "text-alert-high bg-alert-high/10 border-alert-high/30",
  critical: "text-alert-critical bg-alert-critical/10 border-alert-critical/30",
  none: "text-slate-400 bg-slate-500/10 border-slate-500/30",
};

export function SeverityBadge({ severity }) {
  const key = (severity || "none").toLowerCase();
  const style = SEVERITY_STYLES[key] || SEVERITY_STYLES.none;
  return (
    <span className={`inline-flex items-center px-2 py-0.5 rounded-md border text-[11px] font-mono font-medium uppercase tracking-wide ${style}`}>
      {severity || "none"}
    </span>
  );
}

export function DecisionBadge({ decision }) {
  const isBlock = decision === "BLOCK";
  return (
    <span
      className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md border text-xs font-mono font-semibold uppercase tracking-wide ${
        isBlock
          ? "text-alert-critical bg-alert-critical/10 border-alert-critical/30"
          : "text-teal-glow bg-teal-glow/10 border-teal-glow/30"
      }`}
    >
      <span className={`w-1.5 h-1.5 rounded-full ${isBlock ? "bg-alert-critical" : "bg-teal-glow"}`} />
      {decision}
    </span>
  );
}

function riskColor(score) {
  if (score >= 85) return "#FF3B5C";
  if (score >= 60) return "#FF6B4A";
  if (score >= 30) return "#F5A623";
  return "#2DD4BF";
}

export function RiskGauge({ score = 0, size = 140 }) {
  const radius = (size - 16) / 2;
  const circumference = 2 * Math.PI * radius;
  const clamped = Math.max(0, Math.min(100, score));
  const offset = circumference - (clamped / 100) * circumference;
  const color = riskColor(clamped);

  return (
    <div className="relative" style={{ width: size, height: size }}>
      <svg width={size} height={size} className="-rotate-90">
        <circle cx={size / 2} cy={size / 2} r={radius} stroke="#1A2340" strokeWidth={10} fill="none" />
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke={color}
          strokeWidth={10}
          fill="none"
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          style={{ transition: "stroke-dashoffset 0.6s ease, stroke 0.6s ease" }}
        />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span className="font-display font-bold text-3xl" style={{ color }}>
          {clamped}
        </span>
        <span className="text-[10px] uppercase tracking-widest text-slate-500">risk score</span>
      </div>
    </div>
  );
}

export function EmptyState({ title, sub }) {
  return (
    <div className="card p-10 text-center">
      <p className="font-display text-lg font-semibold text-slate-300">{title}</p>
      {sub && <p className="text-sm text-slate-500 mt-1">{sub}</p>}
    </div>
  );
}

export function Spinner() {
  return (
    <div className="flex items-center justify-center py-16">
      <div className="w-6 h-6 border-2 border-teal-glow/30 border-t-teal-glow rounded-full animate-spin" />
    </div>
  );
}
