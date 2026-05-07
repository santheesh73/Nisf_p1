import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { ArrowRight, FileText, Sparkles } from "lucide-react";
import Badge from "../components/common/Badge";
import { getTemplates } from "../api/templatesApi";
import Button from "../components/common/Button";
import Card from "../components/common/Card";
import ErrorMessage from "../components/common/ErrorMessage";
import Loader from "../components/common/Loader";
import PageHeader from "../components/common/PageHeader";
import { useTemplateStore } from "../store/templateStore";
import { DEFAULT_TEMPLATES } from "../utils/constants";
import { labelize } from "../utils/scoreFormatter";

const withDescriptions = (templates) => templates.map((template) => ({
  ...template,
  title: template.title || template.name || labelize(template.content_type || template.id),
  description: template.description || template.prompt || "Starter structure for NISF optimization."
}));

export default function Templates() {
  const navigate = useNavigate();
  const setSelectedTemplate = useTemplateStore((state) => state.setSelectedTemplate);
  const setTemplates = useTemplateStore((state) => state.setTemplates);
  const [templates, setLocalTemplates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const load = async () => {
      try {
        const data = await getTemplates();
        const list = withDescriptions(Array.isArray(data) ? data : data?.templates || []);
        setLocalTemplates(list.length ? list : withDescriptions(DEFAULT_TEMPLATES));
        setTemplates(list.length ? list : DEFAULT_TEMPLATES);
      } catch (err) {
        setError(err.message || "Templates API unavailable. Showing fallback templates.");
        setLocalTemplates(withDescriptions(DEFAULT_TEMPLATES));
        setTemplates(DEFAULT_TEMPLATES);
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [setTemplates]);

  const useTemplate = (template) => {
    setSelectedTemplate(template);
    navigate("/generate/text");
  };

  return (
    <>
      <PageHeader
        title="Templates"
        description="Start from proven content patterns and send them into the optimization loop."
        actions={error && <Badge className="border-amber-300 bg-amber-100/70 text-amber-700">Fallback Templates</Badge>}
      />
      {loading && <Loader label="Loading templates" />}
      <ErrorMessage message={error} />
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {templates.map((template) => (
          <Card key={template.id || template.content_type} className="group hover:-translate-y-1 hover:border-slate-400 hover:shadow-[0_24px_70px_rgba(52,52,73,0.12)]">
            <div className="mb-4 flex items-center justify-between gap-3">
              <div className="flex h-11 w-11 items-center justify-center rounded-2xl border border-slate-300/60 bg-gradient-to-br from-[#E5E6E8] to-[#E8E9EC] text-[#4a4b61] shadow-sm"><FileText className="h-5 w-5" /></div>
              <Badge className="border-slate-300/80 bg-white/70 text-[#777a91]">{labelize(template.platform || "website")}</Badge>
            </div>
            <Badge className="border-slate-300/60 bg-gradient-to-br from-[#E5E6E8] to-[#E8E9EC] text-[#4a4b61] shadow-sm"><Sparkles className="h-3.5 w-3.5" /> {labelize(template.content_type || "template")}</Badge>
            <h2 className="mt-4 text-lg font-black text-slate-950">{template.title}</h2>
            <p className="mt-2 min-h-20 text-sm leading-6 text-slate-500">{template.description}</p>
            <Button className="group mt-5 w-full" variant="primary" onClick={() => useTemplate(template)}>Use Template <ArrowRight className="h-4 w-4 group-hover:animate-[arrowFly_0.6s_ease-in-out]" /></Button>
          </Card>
        ))}
      </div>
    </>
  );
}
