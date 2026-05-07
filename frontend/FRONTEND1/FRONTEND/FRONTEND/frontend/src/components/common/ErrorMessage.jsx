import { AlertCircle } from "lucide-react";

export default function ErrorMessage({ message }) {
  if (!message) return null;
  return (
    <div className="flex items-start gap-3 rounded-2xl border border-rose-300 bg-rose-100/75 px-4 py-3 text-sm font-semibold text-rose-700 shadow-sm">
      <AlertCircle className="mt-0.5 h-4 w-4 shrink-0" />
      <span>{message}</span>
    </div>
  );
}
