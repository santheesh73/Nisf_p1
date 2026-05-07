import { NavLink } from "react-router-dom";

const links = [
  { to: "/", label: "Dashboard" },
  { to: "/generate/text", label: "Generate Text" },
  { to: "/score", label: "Score Only" },
  { to: "/templates", label: "Templates" },
  { to: "/history", label: "History" },
  { to: "/settings", label: "Settings" }
];

export default function Sidebar() {
  return (
    <aside className="fixed inset-x-0 bottom-6 z-50 px-4">
      <div className="relative mx-auto flex w-full max-w-fit items-center justify-center rounded-2xl bg-[#2a2a2a] p-1.5 shadow-2xl ring-1 ring-white/10">
        <nav className="flex items-center gap-1.5 overflow-x-auto hide-scrollbar">
          {links.map(({ to, label }) => (
            <NavLink
              key={to}
              to={to}
              className={({ isActive }) => `shrink-0 rounded-xl border px-5 py-2.5 text-sm tracking-wide transition-all ${isActive ? "border-white/80 text-white" : "border-white/10 text-white/70 hover:border-white/30 hover:text-white hover:bg-white/5"}`}
            >
              {label}
            </NavLink>
          ))}
        </nav>
      </div>
    </aside>
  );
}
