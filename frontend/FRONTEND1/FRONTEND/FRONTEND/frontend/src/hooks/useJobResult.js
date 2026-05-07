import { useEffect, useState } from "react";
import { getJobResult } from "../api/jobsApi";
import { useJobStore } from "../store/jobStore";

export function useJobResult(jobId) {
  const setLatestResult = useJobStore((state) => state.setLatestResult);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(Boolean(jobId));
  const [error, setError] = useState("");

  useEffect(() => {
    if (!jobId) {
      setError("Missing job_id. Cannot load result.");
      setLoading(false);
      return;
    }
    const load = async () => {
      try {
        setLoading(true);
        const data = await getJobResult(jobId);
        setResult(data);
        setLatestResult(data);
        setError("");
      } catch (err) {
        const notReady = err.status === 404 || err.status === 409;
        setError(notReady ? "Job result is not ready yet." : err.message || "Unable to load job result.");
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [jobId, setLatestResult]);

  return { result, loading, error };
}
