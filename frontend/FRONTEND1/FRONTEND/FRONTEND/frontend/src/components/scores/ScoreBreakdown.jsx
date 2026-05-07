import { SCORE_DIMENSIONS } from "../../utils/constants";
import ScoreCard from "./ScoreCard";

export default function ScoreBreakdown({ scores = {} }) {
  return (
    <div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
      {SCORE_DIMENSIONS.map((key) => <ScoreCard key={key} label={key} value={scores[key]} />)}
    </div>
  );
}
