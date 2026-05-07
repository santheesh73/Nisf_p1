import { useEffect, useState } from "react";
import { getJobStatus } from "../api/jobsApi";
import { useJobStore } from "../store/jobStore";
import { TERMINAL_STATUSES } from "../utils/constants";

export function useJobStatus(jobId) {
  const setCurrentJobStatus = useJobStore((state) => state.setCurrentJobStatus);
  const [status, setStatus] = useState("");
  const [loading, setLoading] = useState(Boolean(jobId));
  const [error, setError] = useState("");
  const [timedOut, setTimedOut] = useState(false);

  const formatStatusError = (err) => {
    if (err?.status === 404) {
      return "This optimization job could not be found.";
    }
    if (err?.status === 429 || err?.code === "rate_limit_exceeded") {
      return "Status polling is being rate limited. Please wait a moment and try again.";
    }
    if (/network error|timeout|failed to fetch/i.test(err?.message || "")) {
      return "The backend is offline or not responding. Make sure FastAPI is running on 127.0.0.1:8000.";
    }
    return err?.message || "Unable to fetch job status.";
  };

  useEffect(() => {
    if (!jobId) {
      setError("Missing job_id. Start an optimization job first.");
      setLoading(false);
      setTimedOut(false);
      return undefined;
    }
    let active = true;
    let timer;
    const startedAt = Date.now();
    const poll = async () => {
      if (Date.now() - startedAt >= 60000) {
        if (!active) return;
        setTimedOut(true);
        setError("Optimization timed out. Please return to Generate Text and try again.");
        setLoading(false);
        return;
      }
      try {
        const data = await getJobStatus(jobId);
        const nextStatus = data?.status || data?.job_status || "";
        if (!active) return;
        setStatus(nextStatus);
        setCurrentJobStatus(nextStatus);
        setTimedOut(false);
        setError("");
        setLoading(!TERMINAL_STATUSES.includes(nextStatus));
        if (!TERMINAL_STATUSES.includes(nextStatus)) timer = setTimeout(poll, 2000);
      } catch (err) {
        if (!active) return;
        setError(formatStatusError(err));
        setLoading(false);
      }
    };
    poll();
    return () => {
      active = false;
      clearTimeout(timer);
    };
  }, [jobId, setCurrentJobStatus]);

  return { status, loading, error, timedOut };
}
