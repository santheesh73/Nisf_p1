export default function Badge({ children, className = "" }) {
  return <span className={`inline-flex items-center gap-1.5 rounded-full border border-slate-300/70 bg-[#f5f6f2]/80 px-3 py-1.5 text-xs font-bold leading-none text-[#4d4f68] shadow-sm ${className}`}>{children}</span>;
}
