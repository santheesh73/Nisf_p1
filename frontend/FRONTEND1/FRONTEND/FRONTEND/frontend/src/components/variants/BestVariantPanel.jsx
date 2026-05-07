import Card from "../common/Card";
import AttentionCoefficient from "../scores/AttentionCoefficient";

export default function BestVariantPanel({ variant }) {
  return (
    <Card>
      <div className="grid gap-5 lg:grid-cols-[1fr_260px]">
        <div>
          <p className="text-xs font-bold uppercase tracking-[0.18em] text-slate-700">Best Optimized Text</p>
          <p className="mt-3 whitespace-pre-wrap text-lg leading-8 text-[#343449]">{variant?.text || "No optimized text returned."}</p>
          <p className="mt-4 text-sm text-[#777a91]">Iteration {variant?.iteration || "n/a"}</p>
        </div>
        <AttentionCoefficient value={variant?.attention_coefficient} />
      </div>
    </Card>
  );
}
