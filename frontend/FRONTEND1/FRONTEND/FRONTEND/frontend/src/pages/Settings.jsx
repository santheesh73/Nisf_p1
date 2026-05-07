import { CheckCircle, FlaskConical, RadioTower, RefreshCcw, Settings2 } from "lucide-react";
import { API_BASE_URL } from "../api/client";
import Badge from "../components/common/Badge";
import Button from "../components/common/Button";
import Card from "../components/common/Card";
import ErrorMessage from "../components/common/ErrorMessage";
import Loader from "../components/common/Loader";
import PageHeader from "../components/common/PageHeader";
import { useBackendHealth } from "../hooks/useBackendHealth";

export default function Settings() {
  const { health, online, loading, error, checkHealth } = useBackendHealth(0);
  return (
    <>
      <PageHeader title="Platform Settings" description="Configure engine parameters and persistent storage for NISF modules." />
      <div className="grid gap-6 xl:grid-cols-2">
        <Card>
          <h2 className="flex items-center gap-2 text-lg font-black text-slate-950"><Settings2 className="h-5 w-5 text-slate-600" /> Frontend Environment</h2>
          <dl className="mt-4 grid gap-3">
            {[
              ["API Endpoint", API_BASE_URL],
              ["Environment", import.meta.env.MODE],
              ["App Version", "v1.0 demo"],
            ].map(([label, value]) => (
              <div key={label} className="flex justify-between gap-4 rounded-2xl border border-slate-300/80 bg-white/60 px-4 py-3">
                <dt className="text-slate-500">{label}</dt>
                <dd className="break-all text-right font-semibold text-slate-900">{value}</dd>
              </div>
            ))}
            <div className="flex justify-between gap-4 rounded-2xl border border-slate-300/80 bg-white/60 px-4 py-3">
              <dt className="text-slate-500">Active Module</dt>
              <dd><Badge className="border-slate-300 bg-slate-100/70 text-slate-700">Text Engine v1</Badge></dd>
            </div>
          </dl>
        </Card>
        <Card>
          <div className="flex items-center justify-between gap-4">
            <h2 className="flex items-center gap-2 text-lg font-black text-slate-950"><RadioTower className="h-5 w-5 text-slate-600" /> Backend Health</h2>
            <Button variant="secondary" onClick={checkHealth}><RefreshCcw className="h-4 w-4" /> Refresh</Button>
          </div>
          <div className="mt-4">
            {loading ? <Loader label="Checking backend" /> : <Badge className={online ? "border-slate-300 bg-slate-100/70 text-slate-700" : "border-amber-300 bg-amber-100/70 text-amber-700"}>{online ? "Online" : "Offline"}</Badge>}
          </div>
          <ErrorMessage message={error} />
          <pre className="mt-4 max-h-64 overflow-auto rounded-2xl border border-slate-300/80 bg-white/70 p-4 text-xs text-[#54566f]">{JSON.stringify(health || {}, null, 2)}</pre>
        </Card>
      </div>
      <Card className="mt-6">
        <h2 className="mb-4 flex items-center gap-2 text-lg font-black text-slate-950"><FlaskConical className="h-5 w-5 text-slate-600" /> Feature Modules</h2>
        <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-5">
          {["Text Optimization", "Image Optimization", "Audio Optimization", "Video Optimization", "Multimodal Campaigns"].map((item, index) => (
            <div key={item} className="rounded-2xl border border-slate-300/80 bg-white/60 p-4 transition-all duration-200 hover:-translate-y-0.5 hover:border-slate-300 hover:bg-white">
              <CheckCircle className={`mb-3 h-5 w-5 ${index === 0 ? "text-slate-600" : "text-slate-400"}`} />
              <p className="font-bold text-slate-950">{item}</p>
              <Badge className={`mt-3 ${index === 0 ? "border-emerald-300 bg-emerald-100/70 text-emerald-700" : "border-slate-300/80 bg-white/70 text-[#777a91]"}`}>{index === 0 ? "Active" : "Coming Soon"}</Badge>
            </div>
          ))}
        </div>
      </Card>
    </>
  );
}
