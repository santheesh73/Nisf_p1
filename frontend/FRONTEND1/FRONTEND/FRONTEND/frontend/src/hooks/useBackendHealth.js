import { useCallback, useEffect, useState } from "react";
import { getHealth } from "../api/healthApi";

export function useBackendHealth(intervalMs = 0) {
  const [health, setHealth] = useState(null);
  const [online, setOnline] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const checkHealth = useCallback(async () => {
    try {
      setLoading(true);
      const data = await getHealth();
      setHealth(data);
      setOnline(true);
      setError("");
    } catch (err) {
      setOnline(false);
      setError(err.message || "Backend is not reachable. Make sure FastAPI is running on 127.0.0.1:8000.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    checkHealth();
    if (!intervalMs) return undefined;
    const timer = setInterval(checkHealth, intervalMs);
    return () => clearInterval(timer);
  }, [checkHealth, intervalMs]);

  return { health, online, loading, error, checkHealth };
}
