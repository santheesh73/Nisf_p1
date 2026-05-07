export default function Loader({ label = "Loading" }) {
  return (
    <div className="inline-flex items-center gap-3 rounded-full border border-slate-300/80 bg-white/75 px-3 py-2 text-sm font-semibold text-[#54566f] shadow-sm">
      <span className="h-4 w-4 animate-spin rounded-full border-2 border-slate-200 border-t-slate-500" />
      <span>{label}</span>
    </div>
  );
}
