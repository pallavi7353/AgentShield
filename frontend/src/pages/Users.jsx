import { useEffect, useState } from "react";
import { Users as UsersIcon, Trash2, Plus, X } from "lucide-react";
import api from "../lib/api";
import { Spinner, EmptyState } from "../components/ui";

export default function Users() {
  const [users, setUsers] = useState(null);
  const [roles, setRoles] = useState([]);
  const [error, setError] = useState("");
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({ username: "", email: "", password: "", role_id: "" });
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    load();
  }, []);

  function load() {
    Promise.all([api.get("/users"), api.get("/roles")])
      .then(([u, r]) => {
        setUsers(u.data);
        setRoles(r.data);
        setForm((f) => ({ ...f, role_id: f.role_id || r.data[0]?.id || "" }));
      })
      .catch(() => setError("Could not load users/roles."));
  }

  async function createUser(e) {
    e.preventDefault();
    setSubmitting(true);
    setError("");
    try {
      await api.post("/users", { ...form, role_id: Number(form.role_id) });
      setForm({ username: "", email: "", password: "", role_id: roles[0]?.id || "" });
      setShowForm(false);
      load();
    } catch (err) {
      setError(err.response?.data?.detail || "Could not create user.");
    } finally {
      setSubmitting(false);
    }
  }

  async function updateRole(userId, roleId) {
    try {
      await api.put(`/users/${userId}`, { role_id: Number(roleId) });
      load();
    } catch {
      setError("Could not update role.");
    }
  }

  async function updateStatus(userId, status) {
    try {
      await api.put(`/users/${userId}`, { status });
      load();
    } catch {
      setError("Could not update status.");
    }
  }

  async function deleteUser(userId) {
    if (!confirm("Delete this user? This cannot be undone.")) return;
    try {
      await api.delete(`/users/${userId}`);
      load();
    } catch {
      setError("Could not delete user.");
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-start justify-between">
        <div>
          <h1 className="font-display text-2xl font-semibold flex items-center gap-2">
            <UsersIcon size={20} className="text-teal-glow" />
            Users &amp; Roles
          </h1>
          <p className="text-sm text-slate-500 mt-1">Admin-only: manage accounts and role assignments.</p>
        </div>
        <button onClick={() => setShowForm((s) => !s)} className="btn-primary">
          {showForm ? <X size={16} /> : <Plus size={16} />}
          {showForm ? "Cancel" : "New user"}
        </button>
      </div>

      {error && <p className="text-alert-critical text-sm">{error}</p>}

      {showForm && (
        <form onSubmit={createUser} className="card p-5 grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label className="text-xs font-medium text-slate-400 mb-1.5 block">Username</label>
            <input
              className="input-field"
              value={form.username}
              onChange={(e) => setForm({ ...form, username: e.target.value })}
              required
              minLength={3}
            />
          </div>
          <div>
            <label className="text-xs font-medium text-slate-400 mb-1.5 block">Email</label>
            <input
              type="email"
              className="input-field"
              value={form.email}
              onChange={(e) => setForm({ ...form, email: e.target.value })}
              required
            />
          </div>
          <div>
            <label className="text-xs font-medium text-slate-400 mb-1.5 block">Password</label>
            <input
              type="password"
              className="input-field"
              value={form.password}
              onChange={(e) => setForm({ ...form, password: e.target.value })}
              required
              minLength={8}
            />
          </div>
          <div>
            <label className="text-xs font-medium text-slate-400 mb-1.5 block">Role</label>
            <select
              className="input-field"
              value={form.role_id}
              onChange={(e) => setForm({ ...form, role_id: e.target.value })}
            >
              {roles.map((r) => (
                <option key={r.id} value={r.id} className="bg-ink-900">
                  {r.role_name}
                </option>
              ))}
            </select>
          </div>
          <div className="sm:col-span-2">
            <button type="submit" disabled={submitting} className="btn-primary">
              {submitting ? "Creating…" : "Create user"}
            </button>
          </div>
        </form>
      )}

      {!users && !error && <Spinner />}
      {users && users.length === 0 && <EmptyState title="No users found" />}

      {users && users.length > 0 && (
        <div className="card overflow-hidden">
          <table className="w-full text-sm">
            <thead>
              <tr className="text-left text-xs uppercase tracking-wide text-slate-500 border-b border-ink-700/70">
                <th className="px-5 py-3 font-medium">Username</th>
                <th className="px-5 py-3 font-medium">Email</th>
                <th className="px-5 py-3 font-medium">Role</th>
                <th className="px-5 py-3 font-medium">Status</th>
                <th className="px-5 py-3 font-medium">Created</th>
                <th className="px-5 py-3 font-medium"></th>
              </tr>
            </thead>
            <tbody>
              {users.map((u) => (
                <tr key={u.id} className="border-b border-ink-700/40 last:border-0 hover:bg-ink-700/20">
                  <td className="px-5 py-3 text-slate-200 font-medium">{u.username}</td>
                  <td className="px-5 py-3 text-slate-400">{u.email}</td>
                  <td className="px-5 py-3">
                    <select
                      value={u.role_id}
                      onChange={(e) => updateRole(u.id, e.target.value)}
                      className="bg-transparent border border-ink-600 rounded-md px-2 py-1 text-xs"
                    >
                      {roles.map((r) => (
                        <option key={r.id} value={r.id} className="bg-ink-900">
                          {r.role_name}
                        </option>
                      ))}
                    </select>
                  </td>
                  <td className="px-5 py-3">
                    <select
                      value={u.status}
                      onChange={(e) => updateStatus(u.id, e.target.value)}
                      className="bg-transparent border border-ink-600 rounded-md px-2 py-1 text-xs capitalize"
                    >
                      {["active", "inactive", "locked"].map((s) => (
                        <option key={s} value={s} className="bg-ink-900">
                          {s}
                        </option>
                      ))}
                    </select>
                  </td>
                  <td className="px-5 py-3 text-slate-500 text-xs">
                    {new Date(u.created_at).toLocaleDateString()}
                  </td>
                  <td className="px-5 py-3 text-right">
                    <button onClick={() => deleteUser(u.id)} className="text-slate-500 hover:text-alert-critical transition">
                      <Trash2 size={15} />
                    </button>
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
