import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import ProtectedRoute from "./components/ProtectedRoute";
import Layout from "./components/Layout";

import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Analyze from "./pages/Analyze";
import ThreatHistory from "./pages/ThreatHistory";
import Alerts from "./pages/Alerts";
import AuditLogs from "./pages/AuditLogs";
import Users from "./pages/Users";
import Forbidden from "./pages/Forbidden";
import NotFound from "./pages/NotFound";

function withLayout(page, permission) {
  return (
    <ProtectedRoute permission={permission}>
      <Layout>{page}</Layout>
    </ProtectedRoute>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/forbidden" element={<Forbidden />} />

          <Route path="/" element={withLayout(<Dashboard />, "VIEW_DASHBOARD")} />
          <Route path="/analyze" element={withLayout(<Analyze />, "EXECUTE_AI_AGENT")} />
          <Route path="/threats" element={withLayout(<ThreatHistory />, "READ_LOGS")} />
          <Route path="/alerts" element={withLayout(<Alerts />, "VIEW_DASHBOARD")} />
          <Route path="/audit" element={withLayout(<AuditLogs />, "READ_LOGS")} />
          <Route path="/users" element={withLayout(<Users />, "MANAGE_USERS")} />

          <Route path="*" element={<NotFound />} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}
