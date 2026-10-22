import { useState } from "react";
import { IoShieldCheckmark, IoSchool, IoLockClosed } from "react-icons/io5";
import { loginWithGoogle } from "../api/api";

// Google Client ID from environment variables
const GOOGLE_CLIENT_ID = import.meta.env.VITE_GOOGLE_CLIENT_ID;

function LoginPage({ onLoginSuccess }) {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  // Initialize Google Sign-In and trigger the popup
  function handleGoogleLogin() {
    setIsLoading(true);
    setError(null);

    // Use Google Identity Services (GIS) to show the sign-in popup
    window.google.accounts.id.initialize({
      client_id: GOOGLE_CLIENT_ID,
      callback: handleGoogleCallback,
      auto_select: false,
    });

    // Trigger the Google sign-in prompt
    window.google.accounts.id.prompt((notification) => {
      if (notification.isNotDisplayed() || notification.isSkippedMoment()) {
        // If One Tap is blocked by browser, render a hidden Google button and click it
        const buttonDiv = document.createElement("div");
        buttonDiv.id = "google-btn-hidden";
        buttonDiv.style.position = "fixed";
        buttonDiv.style.top = "-9999px";
        document.body.appendChild(buttonDiv);

        window.google.accounts.id.renderButton(buttonDiv, {
          type: "standard",
          size: "large",
        });

        // Click the rendered button to trigger the sign-in popup
        setTimeout(() => {
          const btn = buttonDiv.querySelector('[role="button"]');
          if (btn) btn.click();
          else {
            setIsLoading(false);
            setError("Could not open Google Sign-In. Please allow popups and try again.");
          }
          // Cleanup the hidden element
          setTimeout(() => buttonDiv.remove(), 5000);
        }, 300);
      }
    });
  }

  // Callback when Google returns the credential (ID token)
  async function handleGoogleCallback(response) {
    try {
      setIsLoading(true);
      setError(null);

      // Send the Google ID token to our backend for verification
      const data = await loginWithGoogle(response.credential);
      console.log("Login successful:", data.user.email);

      // Notify the parent App component
      onLoginSuccess(data.user);
    } catch (err) {
      console.error("Login error:", err);

      // Extract error message from backend response
      const detail =
        err.response?.data?.detail ||
        "Login failed. Please try again.";

      setError(detail);
      setIsLoading(false);
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-900 via-indigo-950 to-gray-900 relative overflow-hidden">
      {/* Background decorative glow elements */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-40 -right-40 w-96 h-96 bg-primary-500/10 rounded-full blur-3xl animate-pulse-slow"></div>
        <div className="absolute -bottom-40 -left-40 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl animate-pulse-slow" style={{ animationDelay: "2s" }}></div>
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-indigo-500/5 rounded-full blur-3xl"></div>
      </div>

      {/* Login Card */}
      <div className="relative z-10 w-full max-w-md mx-4">
        <div className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-3xl p-8 shadow-2xl">
          {/* Logo and Title */}
          <div className="text-center mb-8">
            <div className="w-20 h-20 bg-gradient-to-br from-primary-500 to-purple-600 rounded-2xl flex items-center justify-center mx-auto mb-5 shadow-lg shadow-primary-500/30">
              <IoSchool className="text-white" size={40} />
            </div>
            <h1 className="text-2xl font-bold text-white">
              AI-Powered Document Query System
            </h1>
            <p className="text-gray-400 text-sm mt-2">
              PCCOE MCA Department
            </p>
          </div>

          {/* Access restriction notice */}
          <div className="bg-indigo-500/10 border border-indigo-500/20 rounded-xl p-4 mb-6">
            <div className="flex items-start gap-3">
              <IoLockClosed className="text-indigo-400 mt-0.5 flex-shrink-0" size={18} />
              <div>
                <p className="text-indigo-300 text-sm font-medium">
                  Restricted Access
                </p>
                <p className="text-indigo-300/70 text-xs mt-1">
                  Only <span className="font-semibold text-indigo-200">@pccoepune.org</span> institutional
                  email accounts are authorized to access this system.
                </p>
              </div>
            </div>
          </div>

          {/* Error message */}
          {error && (
            <div className="bg-red-500/10 border border-red-500/30 rounded-xl p-4 mb-6 animate-fade-in-up">
              <p className="text-red-300 text-sm">{error}</p>
            </div>
          )}

          {/* Google Sign-In Button */}
          <button
            onClick={handleGoogleLogin}
            disabled={isLoading}
            className="w-full flex items-center justify-center gap-3 bg-white hover:bg-gray-50 text-gray-800 font-medium py-3.5 px-6 rounded-xl transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg hover:shadow-xl hover:-translate-y-0.5 active:translate-y-0"
          >
            {isLoading ? (
              <>
                <div className="flex gap-1">
                  <div className="loading-dot" style={{ background: "#4f46e5" }}></div>
                  <div className="loading-dot" style={{ background: "#4f46e5" }}></div>
                  <div className="loading-dot" style={{ background: "#4f46e5" }}></div>
                </div>
                <span className="text-sm">Signing in...</span>
              </>
            ) : (
              <>
                {/* Official Google "G" icon */}
                <svg width="20" height="20" viewBox="0 0 48 48">
                  <path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z" />
                  <path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z" />
                  <path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z" />
                  <path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z" />
                </svg>
                <span className="text-sm">Sign in with Google</span>
              </>
            )}
          </button>

          {/* Security badge */}
          <div className="flex items-center justify-center gap-2 mt-6">
            <IoShieldCheckmark className="text-green-400" size={16} />
            <p className="text-gray-500 text-xs">
              Secured with Google OAuth 2.0
            </p>
          </div>
        </div>

        {/* Footer */}
        <p className="text-gray-600 text-xs text-center mt-6">
          Built by Dilip Magar · MCA Sem III Mini Project
        </p>
      </div>
    </div>
  );
}

export default LoginPage;
