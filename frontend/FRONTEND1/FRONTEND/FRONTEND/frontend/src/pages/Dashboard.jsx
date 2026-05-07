import { Link } from "react-router-dom";
import { Activity, ArrowRight, BarChart, Brain, Calendar, CheckCircle, Cloud, Code2, Cpu, Gauge, GitBranch, Heart, History, Layers, MessageSquare, Monitor, Network, RadioTower, Server, ShieldCheck, Sparkles, Terminal, Trophy, Wand2, Zap } from "lucide-react";
import Badge from "../components/common/Badge";
import Button from "../components/common/Button";
import Card from "../components/common/Card";
import Loader from "../components/common/Loader";
import { API_BASE_URL } from "../api/client";
import { useBackendHealth } from "../hooks/useBackendHealth";
import NeuralNetworkViz from "../components/common/NeuralNetworkViz";
import ParticleField from "../components/common/ParticleField";
import { useAuth } from "../context/AuthContext";

const pipelines = [
  ["Text Optimization", "Active", "bg-emerald-100 text-emerald-700 border-emerald-300 shadow-[0_0_12px_rgba(16,185,129,0.2)] font-bold"],
  ["Image Optimization", "Coming Soon", "bg-slate-100/70 text-slate-500 border-slate-300/80"],
  ["Audio Optimization", "Coming Soon", "bg-slate-100/70 text-slate-500 border-slate-300/80"],
  ["Video Optimization", "Coming Soon", "bg-slate-100/70 text-slate-500 border-slate-300/80"],
  ["Multimodal Campaign Engine", "Coming Soon", "bg-slate-100/70 text-slate-500 border-slate-300/80"]
];

export default function Dashboard() {
  const { isAuthenticated } = useAuth();
  const { health, online, loading, error } = useBackendHealth(30000);
  const stats = [
    { label: "Backend Status", value: loading ? "Checking" : online ? "Backend Online" : "Backend Offline", detail: online ? `API Base URL: ${API_BASE_URL}` : error || "Waiting for service", icon: RadioTower, tone: "slate" },
    { label: "Active Module", value: "NISF", detail: "Optimization, scoring, critique", icon: Brain, tone: "cyan" },
    { label: "Attention Baseline", value: "82.4", detail: "Placeholder analytics coefficient", icon: Gauge, tone: "amber" },
    { label: "Recent Jobs", value: "0", detail: "Ready for persistent history", icon: Activity, tone: "slate" }
  ];
  const toneClass = {
    slate: "bg-slate-100/70 text-slate-700 border-slate-300",
    cyan: "bg-cyan-100/70 text-cyan-800 border-cyan-300",
    amber: "bg-amber-100/70 text-amber-700 border-amber-300",
    muted: "bg-white/70 text-[#64677f] border-slate-300/80"
  };

  return (
    <div className="space-y-[50px]">
      <section className="relative overflow-hidden border border-slate-300/80 bg-[#f2f3ef]/90 shadow-[0_28px_90px_rgba(49,51,67,0.10)]">
        <ParticleField />
        <div className="pointer-events-none absolute inset-0 bg-[repeating-linear-gradient(118deg,rgba(86,89,112,0.08)_0_1px,transparent_1px_8px)] opacity-50" />
        <div className="dashboard-hero-decoration pointer-events-none absolute right-[-8rem] top-12 h-[30rem] w-[30rem] rounded-full border border-slate-300/70 opacity-70" />
        <div className="dashboard-hero-decoration mesh-orb pointer-events-none absolute right-[-5rem] top-16 h-[26rem] w-[26rem] rounded-full opacity-60" />
        <div className="dashboard-hero-decoration pointer-events-none absolute right-10 top-12 h-2 w-2 rounded-full bg-slate-400 shadow-[0_0_0_12px_rgba(52,235,167,0.14)]" />

        <div className="flex flex-col gap-10 px-8 pb-10 pt-8 lg:flex-row lg:items-center lg:justify-between lg:px-12">
          <div className="relative z-10 max-w-3xl">
            <p className="mb-3 text-[11px] font-black uppercase tracking-[0.25em] text-[#4a4b61]">Neuro Iterative Synthesis Framework</p>
            <Badge className="mb-4 border-slate-300 bg-slate-100/70 text-slate-800"><Sparkles className="h-3.5 w-3.5" /> Generative Pipeline Live</Badge>
            <h1 className="mt-4 max-w-4xl text-5xl font-black leading-[0.92] tracking-[-0.045em] text-[#4a4b61] md:text-7xl">
              Optimize Text with AI Precision
            </h1>
            <p className="mt-3 max-w-2xl text-lg leading-8 text-[#686b82]">
              Built for fast iteration, attention scoring, critic feedback, and export-ready marketing variants.
            </p>
            <div className="mt-5 flex flex-wrap gap-3">
              <Button as={Link} to={isAuthenticated ? "/generate/text" : "/login"} className="px-6">
                Start Optimization <ArrowRight className="h-4 w-4" />
              </Button>
              <Button as={Link} variant="secondary" to="/score" className="px-6">
                Learn More <Zap className="h-4 w-4" />
              </Button>
            </div>
          </div>
          
          <div className="group relative hidden h-[520px] w-full max-w-[670px] lg:block">
            <div className="absolute inset-0 transition-all duration-500">
              <NeuralNetworkViz />
            </div>
            {/* Optimized decorative elements */}
            <div className="absolute -bottom-10 -right-10 h-48 w-48 rounded-full bg-orange-500/5 blur-[40px] animate-pulse" />
            <div className="absolute -top-10 -left-10 h-48 w-48 rounded-full bg-purple-500/5 blur-[40px] animate-pulse" style={{ animationDelay: '1.5s' }} />
          </div>
        </div>
      </section>

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {stats.map((stat) => (
          <Card key={stat.label} className="relative overflow-hidden hover:-translate-y-1 hover:border-slate-400">
            <div className="absolute inset-x-0 top-0 h-1 bg-gradient-to-r from-transparent via-slate-400/80 to-transparent" />
            <div className="flex items-start justify-between gap-4">
              <div>
                <p className="mono-label text-[10px] uppercase text-slate-500/90 font-bold tracking-wider">{stat.label}</p>
                <p className="mt-3 text-3xl font-black tracking-[-0.03em] text-[#4a4b61]">{stat.value}</p>
                <p className="mt-1 min-h-8 text-sm text-[#777a91]">{stat.detail}</p>
              </div>
              <div className={`flex h-11 w-11 items-center justify-center border ${toneClass[stat.tone]}`}>
                <stat.icon className="h-5 w-5" />
              </div>
            </div>
          </Card>
        ))}
      </div>

      <Card className="relative overflow-hidden">
        <div className="tech-band pointer-events-none absolute inset-x-0 top-0 h-20 border-b border-slate-300/70" />
        <div className="relative mb-6 flex items-center justify-between gap-3">
          <div className="flex items-center gap-2">
            <Layers className="h-5 w-5 text-slate-600" />
            <h2 className="text-xl font-black tracking-[-0.03em] text-[#4a4b61]">Pipeline Modules</h2>
          </div>
          <Badge className="border-slate-300 bg-white/70 text-[#54566f]">NISF</Badge>
        </div>
        <div className="relative grid gap-3 md:grid-cols-2 xl:grid-cols-5">
          {pipelines.map(([title, status, cls]) => (
            <div key={title} className="group border border-slate-300/80 bg-white/70 p-5 text-[#54566f] transition-all duration-200 hover:-translate-y-1 hover:border-slate-300 hover:bg-[#fbfcf8]">
              {status === "Active" ? <CheckCircle className="mb-4 h-5 w-5 text-emerald-500" /> : <Wand2 className="mb-4 h-5 w-5 text-[#9aa0b5] transition group-hover:text-slate-600" />}
              <h3 className="text-sm font-bold text-[#343449]">{title}</h3>
              <Badge className={`mt-3 ${cls}`}>{status}</Badge>
            </div>
          ))}
        </div>
      </Card>

      <div className="grid gap-4 lg:grid-cols-3">
        {[
          [Code2, "Contract Safe", "Frontend styling changed without touching the API endpoint paths."],
          [GitBranch, "Loop Native", "The existing job polling and result routing remain intact."],
          [Cpu, "NISF", "The current optimization module stays active while future modules stay staged."]
        ].map(([Icon, title, detail]) => (
          <Card key={title} className="border-l-4 border-l-slate-400">
            <Icon className="mb-4 h-5 w-5 text-slate-500" />
            <h2 className="text-lg font-black tracking-[-0.02em] text-[#4a4b61]">{title}</h2>
            <p className="mt-2 text-sm leading-6 text-[#686b82]">{detail}</p>
          </Card>
        ))}
      </div>
    </div>
  );
}
