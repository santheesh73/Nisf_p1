import { Routes, Route } from "react-router-dom";
import AppLayout from "../components/layout/AppLayout.jsx";
import ProtectedRoute from "../components/auth/ProtectedRoute.jsx";

import Dashboard from "../pages/Dashboard.jsx";
import GenerateText from "../pages/GenerateText.jsx";
import OptimizeText from "../pages/OptimizeText.jsx";
import JobProgress from "../pages/JobProgress.jsx";
import JobResult from "../pages/JobResult.jsx";
import ScoreOnly from "../pages/ScoreOnly.jsx";
import Templates from "../pages/Templates.jsx";
import Feedback from "../pages/Feedback.jsx";
import Settings from "../pages/Settings.jsx";
import History from "../pages/History.jsx";
import Login from "../pages/Login.jsx";
import Register from "../pages/Register.jsx";
import NotFound from "../pages/NotFound.jsx";

export default function AppRoutes() {
  return (
    <Routes>
      <Route element={<AppLayout />}>
        <Route path="/" element={<Dashboard />} />
      </Route>

      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />

      <Route element={<ProtectedRoute />}>
        <Route element={<AppLayout />}>
          <Route path="/generate/text" element={<GenerateText />} />
          <Route path="/optimize/text" element={<OptimizeText />} />
          <Route path="/jobs/:jobId/progress" element={<JobProgress />} />
          <Route path="/jobs/:jobId/result" element={<JobResult />} />
          <Route path="/score" element={<ScoreOnly />} />
          <Route path="/templates" element={<Templates />} />
          <Route path="/feedback" element={<Feedback />} />
          <Route path="/history" element={<History />} />
          <Route path="/settings" element={<Settings />} />
        </Route>
      </Route>

      <Route path="*" element={<NotFound />} />
    </Routes>
  );
}
