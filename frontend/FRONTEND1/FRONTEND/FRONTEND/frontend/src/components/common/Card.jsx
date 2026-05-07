export default function Card({ children, className = "" }) {
  return (
    <section
      className={`rounded-xl border border-slate-300/80 bg-[#f4f5f1]/92 p-6 text-[#343449] shadow-[0_1px_2px_rgba(49,51,67,0.05),0_18px_50px_rgba(49,51,67,0.08)] backdrop-blur-xl transition-all duration-200 [&_.bg-slate-50]:bg-[#ecefeb] [&_.bg-white]:bg-[#f8f9f5] [&_.bg-indigo-50]:bg-slate-100/60 [&_.bg-slate-50]:bg-slate-100/70 [&_.bg-amber-50]:bg-amber-100/70 [&_.bg-rose-50]:bg-rose-100/70 [&_.border-slate-200]:border-slate-300/70 [&_.border-indigo-200]:border-slate-300 [&_.border-slate-200]:border-slate-300 [&_.border-amber-200]:border-amber-300 [&_.border-rose-200]:border-rose-300 [&_.text-white]:text-[#343449] [&_.text-slate-950]:text-[#343449] [&_.text-slate-900]:text-[#3f4057] [&_.text-slate-800]:text-[#4d4f68] [&_.text-slate-700]:text-[#5b5d76] [&_.text-slate-600]:text-[#64677f] [&_.text-slate-500]:text-[#777a91] [&_.text-indigo-700]:text-slate-700 [&_.text-slate-700]:text-slate-700 [&_.text-amber-700]:text-amber-700 [&_.text-rose-700]:text-rose-700 ${className}`}
    >
      {children}
    </section>
  );
}
