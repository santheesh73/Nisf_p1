import apiClient from "./client";

export const scoreText = async (payload) => {
  const { data } = await apiClient.post("/api/v1/score", payload);
  return data;
};
