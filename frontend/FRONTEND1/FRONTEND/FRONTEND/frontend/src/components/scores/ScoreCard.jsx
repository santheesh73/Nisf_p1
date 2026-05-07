import { formatScore, labelize, scoreToneClass } from "../../utils/scoreFormatter";

export default function ScoreCard({ label, value }) {
  return (
    <div className={`rounded-2xl border p-4 shadow-sm transition-all duration-200 hover:-translate-y-0.5 ${scoreToneClass(value)}`}>
      <div className="text-xs font-semibold uppercase">{labelize(label)}</div>
      <div className="mt-2 text-3xl font-black">{formatScore(value)}</div>
      <div className="mt-3 h-1.5 overflow-hidden rounded-full bg-slate-200/80">
        <div className="h-full rounded-full bg-current" style={{ width: `${Math.max(0, Math.min(100, Number(value) || 0))}%` }} />
      </div>
    </div>
  );
}
