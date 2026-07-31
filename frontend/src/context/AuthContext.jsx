import { createContext, useContext, useEffect, useState } from "react";
import api from "../lib/api";
import { decodeJwt } from "../lib/jwt";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null); // { username, role }
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (token) {
      const claims = decodeJwt(token);
      if (claims) setUser({ username: claims.sub, role: claims.role });
    }
    setLoading(false);
  }, []);

  async function login(username, password) {
    const { data } = await api.post("/auth/login", { username, password });
    localStorage.setItem("access_token", data.access_token);
    localStorage.setItem("refresh_token", data.refresh_token);
    const claims = decodeJwt(data.access_token);
    setUser({ username: claims.sub, role: claims.role });
    return claims;
  }

  async function logout() {
    try {
      await api.post("/auth/logout");
    } catch {
      /* best-effort */
    }
    localStorage.clear();
    setUser(null);
  }

  return (
    <AuthContext.Provider value={{ user, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
