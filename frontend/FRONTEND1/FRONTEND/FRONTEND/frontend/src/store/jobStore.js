import { create } from "zustand";

export const useJobStore = create((set) => ({
  currentJobId: "",
  currentJobStatus: "",
  latestResult: null,
  setCurrentJobId: (currentJobId) => set({ currentJobId }),
  setCurrentJobStatus: (currentJobStatus) => set({ currentJobStatus }),
  setLatestResult: (latestResult) => set({ latestResult }),
  clearJob: () => set({ currentJobId: "", currentJobStatus: "", latestResult: null })
}));
