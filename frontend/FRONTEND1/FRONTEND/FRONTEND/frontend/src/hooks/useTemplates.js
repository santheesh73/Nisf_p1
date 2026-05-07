import { useEffect, useState } from "react";
import { getTemplates } from "../api/templatesApi";
import { useTemplateStore } from "../store/templateStore";
import { DEFAULT_TEMPLATES } from "../utils/constants";

export function useTemplates() {
  const setTemplates = useTemplateStore((state) => state.setTemplates);
  const templates = useTemplateStore((state) => state.templates);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    const load = async () => {
      try {
        setLoading(true);
        const data = await getTemplates();
        const list = Array.isArray(data) ? data : data?.templates;
        setTemplates(list?.length ? list : DEFAULT_TEMPLATES);
        setError("");
      } catch (err) {
        setTemplates(DEFAULT_TEMPLATES);
        setError(err.message || "Using built-in templates while backend templates are unavailable.");
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [setTemplates]);

  return { templates: templates.length ? templates : DEFAULT_TEMPLATES, loading, error };
}
