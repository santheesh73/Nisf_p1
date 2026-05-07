import apiClient from "./client";

export const getJobResult = async (jobId) => {
  const { data } = await apiClient.get(`/api/v1/jobs/${jobId}/result`);
  return data;
};

export const getJobStatus = async (jobId) => {
  const { data } = await apiClient.get(`/api/v1/jobs/${jobId}/status`);
  return data;
};
