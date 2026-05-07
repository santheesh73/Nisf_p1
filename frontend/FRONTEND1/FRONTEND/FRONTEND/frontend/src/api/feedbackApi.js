import apiClient from "./client";

export const submitFeedback = async (payload) => {
  const { data } = await apiClient.post("/api/v1/feedback", payload);
  return data;
};
