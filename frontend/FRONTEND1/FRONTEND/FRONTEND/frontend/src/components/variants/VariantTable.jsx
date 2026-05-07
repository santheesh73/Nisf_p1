import { formatScore } from "../../utils/scoreFormatter";

const getVariantScores = (variant) => variant?.score ?? variant?.scores ?? {};

export default function VariantTable({ variants = [] }) {
  if (!variants.length) {
    return <div className="rounded-2xl border border-dashed border-slate-300/80 bg-white/60 p-6 text-center text-sm font-semibold text-[#777a91]">Variant rows will appear after optimization.</div>;
  }
  return (
    <div className="overflow-x-auto rounded-2xl border border-slate-300/80 shadow-sm">
      <table className="min-w-full divide-y divide-slate-200 text-sm text-[#54566f]">
        <thead className="bg-[#eef1ee] text-left text-xs uppercase tracking-wide text-[#777a91]">
          <tr><th className="px-3 py-3">Variant</th><th className="px-3 py-3">Iteration</th><th className="px-3 py-3">Attention</th><th className="px-3 py-3">Sentiment</th></tr>
        </thead>
        <tbody className="divide-y divide-slate-200 bg-white/60">
          {variants.map((variant, index) => {
            const scores = getVariantScores(variant);
            return (
              <tr key={variant.id || index} className="hover:bg-slate-50/70">
                <td className="px-3 py-3 font-semibold text-[#343449]">Variant {index + 1}</td>
                <td className="px-3 py-3">{variant.iteration ?? "n/a"}</td>
                <td className="px-3 py-3">{formatScore(scores.attention_coefficient || scores.composite)}</td>
                <td className="px-3 py-3">{variant.simulation?.sentiment?.label || "n/a"}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
