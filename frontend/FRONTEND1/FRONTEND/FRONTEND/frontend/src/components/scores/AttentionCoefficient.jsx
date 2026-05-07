import { formatScore, scoreToneClass } from "../../utils/scoreFormatter";

export default function AttentionCoefficient({ value }) {
  return (
    <div className={`rounded-2xl border p-6 text-center shadow-panel ${scoreToneClass(value)}`}>
      <div className="text-xs font-bold uppercase tracking-[0.18em]">Attention Coefficient</div>
      <div className="mt-3 text-6xl font-black tracking-tight">{formatScore(value)}</div>
      <div className="mt-1 text-xs">Composite performance signal</div>
      <div className="mt-5 h-2 overflow-hidden rounded-full bg-slate-200/80">
        <div className="h-full rounded-full bg-current transition-all duration-500" style={{ width: `${Math.max(0, Math.min(100, Number(value) || 0))}%` }} />
      </div>
    </div>
  );
}
