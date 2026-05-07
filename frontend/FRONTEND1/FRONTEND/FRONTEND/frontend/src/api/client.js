import axios from "axios";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

const REQUEST_BASE_URL = import.meta.env.DEV ? "" : API_BASE_URL.replace(/\/$/, "");

const apiClient = axios.create({
  baseURL: REQUEST_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 30000,
});

apiClient.interceptors.request.use((config) => {
  const token = window.localStorage.getItem("nisf_access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error?.response?.status === 401) {
      window.localStorage.removeItem("nisf_access_token");
      window.localStorage.removeItem("nisf_user");
      window.localStorage.setItem("nisf_session_message", "Your session expired. Please sign in again.");
      if (!window.location.pathname.startsWith("/login") && !window.location.pathname.startsWith("/register")) {
        window.location.assign("/login");
      }
    }
    const detail = error?.response?.data?.detail;
    const structuredError = error?.response?.data?.error;
    const message =
      typeof detail === "string"
        ? detail
        : Array.isArray(detail)
        ? detail.map((d) => d.msg || JSON.stringify(d)).join(", ")
        : structuredError?.message ||
          error?.response?.data?.message ||
          error?.message ||
          "API request failed";

    return Promise.reject({
      status: error?.response?.status,
      code: structuredError?.code,
      message,
      data: error?.response?.data,
      raw: error,
    });
  }
);

export default apiClient;
export { API_BASE_URL };
