import Button from "./Button";

export default function Modal({ open, title, children, onClose }) {
  if (!open) return null;
  return (
    <div className="fixed inset-0 z-50 grid place-items-center bg-[#343449]/30 p-4 backdrop-blur-sm">
      <div className="w-full max-w-lg rounded-2xl border border-slate-300/80 bg-[#f5f6f2]/95 p-5 text-[#54566f] shadow-2xl shadow-slate-900/15">
        <div className="mb-4 flex items-center justify-between gap-4">
          <h2 className="text-lg font-semibold text-[#343449]">{title}</h2>
          <Button variant="ghost" onClick={onClose}>Close</Button>
        </div>
        {children}
      </div>
    </div>
  );
}
