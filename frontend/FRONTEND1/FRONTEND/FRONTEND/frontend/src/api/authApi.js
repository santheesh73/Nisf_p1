import apiClient from "./client";

export const register = (payload) => apiClient.post("/api/v1/auth/register", payload).then((res) => res.data);

export const login = (payload) => apiClient.post("/api/v1/auth/login", payload).then((res) => res.data);

export const getMe = () => apiClient.get("/api/v1/auth/me").then((res) => res.data);

export const getAuthConfig = () => apiClient.get("/api/v1/auth/config").then((res) => res.data);
