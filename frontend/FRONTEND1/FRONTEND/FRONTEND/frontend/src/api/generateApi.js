import apiClient from "./client";

export const generateText = async (payload) => {
  const { data } = await apiClient.post("/api/v1/generate/text", payload);
  return data;
};
