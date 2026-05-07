import Badge from "../common/Badge";
import { labelize } from "../../utils/scoreFormatter";

export default function CriticDirectiveCard({ directive }) {
  return (
    <div className="rounded-2xl border border-slate-300/80 bg-white/60 p-4 shadow-sm">
      <div className="flex flex-wrap items-center gap-2">
        <Badge className="border-slate-300 bg-slate-100/70 text-slate-700">{labelize(directive.target_dimension)}</Badge>
        <Badge className="border-amber-300 bg-amber-100/70 text-amber-700">{labelize(directive.priority)} priority</Badge>
        <Badge className="border-slate-300/80 bg-white/70 text-[#777a91]">{labelize(directive.risk_level)} risk</Badge>
      </div>
      <p className="mt-3 text-sm font-semibold text-[#343449]">{directive.issue}</p>
      <p className="mt-2 text-sm text-[#5d6078]">{directive.rewrite_instruction}</p>
    </div>
  );
}
