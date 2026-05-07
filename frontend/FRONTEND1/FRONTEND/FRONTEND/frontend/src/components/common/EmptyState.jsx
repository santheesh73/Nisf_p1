import { Sparkles } from "lucide-react";
import Button from "./Button";

export default function EmptyState({ title, message, actionLabel, onAction }) {
  return (
    <div className="rounded-2xl border border-dashed border-slate-300/80 bg-[#f2f4f0]/90 p-8 text-center text-[#54566f] shadow-[0_24px_70px_rgba(49,51,67,0.10)] backdrop-blur-xl">
      <div className="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-2xl bg-gradient-to-br from-slate-400 to-cyan-300 text-[#343449] shadow-lg shadow-slate-500/20">
        <Sparkles className="h-6 w-6" />
      </div>
      <h3 className="text-lg font-bold text-[#343449]">{title}</h3>
      <p className="mx-auto mt-2 max-w-xl text-sm leading-6 text-[#777a91]">{message}</p>
      {actionLabel && <Button className="mt-4" onClick={onAction}>{actionLabel}</Button>}
    </div>
  );
}
