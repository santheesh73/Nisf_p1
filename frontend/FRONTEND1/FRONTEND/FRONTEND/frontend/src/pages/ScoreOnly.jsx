import { useState } from "react";
import { Activity, Gauge, ScanSearch, ShieldCheck, SlidersHorizontal } from "lucide-react";
import Badge from "../components/common/Badge";
import { scoreText } from "../api/scoreApi";
import Button from "../components/common/Button";
import Card from "../components/common/Card";
import ErrorMessage from "../components/common/ErrorMessage";
import Input from "../components/common/Input";
import PageHeader from "../components/common/PageHeader";
import Select from "../components/common/Select";
import Textarea from "../components/common/Textarea";
import EmotionBarChart from "../components/charts/EmotionBarChart";
import SentimentPanel from "../components/simulation/SentimentPanel";
import AttentionCoefficient from "../components/scores/AttentionCoefficient";
import ScoreBreakdown from "../components/scores/ScoreBreakdown";
import { CONTENT_TYPES, PLATFORMS, TONES } from "../utils/constants";
import { parseBrandTerms } from "../utils/apiPayload";

const initialForm = {
  text: "Upgrade every scroll, shot, and stream with an AI-powered smartphone built for fast-moving professionals. Discover smarter mobile performance today.",
  content_type: "ad_copy",
  tone: "persuasive",
  platform: "instagram",
  brand_terms: "AI-powered, smartphone, mobile experience"
};

export default function ScoreOnly() {
  const [form, setForm] = useState(initialForm);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const submit = async (event) => {
    event.preventDefault();
    if (!form.text.trim()) {
      setError("Input text is required.");
      return;
    }
    try {
      setLoading(true);
      setError("");
      const data = await scoreText({
        text: form.text,
        content_type: form.content_type,
        tone: form.tone,
        platform: form.platform,
        brand_terms: parseBrandTerms(form.brand_terms)
      });
      setResult(data);
    } catch (err) {
      setError(err.message || "Unable to score text.");
    } finally {
      setLoading(false);
    }
  };

  const scores = result?.scores || result?.score_breakdown || result || {};
  const attention = result?.attention_coefficient || scores?.attention_coefficient;
  const sentiment = result?.sentiment || result?.simulation?.sentiment || {};
  const emotion = result?.emotion || result?.simulation?.emotion || {};

  return (
    <>
      <PageHeader title="Score Only" description="Evaluate text without launching a full optimization loop." />
      <div className="grid gap-6 xl:grid-cols-[0.9fr_1.1fr]">
        <form onSubmit={submit} className="space-y-6">
          <Card className="space-y-6">
            <div className="flex items-center gap-3">
              <div className="flex h-11 w-11 items-center justify-center rounded-2xl border border-slate-300/70 bg-slate-100/70 text-slate-700"><ScanSearch className="h-5 w-5" /></div>
              <div>
                <h2 className="text-lg font-black text-slate-950">Text Input & Configuration</h2>
                <p className="text-sm text-slate-500">Run an AI scoring pass with the approved schema.</p>
              </div>
            </div>
            
            <Textarea label="Input Text" helper="Sent as text to the backend score API." value={form.text} onChange={(e) => setForm({ ...form, text: e.target.value })} placeholder="Paste text to score..." className="min-h-40" />
            <Input label="Brand Terms" helper="Comma-separated here, sent as an array to the backend." value={form.brand_terms} onChange={(e) => setForm({ ...form, brand_terms: e.target.value })} />
            
            <div className="grid gap-4 sm:grid-cols-3">
              <Select label="Content Type" options={CONTENT_TYPES} value={form.content_type} onChange={(e) => setForm({ ...form, content_type: e.target.value })} />
              <Select label="Tone" options={TONES} value={form.tone} onChange={(e) => setForm({ ...form, tone: e.target.value })} />
              <Select label="Platform" options={PLATFORMS} value={form.platform} onChange={(e) => setForm({ ...form, platform: e.target.value })} />
            </div>

            <ErrorMessage message={error} />
            <Button type="submit" loading={loading} disabled={loading} className="w-full"><Gauge className="h-4 w-4" /> {loading ? "Scoring" : "Score Text"}</Button>
          </Card>
        </form>
        <div className="space-y-6">
          {result ? (
            <>
              <AttentionCoefficient value={attention} />
              <Card><div className="mb-4 flex items-center justify-between"><h2 className="text-lg font-black">Score Breakdown</h2><Badge className="border-slate-300 bg-slate-100/70 text-slate-700"><Activity className="h-3.5 w-3.5" /> Analysis</Badge></div><ScoreBreakdown scores={scores} /></Card>
              <div className="grid gap-6 lg:grid-cols-2">
                <Card><h2 className="mb-4 text-lg font-black">Sentiment</h2><SentimentPanel sentiment={sentiment} /></Card>
                <Card><h2 className="mb-4 text-lg font-black">Emotion</h2><EmotionBarChart emotion={emotion} /></Card>
              </div>
              <Card>
                <h2 className="mb-3 flex items-center gap-2 text-lg font-black"><ShieldCheck className="h-5 w-5 text-slate-600" /> Safety Status</h2>
                <Badge className="border-slate-300 bg-slate-100/70 text-slate-700">{result?.safety_status || result?.safety?.status || "No safety issue reported"}</Badge>
              </Card>
            </>
          ) : (
            <Card className="py-12"><div className="flex flex-col items-center justify-center text-center"><Gauge className="mb-4 h-10 w-10 text-slate-600" /><h2 className="text-lg font-black text-[#343449]">Ready to Analyze</h2><p className="mt-2 max-w-md text-sm leading-6 text-[#777a91]">Submit text to see attention, score, sentiment, emotion, and safety signals in a clean analysis panel.</p></div></Card>
          )}
        </div>
      </div>
    </>
  );
}
