import apiClient from "./client";

export const createOptimizationJob = async (payload) => {
  const { data } = await apiClient.post("/api/v1/optimize", payload);
  return data;
};

export const startTextOptimization = createOptimizationJob;
