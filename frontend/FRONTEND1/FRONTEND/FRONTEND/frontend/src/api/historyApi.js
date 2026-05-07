import apiClient from "./client";

export const getHistory = async (params = {}) => {
  const { data } = await apiClient.get("/api/v1/history", { params });
  return data;
};
