import { labelize } from "./scoreFormatter";

export const statusLabel = (status) => labelize(status || "unknown");
export const statusClass = (status) => {
  if (status === "completed") return "bg-slate-100 text-slate-800 border-slate-200";
  if (status === "failed" || status === "cancelled") return "bg-rose-100 text-rose-800 border-rose-200";
  if (status === "queued") return "bg-slate-100 text-slate-700 border-slate-200";
  return "bg-cyan-100 text-cyan-800 border-cyan-200";
};
