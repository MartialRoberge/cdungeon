import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { useAuthStore } from "./store";
import HUD from "./components/hud/HUD";
import AuthPage from "./pages/AuthPage";
import DungeonMapPage from "./pages/DungeonMapPage";
import ZonePage from "./pages/ZonePage";
import RoomPage from "./pages/RoomPage";
import ProfilePage from "./pages/ProfilePage";
import LeaderboardPage from "./pages/LeaderboardPage";
import MentorPage from "./pages/MentorPage";

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { token } = useAuthStore();
  if (!token) return <Navigate to="/auth" replace />;
  return <>{children}</>;
}

export default function App() {
  const { token } = useAuthStore();
  return (
    <BrowserRouter>
      <div className="scanline-overlay" />
      {token && <HUD />}
      <Routes>
        <Route path="/auth" element={token ? <Navigate to="/map" replace /> : <AuthPage />} />
        <Route path="/" element={<Navigate to={token ? "/map" : "/auth"} replace />} />
        <Route path="/map" element={<ProtectedRoute><DungeonMapPage /></ProtectedRoute>} />
        <Route path="/zone/:zoneNumber" element={<ProtectedRoute><ZonePage /></ProtectedRoute>} />
        <Route path="/room/:roomId" element={<ProtectedRoute><RoomPage /></ProtectedRoute>} />
        <Route path="/profile" element={<ProtectedRoute><ProfilePage /></ProtectedRoute>} />
        <Route path="/leaderboard" element={<ProtectedRoute><LeaderboardPage /></ProtectedRoute>} />
        <Route path="/mentor" element={<ProtectedRoute><MentorPage /></ProtectedRoute>} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
