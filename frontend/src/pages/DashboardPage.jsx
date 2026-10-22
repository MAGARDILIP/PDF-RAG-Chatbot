import { useState, useEffect } from "react";
import { IoDocumentText, IoLayers, IoServer, IoRefresh } from "react-icons/io5";
import { getStats } from "../api/api";

function DashboardPage() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  // Load stats on page load
  useEffect(() => {
    loadStats();
  }, []);

  async function loadStats() {
    setLoading(true);
    try {
      const data = await getStats();
      setStats(data);
    } catch (error) {
      console.error("Error loading stats:", error);
    }
    setLoading(false);
  }

  // Stat card component
  function StatCard({ icon, label, value, color }) {
    return (
      <div className="bg-white rounded-xl border border-gray-200 p-5 hover:shadow-md transition-shadow">
        <div className="flex items-center gap-3">
          <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${color}`}>
            {icon}
          </div>
          <div>
            <p className="text-2xl font-bold text-gray-800">{value}</p>
            <p className="text-xs text-gray-500">{label}</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full bg-gray-50 overflow-y-auto">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 px-6 py-4 flex items-center justify-between">
        <div>
          <h2 className="text-lg font-semibold text-gray-800">📊 Dashboard</h2>
          <p className="text-xs text-gray-500">System overview and statistics</p>
        </div>
        <button
          onClick={loadStats}
          className="text-gray-400 hover:text-primary-600 transition-colors p-2 rounded-lg hover:bg-gray-100"
          title="Refresh stats"
        >
          <IoRefresh size={20} />
        </button>
      </div>

      <div className="p-6 space-y-6 max-w-4xl">
        {loading ? (
          <div className="text-center py-12">
            <div className="flex justify-center gap-1.5 mb-3">
              <div className="loading-dot"></div>
              <div className="loading-dot"></div>
              <div className="loading-dot"></div>
            </div>
            <p className="text-sm text-gray-500">Loading statistics...</p>
          </div>
        ) : stats ? (
          <>
            {/* Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <StatCard
                icon={<IoDocumentText className="text-blue-600" size={20} />}
                label="PDF Documents"
                value={stats.pdf_count}
                color="bg-blue-100"
              />
              <StatCard
                icon={<IoLayers className="text-purple-600" size={20} />}
                label="Indexed Chunks"
                value={stats.indexed_chunks}
                color="bg-purple-100"
              />
              <StatCard
                icon={<IoServer className="text-emerald-600" size={20} />}
                label="Total Size"
                value={`${stats.total_size_mb} MB`}
                color="bg-emerald-100"
              />
            </div>

            {/* Status */}
            <div className="bg-white rounded-xl border border-gray-200 p-5">
              <h3 className="text-sm font-semibold text-gray-700 mb-3">
                System Status
              </h3>
              <div className="flex items-center gap-2">
                <div
                  className={`w-2.5 h-2.5 rounded-full ${
                    stats.status === "ready"
                      ? "bg-green-500 pulse-glow"
                      : "bg-amber-500"
                  }`}
                ></div>
                <span className="text-sm text-gray-700">
                  {stats.status === "ready"
                    ? "Knowledge base is ready — you can start asking questions!"
                    : "No documents indexed — upload PDFs and rebuild the index first."}
                </span>
              </div>
            </div>

            {/* Tech Stack Info */}
            <div className="bg-white rounded-xl border border-gray-200 p-5">
              <h3 className="text-sm font-semibold text-gray-700 mb-3">
                Technology Stack
              </h3>
              <div className="grid grid-cols-2 gap-3 text-sm">
                {[
                  { label: "Embedding Model", value: "BAAI/bge-small-en-v1.5" },
                  { label: "Reranker", value: "ms-marco-MiniLM-L-6-v2" },
                  { label: "LLM", value: "Groq (gpt-oss-20b)" },
                  { label: "Vector Database", value: "ChromaDB" },
                  { label: "Backend", value: "Python + FastAPI" },
                  { label: "Frontend", value: "React + Tailwind CSS" },
                ].map((item, i) => (
                  <div key={i} className="bg-gray-50 rounded-lg px-3 py-2">
                    <p className="text-xs text-gray-500">{item.label}</p>
                    <p className="font-medium text-gray-700">{item.value}</p>
                  </div>
                ))}
              </div>
            </div>
          </>
        ) : (
          <div className="text-center py-12">
            <p className="text-sm text-gray-500">
              Could not load stats. Is the backend running?
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

export default DashboardPage;
