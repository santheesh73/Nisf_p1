import Badge from "../common/Badge";

export default function SentimentPanel({ sentiment = {} }) {
  const label = sentiment.label || sentiment.sentiment || "Unknown";
  const rawConfidence = Number(sentiment.confidence ?? sentiment.score ?? 0);
  const confidence = rawConfidence > 1 ? rawConfidence / 100 : rawConfidence;
  return (
    <div className="rounded-2xl border border-slate-300/80 bg-white/60 p-4">
      <h3 className="font-black text-[#343449]">Sentiment</h3>
      <div className="mt-3 flex flex-wrap items-center gap-3">
        <Badge className="border-slate-300 bg-slate-100/70 text-slate-700">{label}</Badge>
        <span className="text-sm font-semibold text-[#777a91]">{Math.round(Number(confidence || 0) * 100)}% confidence</span>
      </div>
      <div className="mt-4 h-2 overflow-hidden rounded-full bg-slate-200/80">
        <div className="h-full rounded-full bg-slate-500" style={{ width: `${Math.max(0, Math.min(100, Number(confidence || 0) * 100))}%` }} />
      </div>
    </div>
  );
}
