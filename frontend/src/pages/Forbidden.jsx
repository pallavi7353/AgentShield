import { Link } from "react-router-dom";
import { ShieldOff } from "lucide-react";

export default function Forbidden() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center text-center px-4">
      <ShieldOff size={40} className="text-alert-critical mb-4" />
      <h1 className="font-display text-2xl font-semibold">Access denied</h1>
      <p className="text-sm text-slate-500 mt-2 max-w-sm">
        Your role doesn't have the permission required to view this page.
      </p>
      <Link to="/" className="btn-primary mt-6">
        Back to dashboard
      </Link>
    </div>
  );
}
