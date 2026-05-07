import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Check, Clipboard, Clock3, Eye, Gauge, History as HistoryIcon, Trash2 } from "lucide-react";
import Badge from "../components/common/Badge";
import Button from "../components/common/Button";
import Card from "../components/common/Card";
import EmptyState from "../components/common/EmptyState";
import ErrorMessage from "../components/common/ErrorMessage";
import PageHeader from "../components/common/PageHeader";
import { getHistory as getBackendHistory } from "../api/historyApi";
import { clearJobHistory, getJobHistory } from "../utils/jobHistory";
import { formatDateTime } from "../utils/dateFormatter";
import { labelize } from "../utils/scoreFormatter";
import { statusClass, statusLabel } from "../utils/statusFormatter";

const previewText = (value = "", maxLength = 180) => {
  if (!value) return "";
  return value.length > maxLength ? `${value.slice(0, maxLength).trim()}...` : value;
};

export default function History() {
  const navigate = useNavigate();
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [source, setSource] = useState("backend");
  const [copiedJobId, setCopiedJobId] = useState("");

  useEffect(() => {
    let active = true;

    const loadHistory = async () => {
      try {
        setLoading(true);
        setError("");
        const data = await getBackendHistory();
        if (!active) return;
        setJobs(Array.isArray(data?.items) ? data.items : []);
        setSource("backend");
      } catch {
        if (!active) return;
        setJobs(getJobHistory());
        setSource("local");
        setError("Backend history is unavailable, showing local browser history.");
      } finally {
        if (active) setLoading(false);
      }
    };

    loadHistory();
    return () => {
      active = false;
    };
  }, []);

  useEffect(() => {
    if (!copiedJobId) return undefined;

    const timeoutId = window.setTimeout(() => setCopiedJobId(""), 1600);
    return () => window.clearTimeout(timeoutId);
  }, [copiedJobId]);

  const handleClearHistory = () => {
    clearJobHistory();
    setJobs([]);
  };

  const copyJobId = async (jobId) => {
    await navigator.clipboard?.writeText(jobId);
    setCopiedJobId(jobId);
  };

  return (
    <>
      <PageHeader
        title="History"
        description={source === "backend" ? "Recent optimization jobs from MongoDB." : "Recent optimization jobs saved in this browser."}
        actions={source === "local" && jobs.length ? (
          <Button type="button" variant="secondary" onClick={handleClearHistory}>
            <Trash2 className="h-4 w-4" /> Clear Local History
          </Button>
        ) : null}
      />
      <div className="mb-4">
        <Badge className={source === "backend" ? "border-emerald-300 bg-emerald-100/70 text-emerald-800" : "border-amber-300 bg-amber-100/80 text-amber-800"}>
          {source === "backend" ? "Backend History" : "Local Browser History"}
        </Badge>
      </div>
      <ErrorMessage message={error} />

      {loading ? (
        <EmptyState title="Loading History" message="Fetching recent optimization jobs." />
      ) : jobs.length ? (
        <div className="grid gap-4">
          {jobs.map((job) => {
            const copied = copiedJobId === job.job_id;
            const bestVariantPreview = previewText(job.best_variant_preview || job.best_variant);

            return (
              <Card key={job.job_id} className="space-y-4">
                <div className="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
                  <div className="min-w-0">
                    <div className="mb-3 flex flex-wrap items-center gap-2">
                      <Badge className={statusClass(job.status)}>{statusLabel(job.status)}</Badge>
                      {job.content_type && <Badge>{labelize(job.content_type)}</Badge>}
                      {job.tone && <Badge>{labelize(job.tone)}</Badge>}
                      {job.platform && <Badge>{labelize(job.platform)}</Badge>}
                      {Number.isFinite(Number(job.attention_coefficient)) && (
                        <Badge className="border-cyan-300 bg-cyan-100/70 text-cyan-800">
                          <Gauge className="h-3.5 w-3.5" /> Attention {Number(job.attention_coefficient).toFixed(2)}
                        </Badge>
                      )}
                    </div>
                    <h2 className="break-all font-mono text-sm font-black text-slate-950">{job.job_id}</h2>
                    <p className="mt-2 flex items-center gap-2 text-sm font-semibold text-slate-500">
                      <Clock3 className="h-4 w-4" />
                      {job.created_at ? formatDateTime(job.created_at) : "Created time unavailable"}
                    </p>
                  </div>

                  <div className="flex flex-wrap gap-2">
                    <Button as={Link} to={`/jobs/${job.job_id}/result`}>
                      <Eye className="h-4 w-4" /> View Result
                    </Button>
                    <Button as={Link} variant="secondary" to={`/jobs/${job.job_id}/progress`}>
                      <HistoryIcon className="h-4 w-4" /> View Progress
                    </Button>
                    <Button type="button" variant="ghost" className="px-3" title="Copy job ID" onClick={() => copyJobId(job.job_id)}>
                      {copied ? <Check className="h-4 w-4" /> : <Clipboard className="h-4 w-4" />}
                      <span className="hidden sm:inline">{copied ? "Copied" : "Copy Job ID"}</span>
                    </Button>
                  </div>
                </div>

                {job.brief && (
                  <div className="rounded-xl border border-slate-300/80 bg-white/60 p-4">
                    <p className="text-xs font-bold uppercase tracking-wide text-slate-500">Brief</p>
                    <p className="mt-2 text-sm leading-6 text-slate-700">{job.brief}</p>
                  </div>
                )}

                {bestVariantPreview && (
                  <div className="rounded-xl border border-slate-300/80 bg-white/60 p-4">
                    <p className="text-xs font-bold uppercase tracking-wide text-slate-500">Best Variant Preview</p>
                    <p className="mt-2 whitespace-pre-wrap text-sm leading-6 text-slate-700">{bestVariantPreview}</p>
                  </div>
                )}
              </Card>
            );
          })}
        </div>
      ) : (
        <EmptyState
          title="No optimization history yet"
          message="No optimization history yet. Start by generating and optimizing a variant."
          actionLabel="Go to Generate Text"
          onAction={() => navigate("/generate/text")}
        />
      )}
    </>
  );
}
