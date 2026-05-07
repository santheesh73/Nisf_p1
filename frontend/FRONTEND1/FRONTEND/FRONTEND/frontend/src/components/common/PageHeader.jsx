export default function PageHeader({ title, eyebrow = "NISF", description, actions }) {
  return (
    <div className="relative mb-8 flex flex-col gap-4 overflow-hidden border border-slate-300/80 bg-[#f4f5f1]/90 p-6 text-[#343449] shadow-[0_1px_2px_rgba(49,51,67,0.05),0_18px_50px_rgba(49,51,67,0.08)] backdrop-blur-xl md:flex-row md:items-end md:justify-between">
      <div className="tech-band pointer-events-none absolute inset-x-0 top-0 h-20 border-b border-slate-300/70" />
      <div className="relative">

        <h1 className="mt-3 text-3xl font-black tracking-[-0.035em] text-[#4a4b61] md:text-4xl">{title}</h1>
        {description && <p className="mt-3 max-w-3xl text-sm leading-6 text-[#64677f]">{description}</p>}
      </div>
      {actions && <div className="relative flex flex-wrap gap-2">{actions}</div>}
    </div>
  );
}
