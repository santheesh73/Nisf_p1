import { Outlet, useLocation } from "react-router-dom";
import Sidebar from "./Sidebar";
import Topbar from "./Topbar";
import Footer from "./Footer";

export default function AppLayout() {
  const { pathname } = useLocation();
  const showSidebar = pathname !== "/";

  return (
    <div className="min-h-screen bg-transparent">
      <div className="flex min-h-screen flex-1 flex-col">
        <Topbar />
        <main className={`flex-1 px-4 pt-3 md:px-6 md:pt-4 lg:px-8 ${showSidebar ? "pb-32" : "pb-10"}`}>
          <div className="mx-auto w-full max-w-7xl">
            <Outlet />
          </div>
        </main>
        <Footer />
      </div>
      {showSidebar && <Sidebar />}
    </div>
  );
}
