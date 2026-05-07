import ScoreBreakdown from "../scores/ScoreBreakdown";

const getVariantText = (variant) => variant?.content ?? variant?.text ?? "";
const getVariantScores = (variant) => variant?.score ?? variant?.scores ?? {};

export default function VariantCard({ variant, index }) {
  const text = getVariantText(variant);
  const scores = getVariantScores(variant);

  return (
    <article className="rounded-2xl border border-slate-300/80 bg-[#f5f6f2]/90 p-5 text-[#54566f] shadow-[0_18px_48px_rgba(49,51,67,0.10)] backdrop-blur-xl transition-all hover:-translate-y-1 hover:border-slate-300 hover:bg-[#fbfcf8] hover:shadow-md">
      <div className="mb-3 flex items-center justify-between">
        <h3 className="font-black text-[#343449]">Variant {index + 1}</h3>
        <span className="rounded-full border border-slate-300/80 bg-white/70 px-2.5 py-1 text-xs font-bold text-[#777a91]">Iteration {variant.iteration ?? "n/a"}</span>
      </div>
      <p className="mb-4 whitespace-pre-wrap text-sm leading-6 text-[#5d6078]">{text || "No variant content returned."}</p>
      <ScoreBreakdown scores={scores} />
    </article>
  );
}
