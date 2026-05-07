import EmotionBarChart from "../charts/EmotionBarChart";

export default function EmotionPanel({ emotion = {} }) {
  return (
    <div className="rounded-2xl border border-slate-300/80 bg-white/60 p-4">
      <h3 className="font-black text-[#343449]">Emotion Distribution</h3>
      <EmotionBarChart emotion={emotion} />
    </div>
  );
}
