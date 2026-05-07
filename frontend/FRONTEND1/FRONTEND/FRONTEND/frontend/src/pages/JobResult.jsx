import { useEffect, useState } from "react";
import { Check, Clipboard } from "lucide-react";
import { useParams } from "react-router-dom";
import Badge from "../components/common/Badge";
import Button from "../components/common/Button";
import Card from "../components/common/Card";
import PageHeader from "../components/common/PageHeader";
import { getJobResult } from "../api/jobsApi";
import { labelize } from "../utils/scoreFormatter";
import { updateJobInHistory } from "../utils/jobHistory";

const getBestVariantText = (result) =>
  result?.best_variant?.content ??
  result?.best_variant?.text ??
  (typeof result?.best_variant === "string" ? result.best_variant : "") ??
  "";

const getScores = (result) =>
  result?.scores ??
  result?.best_variant?.score ??
  result?.best_variant?.scores ??
  {};

const getAttentionScore = (result) =>
  getScores(result)?.attention_coefficient ??
  result?.best_variant?.attention_coefficient ??
  0;

const getVariants = (result) =>
  Array.isArray(result?.variants) ? result.variants : [];

const getVariantText = (variant) =>
  variant?.content ?? variant?.text ?? "";

const getVariantScores = (variant) =>
  variant?.score ?? variant?.scores ?? {};

const getCriticDirectives = (result) =>
  Array.isArray(result?.critic_directives) ? result.critic_directives : [];

const getIterationHistory = (result) =>
  Array.isArray(result?.iteration_history) ? result.iteration_history : [];

const scoreEntries = (scores) =>
  Object.entries(scores || {}).filter(([, value]) => typeof value === "number");

export default function JobResult() {
  const { jobId } = useParams();
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(Boolean(jobId));
  const [error, setError] = useState("");
  const [bestVariantCopied, setBestVariantCopied] = useState(false);

  useEffect(() => {
    let active = true;

    const load = async () => {
      if (!jobId) {
        setError("Missing job ID.");
        setLoading(false);
        return;
      }

      try {
        setLoading(true);
        setError("");
        const data = await getJobResult(jobId);
        if (active) {
          setResult(data);
          updateJobInHistory(jobId, {
            status: data.status || "completed",
            attention_coefficient: getAttentionScore(data),
            best_variant: getBestVariantText(data),
            completed_at: new Date().toISOString()
          });
        }
      } catch (err) {
        if (active) setError(err.message || "API request failed");
      } finally {
        if (active) setLoading(false);
      }
    };

    load();
    return () => {
      active = false;
    };
  }, [jobId]);

  const bestText = getBestVariantText(result);

  useEffect(() => {
    if (!bestVariantCopied) return undefined;

    const timeoutId = window.setTimeout(() => setBestVariantCopied(false), 1600);
    return () => window.clearTimeout(timeoutId);
  }, [bestVariantCopied]);

  const copyBestVariant = async () => {
    if (!bestText) return;

    await navigator.clipboard?.writeText(bestText);
    setBestVariantCopied(true);
  };

  const scores = getScores(result);
  const attentionScore = getAttentionScore(result);
  const variants = getVariants(result);
  const criticDirectives = getCriticDirectives(result);
  const iterationHistory = getIterationHistory(result);
  const resultReady = Boolean(bestText || variants.length || scoreEntries(scores).length);
  const simulation = result?.best_variant?.simulation || result?.simulation || {};
  const sentiment = simulation?.sentiment || result?.sentiment || {};
  const emotions = simulation?.emotions || simulation?.emotion || result?.emotion || {};

  return (
    <>
      <PageHeader title="Optimization Result" description={`Result package for job ${jobId || "unknown"}.`} />

      {loading && (
        <Card>
          <p className="text-sm font-semibold text-slate-700">Loading job result...</p>
        </Card>
      )}

      {!loading && error && (
        <Card className="border-rose-300 bg-rose-50">
          <h2 className="text-lg font-black text-rose-700">Could not load job result</h2>
          <p className="mt-2 text-sm font-semibold text-rose-600">{error}</p>
        </Card>
      )}

      {!loading && !error && !result && (
        <Card>
          <p className="text-sm font-semibold text-slate-700">No result available yet.</p>
        </Card>
      )}

      {!loading && !error && result && !resultReady && (
        <Card>
          <p className="text-sm font-semibold text-slate-700">Result is not ready yet.</p>
        </Card>
      )}

      {!loading && !error && result && resultReady && (
        <div className="space-y-6">
          <Card>
            <div className="grid gap-4 md:grid-cols-3">
              <div>
                <p className="text-xs font-bold uppercase tracking-wide text-slate-500">Job ID</p>
                <p className="mt-1 break-all font-mono text-sm text-slate-900">{result?.job_id || jobId}</p>
              </div>
              <div>
                <p className="text-xs font-bold uppercase tracking-wide text-slate-500">Status</p>
                <Badge className="mt-1 border-slate-300 bg-slate-100/70 text-slate-700">{result?.status || "unknown"}</Badge>
              </div>
              <div>
                <p className="text-xs font-bold uppercase tracking-wide text-slate-500">Attention Coefficient</p>
                <p className="mt-1 text-2xl font-black text-slate-900">{Number(attentionScore || 0).toFixed(2)}</p>
              </div>
            </div>
          </Card>

          <Card>
            <div className="flex flex-wrap items-center justify-between gap-3">
              <h2 className="text-lg font-black text-slate-950">Best Variant</h2>
              <Button
                type="button"
                variant="ghost"
                className="min-h-10 px-3"
                title={bestVariantCopied ? "Copied best variant" : "Copy best variant"}
                aria-label={bestVariantCopied ? "Copied best variant" : "Copy best variant"}
                disabled={!bestText}
                onClick={copyBestVariant}
              >
                {bestVariantCopied ? <Check className="h-4 w-4" /> : <Clipboard className="h-4 w-4" />}
                <span className="hidden sm:inline">{bestVariantCopied ? "Copied" : "Copy"}</span>
              </Button>
            </div>
            <p className="mt-4 whitespace-pre-wrap text-lg font-semibold leading-8 text-slate-900">
              {bestText || "No best variant content returned."}
            </p>
          </Card>

          <Card>
            <h2 className="text-lg font-black text-slate-950">Score Breakdown</h2>
            {scoreEntries(scores).length ? (
              <div className="mt-4 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
                {scoreEntries(scores).map(([key, value]) => (
                  <div key={key} className="rounded-2xl border border-slate-300/80 bg-white/70 p-4">
                    <p className="text-xs font-bold uppercase tracking-wide text-slate-500">{labelize(key)}</p>
                    <p className="mt-1 text-xl font-black text-slate-900">{Number(value).toFixed(2)}</p>
                  </div>
                ))}
              </div>
            ) : (
              <p className="mt-3 text-sm font-semibold text-slate-600">No score breakdown available.</p>
            )}
          </Card>

          <Card>
            <h2 className="text-lg font-black text-slate-950">All Variants</h2>
            {variants.length ? (
              <div className="mt-4 grid gap-4">
                {variants.map((variant, index) => {
                  const variantScores = getVariantScores(variant);
                  return (
                    <div key={variant?.id || index} className="rounded-2xl border border-slate-300/80 bg-white/70 p-4">
                      <div className="flex flex-wrap items-center justify-between gap-3">
                        <h3 className="font-black text-slate-900">Variant {index + 1}</h3>
                        <Badge className="border-slate-300 bg-slate-100/70 text-slate-700">Iteration {variant?.iteration ?? "n/a"}</Badge>
                      </div>
                      <p className="mt-3 whitespace-pre-wrap text-sm leading-6 text-slate-700">{getVariantText(variant) || "No variant content returned."}</p>
                      {scoreEntries(variantScores).length > 0 && (
                        <div className="mt-3 flex flex-wrap gap-2">
                          {scoreEntries(variantScores).map(([key, value]) => (
                            <Badge key={key} className="border-slate-300 bg-slate-100/70 text-slate-700">
                              {labelize(key)}: {Number(value).toFixed(2)}
                            </Badge>
                          ))}
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            ) : (
              <p className="mt-3 text-sm font-semibold text-slate-600">No generated variants available.</p>
            )}
          </Card>

          <Card>
            <h2 className="text-lg font-black text-slate-950">Simulation Summary</h2>
            <div className="mt-4 grid gap-4 md:grid-cols-2">
              <div className="rounded-2xl border border-slate-300/80 bg-white/70 p-4">
                <p className="text-xs font-bold uppercase tracking-wide text-slate-500">Sentiment</p>
                <pre className="mt-2 overflow-auto whitespace-pre-wrap text-xs text-slate-700">{JSON.stringify(sentiment || {}, null, 2)}</pre>
              </div>
              <div className="rounded-2xl border border-slate-300/80 bg-white/70 p-4">
                <p className="text-xs font-bold uppercase tracking-wide text-slate-500">Emotions</p>
                <pre className="mt-2 overflow-auto whitespace-pre-wrap text-xs text-slate-700">{JSON.stringify(emotions || {}, null, 2)}</pre>
              </div>
            </div>
          </Card>

          <Card>
            <h2 className="text-lg font-black text-slate-950">Critic Directives</h2>
            {criticDirectives.length ? (
              <div className="mt-4 grid gap-3">
                {criticDirectives.map((directive, index) => (
                  <pre key={index} className="overflow-auto rounded-2xl border border-slate-300/80 bg-white/70 p-4 text-xs text-slate-700">{JSON.stringify(directive, null, 2)}</pre>
                ))}
              </div>
            ) : (
              <p className="mt-3 text-sm font-semibold text-slate-600">No critic feedback available.</p>
            )}
          </Card>

          <Card>
            <h2 className="text-lg font-black text-slate-950">Iteration History</h2>
            {iterationHistory.length ? (
              <div className="mt-4 grid gap-3">
                {iterationHistory.map((item, index) => (
                  <pre key={index} className="overflow-auto rounded-2xl border border-slate-300/80 bg-white/70 p-4 text-xs text-slate-700">{JSON.stringify(item, null, 2)}</pre>
                ))}
              </div>
            ) : (
              <p className="mt-3 text-sm font-semibold text-slate-600">No iteration history available.</p>
            )}
          </Card>
        </div>
      )}
    </>
  );
}
