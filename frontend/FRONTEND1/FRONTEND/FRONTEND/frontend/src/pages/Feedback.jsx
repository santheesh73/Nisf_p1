import { useState } from "react";
import { BarChart3, Database, MousePointerClick, Send, TrendingUp } from "lucide-react";
import Badge from "../components/common/Badge";
import { submitFeedback } from "../api/feedbackApi";
import Button from "../components/common/Button";
import Card from "../components/common/Card";
import ErrorMessage from "../components/common/ErrorMessage";
import Input from "../components/common/Input";
import PageHeader from "../components/common/PageHeader";
import Select from "../components/common/Select";
import { PLATFORMS } from "../utils/constants";

const initialForm = {
  job_id: "",
  variant_id: "",
  platform: "website",
  impressions: "",
  clicks: "",
  likes: "",
  shares: "",
  conversions: "",
  ctr: "",
  conversion_rate: ""
};

export default function Feedback() {
  const [form, setForm] = useState(initialForm);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const update = (field, value) => setForm((prev) => ({ ...prev, [field]: value }));

  const submit = async (event) => {
    event.preventDefault();
    try {
      setLoading(true);
      setError("");
      setSuccess("");
      const numeric = ["impressions", "clicks", "likes", "shares", "conversions", "ctr", "conversion_rate"];
      const payload = { ...form };
      numeric.forEach((key) => { payload[key] = form[key] === "" ? 0 : Number(form[key]); });
      await submitFeedback(payload);
      setSuccess("Feedback submitted successfully.");
      setForm(initialForm);
    } catch (err) {
      setError(err.message || "Unable to submit feedback.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <PageHeader title="Feedback" description="Send performance outcomes back to NISF for future learning loops." />
      <form onSubmit={submit} className="grid gap-6 lg:grid-cols-2 xl:grid-cols-4">
        <Card className="space-y-4">
          <div className="flex items-center gap-3">
            <div className="flex h-11 w-11 items-center justify-center rounded-2xl border border-slate-300/70 bg-slate-100/70 text-slate-700"><Database className="h-5 w-5" /></div>
            <div><h2 className="font-black text-slate-950">Job Metadata</h2><p className="text-sm text-slate-500">Job and variant references.</p></div>
          </div>
          <Input label="Job ID" value={form.job_id} onChange={(e) => update("job_id", e.target.value)} required />
          <Input label="Variant ID" value={form.variant_id} onChange={(e) => update("variant_id", e.target.value)} required />
          <Select label="Platform" options={PLATFORMS} value={form.platform} onChange={(e) => update("platform", e.target.value)} />
        </Card>
        <Card className="space-y-4">
          <div className="flex items-center gap-3">
            <div className="flex h-11 w-11 items-center justify-center rounded-2xl border border-amber-300/70 bg-amber-100/70 text-amber-700"><BarChart3 className="h-5 w-5" /></div>
            <div><h2 className="font-black text-slate-950">Engagement Metrics</h2><p className="text-sm text-slate-500">Reach and interaction.</p></div>
          </div>
          <Input label="Impressions" type="number" step="any" value={form.impressions} onChange={(e) => update("impressions", e.target.value)} />
          <Input label="Clicks" type="number" step="any" value={form.clicks} onChange={(e) => update("clicks", e.target.value)} />
          <Input label="Likes" type="number" step="any" value={form.likes} onChange={(e) => update("likes", e.target.value)} />
          <Input label="Shares" type="number" step="any" value={form.shares} onChange={(e) => update("shares", e.target.value)} />
        </Card>
        <Card className="space-y-4">
          <div className="flex items-center gap-3">
            <div className="flex h-11 w-11 items-center justify-center rounded-2xl border border-slate-300/70 bg-slate-100/70 text-slate-700"><MousePointerClick className="h-5 w-5" /></div>
            <div><h2 className="font-black text-slate-950">Conversion Metrics</h2><p className="text-sm text-slate-500">Outcome quality signals.</p></div>
          </div>
          <Input label="Conversions" type="number" step="any" value={form.conversions} onChange={(e) => update("conversions", e.target.value)} />
          <Input label="CTR" type="number" step="any" value={form.ctr} onChange={(e) => update("ctr", e.target.value)} />
          <Input label="Conversion Rate" type="number" step="any" value={form.conversion_rate} onChange={(e) => update("conversion_rate", e.target.value)} />
        </Card>
        <Card className="space-y-4">
          <div className="flex items-center gap-3">
            <div className="flex h-11 w-11 items-center justify-center rounded-2xl border border-slate-300/80 bg-white/75 text-[#54566f]"><TrendingUp className="h-5 w-5" /></div>
            <div><h2 className="font-black text-slate-950">Submit</h2><p className="text-sm text-slate-500">Close the learning loop.</p></div>
          </div>
          <p className="text-sm leading-6 text-slate-500">Submit real campaign outcomes so future optimization workflows can compare generated variants against business results.</p>
          <Badge className="w-fit border-slate-300 bg-slate-100/70 text-slate-700">POST /api/v1/feedback</Badge>
          <ErrorMessage message={error} />
          {success && <div className="rounded-xl border border-slate-300 bg-slate-100/70 px-4 py-3 text-sm font-medium text-slate-700">{success}</div>}
          <Button type="submit" loading={loading} disabled={loading} className="w-full"><Send className="h-4 w-4" /> {loading ? "Submitting" : "Submit Feedback"}</Button>
        </Card>
      </form>
    </>
  );
}
