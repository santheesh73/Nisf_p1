import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { startTextOptimization } from "../api/optimizeApi";
import { useJobStore } from "../store/jobStore";
import { addJobToHistory } from "../utils/jobHistory";

export function useOptimizeJob() {
  const navigate = useNavigate();
  const setCurrentJobId = useJobStore((state) => state.setCurrentJobId);
  const setCurrentJobStatus = useJobStore((state) => state.setCurrentJobStatus);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const formatOptimizeError = (err) => {
    if (err?.status === 429 || err?.code === "rate_limit_exceeded") {
      return "Optimization rate limit reached. Please try again shortly.";
    }
    if (err?.status === 422) {
      return "The backend rejected this optimization request. Check the form values and try again.";
    }
    if (/network error|timeout|failed to fetch/i.test(err?.message || "")) {
      return "The backend is offline or not responding. Make sure FastAPI is running on 127.0.0.1:8000.";
    }
    return err?.message || "Unable to start optimization.";
  };

  const startJob = async (payload) => {
    try {
      setLoading(true);
      setError("");
      const data = await startTextOptimization(payload);
      if (!data?.job_id) throw new Error("The backend did not return a job_id. Try again or check the optimize API response.");
      setCurrentJobId(data.job_id);
      setCurrentJobStatus(data.status || "queued");
      const now = new Date().toISOString();
      addJobToHistory({
        job_id: data.job_id,
        status: data.status || "queued",
        source: "optimize_text",
        text: payload.text,
        brief: payload.brief,
        content_type: payload.content_type,
        tone: payload.tone,
        platform: payload.platform,
        created_at: now,
        updated_at: now
      });
      navigate(`/jobs/${data.job_id}/progress`);
    } catch (err) {
      setError(formatOptimizeError(err));
    } finally {
      setLoading(false);
    }
  };

  return { startJob, loading, error };
}
