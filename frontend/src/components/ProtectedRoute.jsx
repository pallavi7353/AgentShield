import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { hasPermission } from "../lib/jwt";

export default function ProtectedRoute({ children, permission }) {
  const { user, loading } = useAuth();

  if (loading) return null;
  if (!user) return <Navigate to="/login" replace />;
  if (permission && !hasPermission(user.role, permission)) {
    return <Navigate to="/forbidden" replace />;
  }
  return children;
}
