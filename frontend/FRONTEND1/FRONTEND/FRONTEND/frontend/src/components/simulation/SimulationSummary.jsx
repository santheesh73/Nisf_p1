import SentimentPanel from "./SentimentPanel";
import EmotionPanel from "./EmotionPanel";

export default function SimulationSummary({ simulation = {} }) {
  return (
    <div className="grid gap-4 lg:grid-cols-[0.8fr_1.2fr]">
      <SentimentPanel sentiment={simulation.sentiment} />
      <EmotionPanel emotion={simulation.emotion} />
    </div>
  );
}
