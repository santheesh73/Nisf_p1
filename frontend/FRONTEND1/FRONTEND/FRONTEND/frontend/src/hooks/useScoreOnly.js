import { useState } from "react";
import { scoreText } from "../api/scoreApi";

export function useScoreOnly() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const submitScore = async (payload) => {
    try {
      setLoading(true);
      setError("");
      const data = await scoreText(payload);
      setResult(data);
    } catch (err) {
      setError(err.message || "Unable to score text.");
    } finally {
      setLoading(false);
    }
  };

  return { submitScore, result, loading, error };
}
