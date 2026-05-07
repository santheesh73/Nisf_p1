import { Loader2 } from "lucide-react";

export default function Button({ children, as: Component = "button", variant = "primary", className = "", disabled = false, loading = false, ...props }) {
  const variants = {
    primary: "cut-corners bg-[#2f3044] !text-white shadow-lg shadow-slate-900/15 hover:-translate-y-0.5 hover:bg-[#222337] hover:shadow-xl active:translate-y-0",
    secondary: "rounded-xl border border-slate-400/80 bg-[#f2f3ef]/85 text-[#343449] shadow-sm shadow-slate-900/5 hover:-translate-y-0.5 hover:border-slate-300 hover:bg-white hover:text-slate-800",
    ghost: "rounded-xl text-[#54566f] hover:bg-white/70 hover:text-[#343449]",
    success: "bg-slate-600 !text-white shadow-sm shadow-slate-600/20 hover:-translate-y-0.5 hover:bg-slate-700",
    danger: "bg-rose-600 !text-white shadow-sm shadow-rose-600/20 hover:-translate-y-0.5 hover:bg-rose-700"
  };
  const isDisabled = disabled || loading;
  const disabledProps = Component === "button" ? { disabled: isDisabled } : { "aria-disabled": isDisabled };
  return (
    <Component
      className={`inline-flex min-h-11 items-center justify-center gap-2 px-4 py-2.5 text-sm font-semibold outline-none transition-all duration-200 focus-visible:ring-4 focus-visible:ring-slate-400/25 disabled:cursor-not-allowed disabled:translate-y-0 disabled:opacity-50 ${variants[variant]} ${className}`}
      {...disabledProps}
      {...props}
    >
      {loading && <Loader2 className="h-4 w-4 animate-spin" />}
      {children}
    </Component>
  );
}
