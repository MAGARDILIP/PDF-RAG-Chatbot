import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { useState, useEffect } from "react";
import Sidebar from "./components/Sidebar";
import ChatPage from "./pages/ChatPage";
import UploadPage from "./pages/UploadPage";
import DashboardPage from "./pages/DashboardPage";
import LoginPage from "./pages/LoginPage";
import { getStoredUser, isAuthenticated } from "./api/api";

function App() {
  // Auth state — check localStorage on mount
  const [user, setUser] = useState(() => getStoredUser());

  // Handle successful login from LoginPage
  function handleLoginSuccess(userData) {
    setUser(userData);
  }

  // Check if user is logged in
  const loggedIn = user && isAuthenticated();

  return (
    <BrowserRouter>
      <Routes>
        {/* Login route — accessible without auth */}
        <Route
          path="/login"
          element={
            loggedIn ? (
              <Navigate to="/" replace />
            ) : (
              <LoginPage onLoginSuccess={handleLoginSuccess} />
            )
          }
        />

        {/* Protected routes — require auth */}
        <Route
          path="/*"
          element={
            loggedIn ? (
              <div className="flex h-screen">
                {/* Sidebar navigation (always visible) */}
                <Sidebar user={user} />

                {/* Main content area */}
                <main className="flex-1 overflow-hidden">
                  <Routes>
                    <Route path="/" element={<ChatPage />} />
                    <Route path="/upload" element={<UploadPage />} />
                    <Route path="/dashboard" element={<DashboardPage />} />
                    {/* Catch-all redirect to chat */}
                    <Route path="*" element={<Navigate to="/" replace />} />
                  </Routes>
                </main>
              </div>
            ) : (
              <Navigate to="/login" replace />
            )
          }
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
