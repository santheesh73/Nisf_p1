import { useMemo, useState } from "react";
import { Gauge, Layers, Send, Wand2 } from "lucide-react";
import Badge from "../components/common/Badge";
import Button from "../components/common/Button";
import Card from "../components/common/Card";
import ErrorMessage from "../components/common/ErrorMessage";
import Input from "../components/common/Input";
import PageHeader from "../components/common/PageHeader";
import Select from "../components/common/Select";
import Textarea from "../components/common/Textarea";
import { useOptimizeJob } from "../hooks/useOptimizeJob";
import { useTemplateStore } from "../store/templateStore";
import { CONTENT_TYPES, PLATFORMS, TONES } from "../utils/constants";
import { clampOptimizeVariantCount, parseBrandTerms } from "../utils/apiPayload";

const initialForm = {
  text: "Boost your mobile experience with our new AI-powered smartphone.",
  brief: "Create a persuasive Instagram ad copy for young professionals in India.",
  content_type: "ad_copy",
  tone: "persuasive",
  platform: "instagram",
  max_iterations: 3,
  target_score: 85,
  convergence_threshold: 2,
  brand_terms: "AI-powered, smartphone, mobile experience",
  variant_count: 5
};

export default function OptimizeText() {
  const selectedTemplate = useTemplateStore((state) => state.selectedTemplate);
  const clearSelectedTemplate = useTemplateStore((state) => state.clearSelectedTemplate);
  const seededForm = useMemo(() => ({
    ...initialForm,
    text: selectedTemplate?.prompt || selectedTemplate?.description || initialForm.text,
    brief: selectedTemplate?.description || initialForm.brief,
    content_type: selectedTemplate?.content_type || initialForm.content_type
  }), [selectedTemplate]);
  const [form, setForm] = useState(seededForm);
  const [validationError, setValidationError] = useState("");
  const { startJob, loading, error } = useOptimizeJob();

  const update = (field, value) => setForm((prev) => ({ ...prev, [field]: value }));

  const submit = (event) => {
    event.preventDefault();
    if (!form.text.trim() || !form.brief.trim()) {
      setValidationError("Input text is required.");
      return;
    }
    setValidationError("");
    clearSelectedTemplate();
    startJob({
      text: form.text,
      brief: form.brief,
      content_type: form.content_type,
      tone: form.tone,
      platform: form.platform,
      max_iterations: Number(form.max_iterations),
      target_score: Number(form.target_score),
      convergence_threshold: Number(form.convergence_threshold || 2),
      variant_count: clampOptimizeVariantCount(form.variant_count),
      brand_terms: parseBrandTerms(form.brand_terms)
    });
  };

  const summary = [
    ["Content", form.content_type],
    ["Tone", form.tone],
    ["Platform", form.platform],
    ["Iterations", form.max_iterations],
    ["Target", form.target_score],
    ["Variants", clampOptimizeVariantCount(form.variant_count)]
  ];

  return (
    <>
      <PageHeader title="Optimize Text" description="Launch a NISF optimization loop with critic feedback and score-driven variants." />
      <form id="optimize-text-form" onSubmit={submit} className="grid animate-[fadeInUp_220ms_ease-out] gap-8 xl:grid-cols-[minmax(0,1.15fr)_minmax(320px,0.85fr)]">
        <Card className="space-y-6 hover:-translate-y-0.5">
          <div className="flex flex-col gap-5 sm:flex-row sm:items-center sm:justify-between">
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-xl border border-slate-300/70 bg-slate-100/70 text-slate-700"><Wand2 className="h-5 w-5" /></div>
              <div>
                <h2 className="text-lg font-semibold tracking-tight text-slate-950">Source Copy</h2>
                <p className="mt-1 text-sm leading-5 text-slate-500">Paste the copy NISF should improve and score.</p>
              </div>
            </div>
            <Button type="submit" loading={loading} disabled={loading} className="min-h-12 w-full px-5 sm:w-auto">
              <Send className="h-4 w-4" /> {loading ? "Starting Optimization" : "Start Optimization"}
            </Button>
          </div>
          <Textarea
            label="Input Text"
            value={form.text}
            onChange={(e) => update("text", e.target.value)}
            placeholder="Boost your brand with AI-powered marketing content."
            error={validationError}
            helper="This is sent as text to the backend optimize API."
            className="min-h-[16rem]"
          />
          <Textarea
            label="Brief"
            value={form.brief}
            onChange={(e) => update("brief", e.target.value)}
            placeholder="Describe the requested output and campaign context."
            className="min-h-28"
          />
          <div id="optimization-summary" className="border border-slate-300/70 bg-slate-50/70 p-5">
            <div className="mb-4 flex items-center gap-2 text-sm font-semibold text-slate-800"><Layers className="h-4 w-4" /> Optimization Summary</div>
            <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
              {summary.map(([label, value]) => (
                <div key={label} className="rounded-lg border border-slate-300/80 bg-[#fbfcf8]/80 px-3 py-2.5 transition-colors hover:border-slate-300 hover:bg-white">
                  <div className="text-[10px] font-bold uppercase tracking-wider text-slate-500/90">{label}</div>
                  <div className="mt-0.5 text-sm font-bold text-slate-800">{String(value).replaceAll("_", " ")}</div>
                </div>
              ))}
            </div>
          </div>
          <ErrorMessage message={error} />
        </Card>

        <Card className="space-y-5 hover:-translate-y-0.5">
          <div className="flex items-center justify-between gap-3">
            <div>
              <h2 className="text-lg font-semibold tracking-tight text-slate-950">Configuration</h2>
              <p className="mt-1 text-sm leading-5 text-slate-500">Tune generation without changing the API contract.</p>
            </div>
            <Badge className="border-slate-300 bg-slate-100/70 text-slate-700 shadow-none"><Gauge className="h-3.5 w-3.5" /> Live</Badge>
          </div>
          <Select label="Content Type" helper="Marketing format for scoring context." options={CONTENT_TYPES} value={form.content_type} onChange={(e) => update("content_type", e.target.value)} />
          <Input label="Brand Terms" helper="Comma-separated here, sent as an array to the backend." value={form.brand_terms} onChange={(e) => update("brand_terms", e.target.value)} />
          <Select label="Tone" helper="Desired voice and persuasion style." options={TONES} value={form.tone} onChange={(e) => update("tone", e.target.value)} />
          <Select label="Platform" helper="Channel-specific optimization context." options={PLATFORMS} value={form.platform} onChange={(e) => update("platform", e.target.value)} />
          <div className="grid gap-4 sm:grid-cols-2">
            <Select label="Max Iterations" options={["1", "2", "3", "4", "5"]} value={String(form.max_iterations)} onChange={(e) => update("max_iterations", e.target.value)} />
            <Select label="Variant Count" options={["3", "4", "5"]} value={String(clampOptimizeVariantCount(form.variant_count))} onChange={(e) => update("variant_count", e.target.value)} />
          </div>
          <Input label="Target Score" helper="Stop once the composite score reaches this target." type="number" min="0" max="100" value={form.target_score} onChange={(e) => update("target_score", e.target.value)} />
        </Card>
      </form>
    </>
  );
}
