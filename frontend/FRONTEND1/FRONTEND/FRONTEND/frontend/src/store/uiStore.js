import { create } from "zustand";

export const useUiStore = create((set) => ({
  loading: false,
  error: "",
  sidebarOpen: false,
  setLoading: (loading) => set({ loading }),
  setError: (error) => set({ error }),
  clearError: () => set({ error: "" }),
  toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen }))
}));
