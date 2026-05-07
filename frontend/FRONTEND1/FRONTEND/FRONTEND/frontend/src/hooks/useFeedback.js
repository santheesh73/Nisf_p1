import { useState } from "react";
import { submitFeedback } from "../api/feedbackApi";

export function useFeedback() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const sendFeedback = async (payload) => {
    try {
      setLoading(true);
      setError("");
      setSuccess("");
      await submitFeedback(payload);
      setSuccess("Engagement feedback submitted successfully.");
    } catch (err) {
      setError(err.message || "Unable to submit feedback.");
    } finally {
      setLoading(false);
    }
  };

  return { sendFeedback, loading, error, success };
}
