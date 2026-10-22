import { useState, useEffect } from "react";
import { IoTrash, IoRefresh, IoCheckmarkCircle, IoAlertCircle } from "react-icons/io5";
import FileUploader from "../components/FileUploader";
import { uploadPDFs, getDocuments, deleteDocument, rebuildIndex } from "../api/api";

function UploadPage() {
  const [documents, setDocuments] = useState([]);
  const [isUploading, setIsUploading] = useState(false);
  const [isRebuilding, setIsRebuilding] = useState(false);
  const [notification, setNotification] = useState(null);

  // Load document list on page load
  useEffect(() => {
    loadDocuments();
  }, []);

  // Show a notification message that disappears after 4 seconds
  function showNotification(message, type = "success") {
    setNotification({ message, type });
    setTimeout(() => setNotification(null), 4000);
  }

  // Fetch the list of uploaded documents
  async function loadDocuments() {
    try {
      const data = await getDocuments();
      setDocuments(data.documents || []);
    } catch (error) {
      console.error("Error loading documents:", error);
    }
  }

  // Handle file upload
  async function handleUpload(files) {
    setIsUploading(true);
    try {
      const data = await uploadPDFs(files);
      showNotification(data.message);
      await loadDocuments();
    } catch (error) {
      showNotification("Upload failed. Is the backend running?", "error");
      console.error("Upload error:", error);
    }
    setIsUploading(false);
  }

  // Handle document deletion
  async function handleDelete(name) {
    if (!confirm(`Delete "${name}"? This cannot be undone.`)) return;

    try {
      await deleteDocument(name);
      showNotification(`Deleted "${name}"`);
      await loadDocuments();
    } catch (error) {
      showNotification("Delete failed", "error");
      console.error("Delete error:", error);
    }
  }

  // Handle index rebuild
  async function handleRebuild() {
    setIsRebuilding(true);
    try {
      const data = await rebuildIndex();
      showNotification(
        `${data.message} (${data.chunks_created} chunks created from ${data.pages_loaded} pages)`
      );
    } catch (error) {
      showNotification("Rebuild failed. Check the backend logs.", "error");
      console.error("Rebuild error:", error);
    }
    setIsRebuilding(false);
  }

  return (
    <div className="flex flex-col h-full bg-gray-50 overflow-y-auto">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 px-6 py-4">
        <h2 className="text-lg font-semibold text-gray-800">📄 Upload PDFs</h2>
        <p className="text-xs text-gray-500">
          Upload department documents and build the knowledge base
        </p>
      </div>

      {/* Notification Toast */}
      {notification && (
        <div
          className={`mx-6 mt-4 p-3 rounded-lg flex items-center gap-2 text-sm animate-fade-in-up ${
            notification.type === "error"
              ? "bg-red-50 text-red-700 border border-red-200"
              : "bg-green-50 text-green-700 border border-green-200"
          }`}
        >
          {notification.type === "error" ? (
            <IoAlertCircle size={18} />
          ) : (
            <IoCheckmarkCircle size={18} />
          )}
          {notification.message}
        </div>
      )}

      <div className="p-6 space-y-6 max-w-3xl">
        {/* File Upload Section */}
        <div className="bg-white rounded-xl border border-gray-200 p-5">
          <h3 className="text-sm font-semibold text-gray-700 mb-3">
            Upload New Documents
          </h3>
          <FileUploader onUpload={handleUpload} isUploading={isUploading} />
        </div>

        {/* Rebuild Index Button */}
        <div className="bg-white rounded-xl border border-gray-200 p-5">
          <h3 className="text-sm font-semibold text-gray-700 mb-2">
            Build Knowledge Base
          </h3>
          <p className="text-xs text-gray-500 mb-3">
            After uploading PDFs, click this button to process them into the AI knowledge base.
            This extracts text, creates embeddings, and stores them in ChromaDB.
          </p>
          <button
            onClick={handleRebuild}
            disabled={isRebuilding}
            className="bg-emerald-600 text-white px-5 py-2.5 rounded-lg font-medium text-sm hover:bg-emerald-700 transition-colors disabled:opacity-50 flex items-center gap-2"
          >
            {isRebuilding ? (
              <>
                <IoRefresh className="animate-spin" size={18} />
                Processing... (this may take a minute)
              </>
            ) : (
              <>
                <IoRefresh size={18} />
                Rebuild Index
              </>
            )}
          </button>
        </div>

        {/* Document List */}
        <div className="bg-white rounded-xl border border-gray-200 p-5">
          <h3 className="text-sm font-semibold text-gray-700 mb-3">
            Uploaded Documents ({documents.length})
          </h3>

          {documents.length === 0 ? (
            <p className="text-sm text-gray-400 text-center py-6">
              No documents uploaded yet
            </p>
          ) : (
            <div className="space-y-2">
              {documents.map((doc, i) => (
                <div
                  key={i}
                  className="flex items-center justify-between bg-gray-50 border border-gray-200 rounded-lg px-4 py-3 hover:bg-gray-100 transition-colors"
                >
                  <div className="flex items-center gap-3">
                    <span className="text-2xl">📄</span>
                    <div>
                      <p className="text-sm font-medium text-gray-700">
                        {doc.name}
                      </p>
                      <p className="text-xs text-gray-400">{doc.size_kb} KB</p>
                    </div>
                  </div>
                  <button
                    onClick={() => handleDelete(doc.name)}
                    className="text-gray-400 hover:text-red-500 transition-colors p-1"
                    title="Delete document"
                  >
                    <IoTrash size={18} />
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default UploadPage;
