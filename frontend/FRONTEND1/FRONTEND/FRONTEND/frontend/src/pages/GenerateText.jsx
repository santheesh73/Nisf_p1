import { useState } from "react";
import { Clipboard, FileText, Send, Sparkles, Wand2 } from "lucide-react";
import { useNavigate } from "react-router-dom";
import Badge from "../components/common/Badge";
import Button from "../components/common/Button";
import Card from "../components/common/Card";
import EmptyState from "../components/common/EmptyState";
import ErrorMessage from "../components/common/ErrorMessage";
import Input from "../components/common/Input";
import PageHeader from "../components/common/PageHeader";
import Select from "../components/common/Select";
import Textarea from "../components/common/Textarea";
import { generateText } from "../api/generateApi";
import { createOptimizationJob } from "../api/optimizeApi";
import { CONTENT_TYPES, PLATFORMS, TONES } from "../utils/constants";
import { clampGenerateVariantCount, clampOptimizeVariantCount, parseBrandTerms } from "../utils/apiPayload";
import { labelize } from "../utils/scoreFormatter";
import { addJobToHistory } from "../utils/jobHistory";

const initialForm = {
  text: "Boost your mobile experience with our new AI-powered smartphone.",
  brief: "Create a persuasive Instagram ad copy for young professionals in India.",
  content_type: "ad_copy",
  tone: "persuasive",
  platform: "instagram",
  variant_count: 5,
  brand_terms: "AI-powered, smartphone, mobile experience",
  max_iterations: 3,
  target_score: 85,
  convergence_threshold: 2
};

const getVariantsFromResponse = (result) => (Array.isArray(result?.variants) ? result.variants : []);

const removeEmptyFields = (payload) =>
  Object.fromEntries(Object.entries(payload).filter(([, value]) => value !== undefined && value !== null));

const getOptimizationErrorMessage = (error) =>
  error?.status === 429 || error?.code === "rate_limit_exceeded"
    ? "Optimization rate limit reached. Please wait a bit before trying again."
    : error?.status === 422
      ? "This variant could not be optimized because the backend rejected the payload."
      : /network error|timeout|failed to fetch/i.test(error?.message || "")
        ? "The backend is offline or took too long to respond. Check that FastAPI is running on 127.0.0.1:8000."
        : "Could not start optimization for this variant.";

export default function GenerateText() {
  const navigate = useNavigate();
  const [form, setForm] = useState(initialForm);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [optimizingByVariantId, setOptimizingByVariantId] = useState({});
  const [optimizationErrorsByVariantId, setOptimizationErrorsByVariantId] = useState({});

  const update = (field, value) => setForm((prev) => ({ ...prev, [field]: value }));

  const submit = async (event) => {
    event.preventDefault();
    if (!form.text.trim() || !form.brief.trim()) {
      setError("Text and brief are required.");
      return;
    }

    const payload = {
      text: form.text,
      brief: form.brief,
      content_type: form.content_type,
      tone: form.tone,
      platform: form.platform,
      variant_count: clampGenerateVariantCount(form.variant_count),
      brand_terms: parseBrandTerms(form.brand_terms)
    };

    try {
      setLoading(true);
      setError("");
      setOptimizationErrorsByVariantId({});
      const data = await generateText(payload);
      setResult(data);
      if (!getVariantsFromResponse(data).length) setError("The backend returned an empty result.");
    } catch (err) {
      setError(err.message || "Unable to generate text.");
    } finally {
      setLoading(false);
    }
  };

  const handleOptimizeVariant = async (event, variant, index) => {
    event.preventDefault();
    event.stopPropagation();

    const variantKey = variant?.id || `variant-${index}`;
    const variantText = variant?.text || variant?.content;

    if (!variantText) {
      setOptimizationErrorsByVariantId((prev) => ({
        ...prev,
        [variantKey]: "Could not start optimization for this variant."
      }));
      return;
    }

    const payload = removeEmptyFields({
      text: variantText,
      brief: form.brief,
      content_type: form.content_type,
      tone: form.tone,
      platform: form.platform,
      max_iterations: Number(form.max_iterations || 3),
      target_score: Number(form.target_score || 85),
      convergence_threshold: Number(form.convergence_threshold || 2),
      variant_count: clampOptimizeVariantCount(form.variant_count),
      brand_terms: parseBrandTerms(form.brand_terms)
    });

    try {
      setOptimizingByVariantId((prev) => ({ ...prev, [variantKey]: true }));
      setOptimizationErrorsByVariantId((prev) => ({ ...prev, [variantKey]: "" }));

      const job = await createOptimizationJob(payload);
      const jobId = job?.job_id || job?.id;

      if (!jobId) {
        setOptimizationErrorsByVariantId((prev) => ({
          ...prev,
          [variantKey]: "Optimization did not return a job ID."
        }));
        return;
      }

      const now = new Date().toISOString();
      addJobToHistory({
        job_id: jobId,
        status: job.status || "queued",
        source: "generate_text",
        text: variantText || form.text,
        brief: form.brief,
        content_type: form.content_type,
        tone: form.tone,
        platform: form.platform,
        created_at: now,
        updated_at: now
      });

      navigate(`/jobs/${jobId}/progress`);
    } catch (err) {
      setOptimizationErrorsByVariantId((prev) => ({
        ...prev,
        [variantKey]: getOptimizationErrorMessage(err)
      }));
    } finally {
      setOptimizingByVariantId((prev) => ({ ...prev, [variantKey]: false }));
    }
  };

  const variants = getVariantsFromResponse(result);

  return (
    <>
      <PageHeader title="Generate Text" description="Generate backend-compatible NISF variants without starting an optimization job." />
      <div className="grid gap-6 xl:grid-cols-[0.95fr_1.05fr]">
        <form onSubmit={submit} className="space-y-6">
          <Card className="space-y-5">
            <div className="flex items-center justify-between gap-3">
              <div className="flex items-center gap-3">
                <div className="flex h-11 w-11 items-center justify-center rounded-2xl border border-slate-300/70 bg-slate-100/70 text-slate-700"><Sparkles className="h-5 w-5" /></div>
                <div>
                  <h2 className="text-lg font-black text-slate-950">Generation Brief</h2>
                  <p className="text-sm text-slate-500">POST /api/v1/generate/text</p>
                </div>
              </div>
              <Button type="submit" loading={loading} disabled={loading} className="hidden sm:inline-flex">
                <Send className="h-4 w-4" /> {loading ? "Generating" : "Generate"}
              </Button>
            </div>

            <Textarea label="Text" value={form.text} onChange={(e) => update("text", e.target.value)} className="min-h-32" />
            <Textarea label="Brief" value={form.brief} onChange={(e) => update("brief", e.target.value)} className="min-h-28" />
            <Input label="Brand Terms" helper="Comma-separated here, sent as an array to the backend." value={form.brand_terms} onChange={(e) => update("brand_terms", e.target.value)} />

            <div className="grid gap-4 sm:grid-cols-2">
              <Select label="Content Type" options={CONTENT_TYPES} value={form.content_type} onChange={(e) => update("content_type", e.target.value)} />
              <Select label="Tone" options={TONES} value={form.tone} onChange={(e) => update("tone", e.target.value)} />
              <Select label="Platform" options={PLATFORMS} value={form.platform} onChange={(e) => update("platform", e.target.value)} />
              <Select label="Variant Count" options={["1", "2", "3", "4", "5"]} value={String(form.variant_count)} onChange={(e) => update("variant_count", e.target.value)} />
            </div>

            <div className="grid gap-4 sm:grid-cols-2">
              <Input label="Max Iterations" type="number" min="1" value={form.max_iterations} onChange={(e) => update("max_iterations", e.target.value)} />
              <Input label="Target Score" type="number" min="1" max="100" value={form.target_score} onChange={(e) => update("target_score", e.target.value)} />
            </div>

            <ErrorMessage message={error} />
            <Button type="submit" loading={loading} disabled={loading} className="w-full sm:hidden">
              <Send className="h-4 w-4" /> {loading ? "Generating" : "Generate"}
            </Button>
          </Card>
        </form>

        <div className="space-y-6">
          {result ? (
            <>
              <Card>
                <div className="flex flex-wrap items-center gap-3">
                  <Badge className="border-slate-300 bg-slate-100/70 text-slate-700">Provider: {result?.provider || "Unknown"}</Badge>
                  <Badge className="border-slate-300 bg-slate-100/70 text-slate-700">Model: {result?.model || "Unknown"}</Badge>
                  <Badge className="border-slate-300 bg-slate-100/70 text-slate-700">Variants: {result?.variant_count ?? variants.length}</Badge>
                </div>
              </Card>

              {variants.length ? (
                <div className="grid gap-4">
                  {variants.map((variant, index) => (
                    <Card key={variant?.id || index} className="space-y-4">
                      <div className="flex flex-wrap items-start justify-between gap-3">
                        <div>
                          <Badge className="border-slate-300 bg-white/70 text-[#54566f]"><FileText className="h-3.5 w-3.5" /> {variant?.id || `variant-${index + 1}`}</Badge>
                          <div className="mt-3 flex flex-wrap gap-2">
                            <Badge className="border-slate-300/80 bg-slate-100/70 text-slate-700">{labelize(variant?.metadata?.content_type || "content")}</Badge>
                            <Badge className="border-slate-300/80 bg-slate-100/70 text-slate-700">{labelize(variant?.metadata?.tone || "tone")}</Badge>
                            <Badge className="border-slate-300/80 bg-slate-100/70 text-slate-700">{labelize(variant?.metadata?.platform || "platform")}</Badge>
                          </div>
                        </div>
                        <div className="flex flex-wrap gap-2">
                          <Button
                            type="button"
                            onClick={(event) => handleOptimizeVariant(event, variant, index)}
                            loading={Boolean(optimizingByVariantId[variant?.id || `variant-${index}`])}
                            disabled={Boolean(optimizingByVariantId[variant?.id || `variant-${index}`])}
                          >
                            <Wand2 className="h-4 w-4" />
                            {optimizingByVariantId[variant?.id || `variant-${index}`]
                              ? "Optimizing..."
                              : optimizationErrorsByVariantId[variant?.id || `variant-${index}`]
                                ? "Retry Optimize"
                                : "Optimize"}
                          </Button>
                          <Button type="button" variant="ghost" className="px-3" title="Copy variant" onClick={() => navigator.clipboard?.writeText(variant?.text || variant?.content || "")}>
                            <Clipboard className="h-4 w-4" />
                          </Button>
                        </div>
                      </div>
                      <p className="whitespace-pre-wrap text-base font-semibold leading-7 text-slate-900">{variant?.text || variant?.content || "No text returned for this variant."}</p>
                      <ErrorMessage message={optimizationErrorsByVariantId[variant?.id || `variant-${index}`]} />
                    </Card>
                  ))}
                </div>
              ) : (
                <EmptyState title="Empty Result" message="The backend responded, but no variants were returned." />
              )}
            </>
          ) : (
            <EmptyState title="Ready to Generate" message="Submit the default brief to generate text variants from the backend." />
          )}
        </div>
      </div>
    </>
  );
}
