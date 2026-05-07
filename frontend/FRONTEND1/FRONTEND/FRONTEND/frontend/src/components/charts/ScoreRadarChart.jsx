import { PolarAngleAxis, PolarGrid, PolarRadiusAxis, Radar, RadarChart, ResponsiveContainer, Tooltip } from "recharts";
import { SCORE_DIMENSIONS } from "../../utils/constants";
import { labelize } from "../../utils/scoreFormatter";

export default function ScoreRadarChart({ scores = {} }) {
  const data = SCORE_DIMENSIONS.map((key) => ({ dimension: labelize(key), score: Number(scores[key] || 0) }));
  return (
    <div className="h-72 w-full">
      <ResponsiveContainer>
        <RadarChart data={data}>
          <PolarGrid stroke="#e2e8f0" />
          <PolarAngleAxis dataKey="dimension" tick={{ fontSize: 11, fill: "#475569" }} />
          <PolarRadiusAxis angle={90} domain={[0, 100]} tick={{ fontSize: 10, fill: "#64748b" }} />
          <Radar dataKey="score" stroke="#4f46e5" fill="#4f46e5" fillOpacity={0.22} strokeWidth={2} />
          <Tooltip />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
}
