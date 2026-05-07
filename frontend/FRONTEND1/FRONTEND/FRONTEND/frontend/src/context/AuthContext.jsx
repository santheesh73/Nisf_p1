import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import * as authApi from "../api/authApi";

const AuthContext = createContext(null);

const readStoredUser = () => {
  try {
    return JSON.parse(window.localStorage.getItem("nisf_user") || "null");
  } catch {
    return null;
  }
};

export function AuthProvider({ children }) {
  const navigate = useNavigate();
  const [token, setToken] = useState(() => window.localStorage.getItem("nisf_access_token"));
  const [user, setUser] = useState(readStoredUser);
  const [loading, setLoading] = useState(true);
  const [authEnabled, setAuthEnabled] = useState(true);
  const [sessionMessage, setSessionMessage] = useState(() => window.localStorage.getItem("nisf_session_message") || "");

  const persistSession = useCallback((authPayload) => {
    window.localStorage.setItem("nisf_access_token", authPayload.access_token);
    window.localStorage.setItem("nisf_user", JSON.stringify(authPayload.user));
    setToken(authPayload.access_token);
    setUser(authPayload.user);
  }, []);

  const loadCurrentUser = useCallback(async () => {
    setLoading(true);
    try {
      const config = await authApi.getAuthConfig();
      setAuthEnabled(config.auth_enabled);
      const storedToken = window.localStorage.getItem("nisf_access_token");
      if (config.auth_enabled && !storedToken) {
        setToken(null);
        setUser(null);
        return;
      }
      const me = await authApi.getMe();
      setUser(me);
      window.localStorage.setItem("nisf_user", JSON.stringify(me));
    } catch {
      setUser(null);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadCurrentUser();
  }, [loadCurrentUser]);

  useEffect(() => {
    if (sessionMessage) {
      window.localStorage.removeItem("nisf_session_message");
    }
  }, [sessionMessage]);

  const login = useCallback(
    async (payload) => {
      const response = await authApi.login(payload);
      persistSession(response);
      setSessionMessage("");
      navigate("/generate/text", { replace: true });
    },
    [navigate, persistSession]
  );

  const register = useCallback(
    async (payload) => {
      const response = await authApi.register(payload);
      persistSession(response);
      setSessionMessage("");
      navigate("/generate/text", { replace: true });
    },
    [navigate, persistSession]
  );

  const logout = useCallback(() => {
    window.localStorage.removeItem("nisf_access_token");
    window.localStorage.removeItem("nisf_user");
    setToken(null);
    setUser(null);
    navigate("/login", { replace: true });
  }, [navigate]);

  const value = useMemo(
    () => ({
      user,
      token,
      authEnabled,
      sessionMessage,
      loading,
      isAuthenticated: Boolean(user) || !authEnabled,
      login,
      register,
      logout,
      loadCurrentUser,
      clearSessionMessage: () => setSessionMessage(""),
    }),
    [authEnabled, loadCurrentUser, loading, login, logout, register, sessionMessage, token, user]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const value = useContext(AuthContext);
  if (!value) {
    throw new Error("useAuth must be used within AuthProvider");
  }
  return value;
}
