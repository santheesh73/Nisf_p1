import { useEffect } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { ArrowRight, CheckCircle2, Clock, Cpu, MessageSquare, RadioTower, XCircle } from "lucide-react";
import Badge from "../components/common/Badge";
import Button from "../components/common/Button";
import Card from "../components/common/Card";
import Loader from "../components/common/Loader";
import PageHeader from "../components/common/PageHeader";
import JobErrorPanel from "../components/jobs/JobErrorPanel";
import JobProgressStepper from "../components/jobs/JobProgressStepper";
import JobStatusBadge from "../components/jobs/JobStatusBadge";
import { useJobStatus } from "../hooks/useJobStatus";
import { updateJobInHistory } from "../utils/jobHistory";

export default function JobProgress() {
  const { jobId } = useParams();
  const navigate = useNavigate();
  const { status, loading, error, timedOut } = useJobStatus(jobId);
  const currentStatus = status || "queued";
  const completed = currentStatus === "completed";

  useEffect(() => {
    if (!jobId || !status) return;

    updateJobInHistory(jobId, {
      status,
      ...(status === "completed" ? { completed_at: new Date().toISOString() } : {})
    });
  }, [jobId, status]);

  useEffect(() => {
    if (status !== "completed" || !jobId) return undefined;
    const timer = setTimeout(() => navigate(`/jobs/${jobId}/result`), 2000);
    return () => clearTimeout(timer);
  }, [jobId, navigate, status]);

  if (status === "failed" || status === "cancelled" || timedOut) {
    return (
      <div className="space-y-6">
        <PageHeader title="Optimization Progress" description={`Job ${jobId || "unknown"} could not complete.`} />
        <JobErrorPanel status={status || "timed_out"} message={error || "Optimization timed out. Please return to Generate Text and try again."} />
        <div className="flex flex-wrap gap-3">
          <Button as={Link} to="/generate/text">Back to Generate Text</Button>
          {jobId && status && !timedOut && <Button as={Link} variant="secondary" to={`/jobs/${jobId}/result`}>View Current Result <ArrowRight className="h-4 w-4" /></Button>}
        </div>
      </div>
    );
  }

  return (
    <>
      <PageHeader title="Optimization Progress" description={`Job ${jobId || "unknown"} is moving through the NISF synthesis loop.`} />
      <div className="space-y-6">
        <Card className={`overflow-hidden ${completed ? "border-slate-300 bg-slate-100/60" : "border-slate-300/80 bg-[#f2f4f0]/90"}`}>
          <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
            <div className="flex items-start gap-4">
              <div className={`flex h-14 w-14 items-center justify-center rounded-2xl ${completed ? "bg-slate-400 text-[#343449]" : "bg-white text-slate-700 ring-1 ring-slate-300"} shadow-lg shadow-slate-900/10`}>
                {completed ? <CheckCircle2 className="h-7 w-7" /> : <Cpu className="h-7 w-7" />}
              </div>
              <div>
              <p className="text-xs font-bold uppercase tracking-wide text-slate-500">Current Status</p>
              <div className="mt-2 flex flex-wrap items-center gap-3">
                <JobStatusBadge status={currentStatus} />
                {loading && <Loader label="Polling every 2 seconds" />}
              </div>
              <p className="mt-3 max-w-2xl text-sm leading-6 text-slate-600">
                {completed ? "The optimization loop completed successfully. The result view is ready." : "NISF is moving through generation, simulation, scoring, critic review, and safety checks."}
              </p>
              </div>
            </div>
            {completed && (
              <div className="flex flex-wrap gap-3">
                <Button as={Link} to={`/jobs/${jobId}/result`}>View Result <ArrowRight className="h-4 w-4" /></Button>
                <Button as={Link} variant="secondary" to="/feedback"><MessageSquare className="h-4 w-4" /> Feedback</Button>
              </div>
            )}
          </div>
          <div className="mt-6">
            <JobProgressStepper status={currentStatus} />
          </div>
        </Card>
        <div className="grid gap-4 lg:grid-cols-4">
          <Card>
            <div className="mb-3 flex h-11 w-11 items-center justify-center rounded-2xl border border-slate-300/70 bg-slate-100/70 text-slate-700"><Cpu className="h-5 w-5" /></div>
            <h2 className="font-black text-slate-950">Optimization Loop</h2>
            <p className="mt-2 text-sm leading-6 text-slate-500">NISF generates variants, simulates response signals, scores candidates, and applies critic feedback until completion.</p>
          </Card>
          <Card>
            <div className="mb-3 flex h-11 w-11 items-center justify-center rounded-2xl border border-slate-300/70 bg-slate-100/70 text-slate-700"><RadioTower className="h-5 w-5" /></div>
            <h2 className="font-black text-slate-950">Polling</h2>
            <p className="mt-2 text-sm leading-6 text-slate-500">The frontend keeps checking job status without changing endpoint paths or request contracts.</p>
          </Card>
          <Card className="lg:col-span-2">
            <div className="mb-3 flex h-11 w-11 items-center justify-center rounded-2xl border border-amber-300/70 bg-amber-100/70 text-amber-700"><Clock className="h-5 w-5" /></div>
            <h2 className="font-black text-slate-950">Job Reference</h2>
            <p className="mt-2 break-all font-mono text-xs text-slate-600">{jobId || "unknown"}</p>
            <Badge className="mt-3 border-slate-300/80 bg-white/70 text-[#777a91]">Auto-routes when completed</Badge>
          </Card>
        </div>
        {error && (
          <Card className="border-rose-300 bg-rose-100/70">
            <div className="flex items-start gap-3 text-rose-700">
              <XCircle className="mt-0.5 h-5 w-5" />
              <div>
                <h2 className="font-black">Progress Warning</h2>
                <p className="mt-1 text-sm leading-6">{error}</p>
              </div>
            </div>
          </Card>
        )}
      </div>
    </>
  );
}
