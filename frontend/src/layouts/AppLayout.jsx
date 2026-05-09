import { useEffect, useState } from "react";
import { Outlet, NavLink } from "react-router-dom";
import {
  LayoutDashboard,
  BookOpen,
  Layers,
  CircleHelp,
  CalendarDays,
  CheckSquare,
  Flame,
  Settings,
  LogOut,
  Moon,
  Sun,
} from "lucide-react";

import logo from "/src/assets/logo.png";

function AppLayout() {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [darkMode, setDarkMode] = useState(false);

  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add("dark");
    } else {
      document.documentElement.classList.remove("dark");
    }

    return () => {
      document.documentElement.classList.remove("dark");
    };
  }, [darkMode]);

  return (
    <div
      className={`h-screen overflow-hidden font-[Poppins] flex transition-colors ${
        darkMode ? "bg-[#0F172A] text-white" : "bg-[#F8FAFC] text-[#1E293B]"
      }`}
    >
      {!sidebarOpen && (
        <button
          onClick={() => setSidebarOpen(true)}
          className="fixed top-6 left-6 z-50 w-12 h-12 rounded-2xl bg-[#8B6CF6] text-white font-extrabold shadow-lg"
        >
          M
        </button>
      )}

      {sidebarOpen && (
        <aside
          className={`w-[250px] h-screen shrink-0 p-6 flex flex-col justify-between overflow-y-auto border-r transition-colors ${
            darkMode
              ? "bg-[#111827] border-slate-800"
              : "bg-white border-slate-100"
          }`}
        >
          <div>
            <button
              onClick={() => setSidebarOpen(false)}
              className="flex items-center gap-3 mb-5 text-left"
            >
              <div className="relative w-12 h-12 rounded-2xl bg-[#8B6CF6] flex items-center justify-center shadow-lg">
                <img src={logo} alt="Memora" className="w-8 h-8 object-contain" />
                <span className="absolute -right-1 -top-1 w-3 h-3 bg-yellow-400 rounded-full" />
              </div>

              <div>
                <h1 className={`font-extrabold text-xl ${darkMode ? "text-white" : "text-[#1E293B]"}`}>
                  Memora
                </h1>
                <p className="text-xs text-slate-400">Révise mieux chaque jour</p>
              </div>
            </button>

            <button
              onClick={() => setDarkMode((v) => !v)}
              className={`w-full mb-6 h-11 rounded-2xl font-bold flex items-center justify-center gap-2 transition ${
                darkMode
                  ? "bg-slate-800 text-white hover:bg-slate-700"
                  : "bg-[#8B6CF6]/10 text-[#8B6CF6] hover:bg-[#8B6CF6]/20"
              }`}
            >
              {darkMode ? <Sun size={18} /> : <Moon size={18} />}
              {darkMode ? "Mode clair" : "Mode sombre"}
            </button>

            <div
              className={`rounded-3xl p-4 mb-7 border ${
                darkMode
                  ? "bg-yellow-500/10 border-yellow-900/40"
                  : "bg-yellow-50 border-yellow-100"
              }`}
            >
              <div className="flex items-center gap-3">
                <div
                  className={`w-11 h-11 rounded-2xl flex items-center justify-center text-yellow-500 ${
                    darkMode ? "bg-yellow-500/20" : "bg-yellow-100"
                  }`}
                >
                  <Flame size={22} />
                </div>

                <div>
                  <p className={`text-sm font-semibold ${darkMode ? "text-slate-300" : "text-slate-500"}`}>
                    Série en cours
                  </p>
                  <h2 className={`font-extrabold text-lg ${darkMode ? "text-white" : "text-[#1E293B]"}`}>
                    12 jours
                  </h2>
                </div>
              </div>

              <div className="flex gap-1 mt-4">
                {[1, 2, 3, 4, 5, 6, 7].map((item) => (
                  <div
                    key={item}
                    className={`h-2 flex-1 rounded-full ${
                      item <= 5
                        ? "bg-yellow-400"
                        : darkMode
                        ? "bg-yellow-500/20"
                        : "bg-yellow-100"
                    }`}
                  />
                ))}
              </div>
            </div>

            <p className="text-xs font-extrabold text-slate-400 uppercase tracking-wider mb-3">
              Navigation
            </p>

            <nav className="space-y-2">
              <MenuItem darkMode={darkMode} to="/dashboard" icon={<LayoutDashboard size={20} />} label="Dashboard" />
              <MenuItem darkMode={darkMode} to="/courses" icon={<BookOpen size={20} />} label="Cours" />
              <MenuItem darkMode={darkMode} to="/flashcards" icon={<Layers size={20} />} label="Flashcards" />
              <MenuItem darkMode={darkMode} to="/quiz" icon={<CircleHelp size={20} />} label="Quiz" />
              <MenuItem darkMode={darkMode} to="/planning" icon={<CalendarDays size={20} />} label="Planning" />
              <MenuItem darkMode={darkMode} to="/todo" icon={<CheckSquare size={20} />} label="To-Do" />
            </nav>
          </div>

          <div className={`border-t pt-5 ${darkMode ? "border-slate-800" : "border-slate-100"}`}>
            <div className="flex items-center gap-3 mb-5">
              <div className="w-11 h-11 rounded-full bg-[#8B6CF6] text-white flex items-center justify-center font-bold">
                FC
              </div>

              <div className="flex-1">
                <h3 className={`font-bold text-sm ${darkMode ? "text-white" : "text-[#1E293B]"}`}>
                  Faiza
                </h3>
              </div>

              <Settings size={18} className="text-slate-400" />
            </div>

            <button className="flex items-center gap-2 text-slate-400 text-sm hover:text-[#8B6CF6]">
              <LogOut size={18} />
              Se déconnecter
            </button>
          </div>
        </aside>
      )}

      <main
        className={`flex-1 min-w-0 h-screen overflow-y-auto transition-colors ${
          darkMode ? "bg-[#0F172A]" : "bg-[#F8FAFC]"
        }`}
      >
        <Outlet />
      </main>
    </div>
  );
}

function MenuItem({ to, icon, label, darkMode }) {
  return (
    <NavLink
      to={to}
      className={({ isActive }) =>
        `flex items-center gap-3 rounded-2xl px-4 py-3 font-bold transition ${
          isActive
            ? "bg-[#8B6CF6]/15 text-[#8B6CF6]"
            : darkMode
            ? "text-slate-300 hover:bg-slate-800"
            : "text-slate-500 hover:bg-slate-50"
        }`
      }
    >
      {icon}
      <span>{label}</span>
    </NavLink>
  );
}

export default AppLayout;