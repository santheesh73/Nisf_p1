export default function Textarea({ label, helper, error, className = "", ...props }) {
  return (
    <label className="block">
      {label && <span className="mb-2 block text-xs font-semibold text-[#4d4f68]">{label}</span>}
      <textarea className={`min-h-40 w-full resize-y rounded-xl border border-slate-300/80 bg-[#fbfcf8] px-4 py-3 text-sm leading-6 text-[#343449] shadow-sm outline-none transition-all placeholder:text-slate-400 hover:border-slate-400 focus:border-slate-400 focus:ring-4 focus:ring-slate-400/20 disabled:cursor-not-allowed disabled:bg-slate-100 disabled:text-slate-500 ${className}`} {...props} />
      {helper && !error && <span className="mt-2 block text-xs leading-5 text-[#777a91]">{helper}</span>}
      {error && <span className="mt-1.5 block text-xs font-medium text-rose-600">{error}</span>}
    </label>
  );
}
