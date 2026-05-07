import { create } from "zustand";

export const useTemplateStore = create((set) => ({
  selectedTemplate: null,
  templates: [],
  setSelectedTemplate: (selectedTemplate) => set({ selectedTemplate }),
  setTemplates: (templates) => set({ templates }),
  clearSelectedTemplate: () => set({ selectedTemplate: null })
}));
