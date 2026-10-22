import { NavLink } from "react-router-dom";
import { IoChatbubbleEllipses, IoCloudUpload, IoStatsChart, IoLogOut } from "react-icons/io5";
import { logout } from "../api/api";

// Sidebar navigation — ChatGPT-inspired dark sidebar with user profile
function Sidebar({ user }) {
  // Navigation items
  const navItems = [
    { path: "/", icon: <IoChatbubbleEllipses size={20} />, label: "Chat" },
    { path: "/upload", icon: <IoCloudUpload size={20} />, label: "Upload PDFs" },
    { path: "/dashboard", icon: <IoStatsChart size={20} />, label: "Dashboard" },
  ];

  return (
    <aside className="w-64 bg-gray-900 text-white flex flex-col h-full">
      {/* Logo / App Name */}
      <div className="p-5 border-b border-gray-700">
        <h1 className="text-xl font-bold flex items-center gap-2">
          <span className="w-8 h-8 bg-gradient-to-br from-primary-500 to-purple-600 rounded-lg flex items-center justify-center text-xs font-bold shadow-md">
            DQ
          </span>
          Document Query
        </h1>
        <p className="text-gray-400 text-xs mt-1">PCCOE MCA Department</p>
      </div>

      {/* Navigation Links */}
      <nav className="flex-1 p-3 space-y-1">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-all duration-200 ${
                isActive
                  ? "bg-primary-600 text-white shadow-lg shadow-primary-600/20"
                  : "text-gray-300 hover:bg-gray-800 hover:text-white"
              }`
            }
          >
            {item.icon}
            {item.label}
          </NavLink>
        ))}
      </nav>

      {/* User Profile & Logout */}
      <div className="p-4 border-t border-gray-700">
        {user && (
          <div className="flex items-center gap-3 mb-3">
            {/* User avatar */}
            {user.picture ? (
              <img
                src={user.picture}
                alt={user.name}
                className="w-9 h-9 rounded-full border-2 border-gray-600 flex-shrink-0"
                referrerPolicy="no-referrer"
              />
            ) : (
              <div className="w-9 h-9 rounded-full bg-primary-600 flex items-center justify-center flex-shrink-0 text-sm font-bold">
                {user.name?.charAt(0)?.toUpperCase() || "U"}
              </div>
            )}
            <div className="min-w-0 flex-1">
              <p className="text-sm font-medium text-gray-200 truncate">
                {user.name}
              </p>
              <p className="text-xs text-gray-500 truncate">
                {user.email}
              </p>
            </div>
          </div>
        )}

        {/* Logout button */}
        <button
          onClick={logout}
          className="w-full flex items-center justify-center gap-2 text-gray-400 hover:text-red-400 hover:bg-gray-800 py-2 px-3 rounded-lg text-sm transition-colors"
        >
          <IoLogOut size={18} />
          Sign Out
        </button>

        <p className="text-gray-600 text-xs text-center mt-3">
          Built by Dilip Magar
        </p>
      </div>
    </aside>
  );
}

export default Sidebar;
