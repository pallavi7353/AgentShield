export function decodeJwt(token) {
  if (!token) return null;
  try {
    const payload = token.split(".")[1];
    const normalized = payload.replace(/-/g, "+").replace(/_/g, "/");
    const decoded = decodeURIComponent(
      atob(normalized)
        .split("")
        .map((c) => "%" + ("00" + c.charCodeAt(0).toString(16)).slice(-2))
        .join("")
    );
    return JSON.parse(decoded);
  } catch {
    return null;
  }
}

// Mirrors backend/app/utils/seed_data.py ROLE_PERMISSION_MAP so the UI
// can hide nav items a role has no access to. The backend is the real
// enforcement point (403s regardless) - this is just for UX.
export const ROLE_PERMISSIONS = {
  Admin: ["READ_LOGS", "VIEW_DASHBOARD", "MANAGE_USERS", "EXECUTE_AI_AGENT", "EXPORT_REPORTS"],
  "Security Analyst": ["READ_LOGS", "VIEW_DASHBOARD", "EXPORT_REPORTS"],
  Employee: ["VIEW_DASHBOARD"],
  "AI Agent": ["EXECUTE_AI_AGENT"],
};

export function hasPermission(role, permission) {
  return (ROLE_PERMISSIONS[role] || []).includes(permission);
}
