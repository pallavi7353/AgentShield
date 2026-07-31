import { Link } from "react-router-dom";
import { Radar } from "lucide-react";

export default function NotFound() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center text-center px-4">
      <Radar size={40} className="text-teal-glow mb-4" />
      <h1 className="font-display text-2xl font-semibold">Page not found</h1>
      <p className="text-sm text-slate-500 mt-2">This route doesn't exist in the security console.</p>
      <Link to="/" className="btn-primary mt-6">
        Back to dashboard
      </Link>
    </div>
  );
}
