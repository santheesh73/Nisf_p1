import { Bar, BarChart, CartesianGrid, Legend, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

export default function ScoreComparisonChart({ variants = [] }) {
  const data = variants.map((variant, index) => {
    const scores = variant.scores || variant.score || {};
    return {
      name: `V${index + 1}`,
      attention: scores.attention_coefficient || scores.composite || variant.attention_coefficient || 0,
      clarity: scores.clarity || 0,
      engagement: scores.engagement || 0
    };
  });
  if (!data.length) {
    return <div className="flex h-72 items-center justify-center rounded-2xl border border-dashed border-slate-300/80 bg-white/60 text-sm font-semibold text-[#777a91]">Variant comparison data will appear after optimization.</div>;
  }
  return (
    <div className="h-72 w-full">
      <ResponsiveContainer>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(148, 163, 184, 0.18)" />
          <XAxis dataKey="name" tick={{ fill: "#94a3b8", fontSize: 12 }} />
          <YAxis domain={[0, 100]} tick={{ fill: "#94a3b8", fontSize: 12 }} />
          <Tooltip />
          <Legend />
          <Bar dataKey="attention" fill="#64748b" radius={[8, 8, 0, 0]} />
          <Bar dataKey="clarity" fill="#475569" radius={[6, 6, 0, 0]} />
          <Bar dataKey="engagement" fill="#d97706" radius={[6, 6, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
