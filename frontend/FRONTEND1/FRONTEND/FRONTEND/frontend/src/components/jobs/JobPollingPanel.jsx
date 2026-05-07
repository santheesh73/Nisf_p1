import Card from "../common/Card";
import Loader from "../common/Loader";
import Button from "../common/Button";
import JobStatusBadge from "./JobStatusBadge";

export default function JobPollingPanel({ jobId, status, loading, onViewResult }) {
  return (
    <Card>
      <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div>
          <p className="text-xs font-bold uppercase tracking-wide text-slate-500">Job ID</p>
          <p className="mt-1 break-all font-mono text-sm text-slate-900">{jobId}</p>
        </div>
        <JobStatusBadge status={status || "queued"} />
      </div>
      <div className="mt-5">{loading ? <Loader label="Polling optimization loop every 2 seconds" /> : <p className="text-sm text-slate-600">Polling stopped.</p>}</div>
      {status === "completed" && <Button className="mt-5" onClick={onViewResult}>View Result</Button>}
    </Card>
  );
}
