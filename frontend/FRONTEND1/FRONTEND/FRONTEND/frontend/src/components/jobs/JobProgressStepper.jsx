import { JOB_STATUSES } from "../../utils/constants";
import { statusLabel } from "../../utils/statusFormatter";
import { CheckCircle, Circle, Loader2 } from "lucide-react";

export default function JobProgressStepper({ status }) {
  const activeIndex = Math.max(0, JOB_STATUSES.indexOf(status));
  const steps = JOB_STATUSES.filter((item) => !["failed", "cancelled"].includes(item));
  return (
    <div className="grid gap-3 md:grid-cols-3 xl:grid-cols-5">
      {steps.map((step, index) => {
        const done = index < activeIndex || status === "completed";
        const active = index === activeIndex && status !== "completed";
        return (
          <div key={step} className={`rounded-2xl border p-4 text-sm transition-all ${done ? "border-slate-300 bg-slate-100/70 text-slate-700" : active ? "border-slate-300 bg-white text-[#343449] shadow-sm shadow-slate-500/10" : "border-slate-300/80 bg-white/60 text-[#85889d]"}`}>
            <div className="mb-3 flex items-center justify-between">
              <span className="text-xs font-black uppercase tracking-wide">Step {index + 1}</span>
              {done ? <CheckCircle className="h-4 w-4" /> : active ? <Loader2 className="h-4 w-4 animate-spin" /> : <Circle className="h-4 w-4" />}
            </div>
            <div className="font-bold">{statusLabel(step)}</div>
          </div>
        );
      })}
    </div>
  );
}
