import { CartesianGrid, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

export default function IterationLineChart({ history = [] }) {
  const data = history.map((item) => ({ ...item, best_score: item.best_score ?? item.score ?? 0 }));
  if (!data.length) {
    return <div className="flex h-64 items-center justify-center rounded-2xl border border-dashed border-slate-300/80 bg-white/60 text-sm font-semibold text-[#777a91]">Iteration history will appear after the backend returns loop data.</div>;
  }
  return (
    <div className="h-64 w-full">
      <ResponsiveContainer>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(148, 163, 184, 0.18)" />
          <XAxis dataKey="iteration" tick={{ fill: "#94a3b8", fontSize: 12 }} />
          <YAxis domain={[0, 100]} tick={{ fill: "#94a3b8", fontSize: 12 }} />
          <Tooltip />
          <Line type="monotone" dataKey="best_score" stroke="#475569" strokeWidth={3} dot={{ r: 4 }} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
