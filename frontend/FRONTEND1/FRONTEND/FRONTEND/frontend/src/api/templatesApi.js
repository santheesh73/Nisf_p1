import apiClient from "./client";

export const getTemplates = async () => {
  const { data } = await apiClient.get("/api/v1/templates");
  return data;
};
