import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { Activity, Brain, LogIn, Moon, Sparkles, Sun, User } from "lucide-react";
import Badge from "../common/Badge";
import Button from "../common/Button";
import { useBackendHealth } from "../../hooks/useBackendHealth";
import { useAuth } from "../../context/AuthContext";

const getInitialTheme = () => {
  const savedTheme = window.localStorage.getItem("nisf-theme");
  if (savedTheme === "dark" || savedTheme === "light") return savedTheme;
  return window.matchMedia?.("(prefers-color-scheme: dark)").matches ? "dark" : "light";
};

export default function Topbar() {
  const { online } = useBackendHealth(30000);
  const { user, authEnabled } = useAuth();
  const [theme, setTheme] = useState(getInitialTheme);
  const isDark = theme === "dark";

  useEffect(() => {
    document.documentElement.dataset.theme = theme;
    window.localStorage.setItem("nisf-theme", theme);
  }, [theme]);

  const toggleTheme = () => setTheme((currentTheme) => (currentTheme === "dark" ? "light" : "dark"));

  return (
    <header className="sticky top-0 z-30 border-b border-slate-300/80 bg-[#f4f5f1]/92 shadow-sm backdrop-blur-xl">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between gap-4 px-4 lg:px-6">
      <Link to="/" className="flex min-w-0 items-center gap-3 transition-opacity hover:opacity-80">
        <div className="flex h-9 w-9 items-center justify-center bg-gradient-to-br from-slate-400 to-cyan-300 text-[#343449] shadow-lg shadow-slate-500/20 [clip-path:polygon(50%_0,100%_25%,100%_75%,50%_100%,0_75%,0_25%)]">
          <Brain className="h-5 w-5" />
        </div>
        <div className="min-w-0">
        <div className="flex items-center gap-2 text-sm font-black text-[#343449]">
          <Sparkles className="h-4 w-4 text-slate-500" /> NISF
        </div>
        <div className="hidden text-xs text-[#64677f] sm:block">Premium text optimization workspace</div>
        </div>
      </Link>

      <div className="flex items-center gap-2 text-sm">
        <Badge className="hidden border-slate-300 bg-slate-100/70 text-slate-700 sm:inline-flex">NISF</Badge>
        {!authEnabled && (
          <Badge className="hidden border-amber-300 bg-amber-100/80 text-amber-700 md:inline-flex">Auth Disabled / Local Mode</Badge>
        )}
        {user && (
          <span className="hidden max-w-[220px] items-center gap-2 truncate rounded-full border border-slate-300 bg-white/75 px-3 py-1.5 text-xs font-bold text-[#54566f] md:inline-flex">
            <User className="h-3.5 w-3.5 shrink-0" /> <span className="truncate">{user.name || user.email}</span>
          </span>
        )}
        <span className={`flex items-center gap-2 rounded-full border px-3 py-1.5 text-xs font-bold ${online ? "border-slate-300 bg-slate-100/70 text-slate-700" : "border-amber-300 bg-amber-100/80 text-amber-700"}`}>
          <Activity className="h-3.5 w-3.5" /> {online ? "Backend Online" : "Backend Offline"}
        </span>
        <Button
          type="button"
          variant="ghost"
          className="min-h-10 rounded-full border border-slate-300/80 bg-white/70 px-3"
          title={isDark ? "Switch to light theme" : "Switch to dark theme"}
          aria-label={isDark ? "Switch to light theme" : "Switch to dark theme"}
          onClick={toggleTheme}
        >
          {isDark ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
          <span className="hidden lg:inline">{isDark ? "Light" : "Dark"}</span>
        </Button>
        <Button
          as={Link}
          to="/login"
          variant="ghost"
          className="min-h-10 rounded-full border border-slate-300/80 bg-white/70 px-3"
          title="Log In"
          aria-label="Log In"
        >
          <LogIn className="h-4 w-4" />
          <span className="hidden lg:inline">Log In</span>
        </Button>
      </div>
      </div>
    </header>
  );
}
