import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { labelize } from "../../utils/scoreFormatter";

export default function EmotionBarChart({ emotion = {} }) {
  const source = Array.isArray(emotion.distribution)
    ? emotion.distribution
    : Object.entries(emotion).map(([label, score]) => ({ label, score }));
  const data = source
    .filter((item) => item && typeof item === "object")
    .map((item) => ({ name: labelize(item.label || item.name), value: Number(item.score ?? item.value ?? 0) }));
  if (!data.length) {
    return <div className="flex h-56 items-center justify-center rounded-2xl border border-dashed border-slate-300/80 bg-white/60 text-sm font-semibold text-[#777a91]">Emotion signals will appear here.</div>;
  }
  return (
    <div className="h-56 w-full">
      <ResponsiveContainer>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(148, 163, 184, 0.18)" />
          <XAxis dataKey="name" tick={{ fill: "#94a3b8", fontSize: 12 }} />
          <YAxis domain={[0, 1]} tick={{ fill: "#94a3b8", fontSize: 12 }} />
          <Tooltip />
          <Bar dataKey="value" fill="#64748b" radius={[8, 8, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
