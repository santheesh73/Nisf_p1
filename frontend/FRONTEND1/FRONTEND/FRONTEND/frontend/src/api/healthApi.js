import apiClient from "./client";

export const getHealth = async () => {
  const { data } = await apiClient.get("/health");
  return data;
};

export const getApiHealth = async () => {
  const { data } = await apiClient.get("/api/v1/health");
  return data;
};
