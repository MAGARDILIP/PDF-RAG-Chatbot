import { useState, useRef } from "react";
import { IoCloudUpload, IoDocument, IoClose } from "react-icons/io5";

// Drag-and-drop file uploader component
function FileUploader({ onUpload, isUploading }) {
  const [dragActive, setDragActive] = useState(false);
  const [selectedFiles, setSelectedFiles] = useState([]);
  const inputRef = useRef(null);

  // Handle drag events
  function handleDrag(e) {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  }

  // Handle file drop
  function handleDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    const files = Array.from(e.dataTransfer.files).filter((f) =>
      f.name.toLowerCase().endsWith(".pdf")
    );
    if (files.length > 0) {
      setSelectedFiles((prev) => [...prev, ...files]);
    }
  }

  // Handle file selection from input
  function handleChange(e) {
    const files = Array.from(e.target.files);
    if (files.length > 0) {
      setSelectedFiles((prev) => [...prev, ...files]);
    }
  }

  // Remove a file from the list
  function removeFile(index) {
    setSelectedFiles((prev) => prev.filter((_, i) => i !== index));
  }

  // Upload all selected files
  async function handleUpload() {
    if (selectedFiles.length === 0) return;
    await onUpload(selectedFiles);
    setSelectedFiles([]);
  }

  return (
    <div>
      {/* Drop zone */}
      <div
        className={`border-2 border-dashed rounded-xl p-8 text-center transition-all duration-200 cursor-pointer ${
          dragActive
            ? "border-primary-500 bg-primary-50"
            : "border-gray-300 hover:border-primary-400 hover:bg-gray-50"
        }`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        onClick={() => inputRef.current.click()}
      >
        <IoCloudUpload
          className={`mx-auto mb-3 ${dragActive ? "text-primary-500" : "text-gray-400"}`}
          size={48}
        />
        <p className="text-sm font-medium text-gray-700">
          Drag & drop PDF files here
        </p>
        <p className="text-xs text-gray-500 mt-1">or click to browse</p>
        <input
          ref={inputRef}
          type="file"
          accept=".pdf"
          multiple
          onChange={handleChange}
          className="hidden"
        />
      </div>

      {/* Selected files list */}
      {selectedFiles.length > 0 && (
        <div className="mt-4 space-y-2">
          <p className="text-sm font-medium text-gray-700">
            Selected files ({selectedFiles.length}):
          </p>
          {selectedFiles.map((file, i) => (
            <div
              key={i}
              className="flex items-center justify-between bg-gray-50 border border-gray-200 rounded-lg px-3 py-2"
            >
              <div className="flex items-center gap-2">
                <IoDocument className="text-red-500" size={18} />
                <span className="text-sm text-gray-700 truncate max-w-xs">
                  {file.name}
                </span>
                <span className="text-xs text-gray-400">
                  ({(file.size / 1024).toFixed(1)} KB)
                </span>
              </div>
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  removeFile(i);
                }}
                className="text-gray-400 hover:text-red-500 transition-colors"
              >
                <IoClose size={18} />
              </button>
            </div>
          ))}

          {/* Upload button */}
          <button
            onClick={handleUpload}
            disabled={isUploading}
            className="w-full mt-3 bg-primary-600 text-white py-2.5 rounded-lg font-medium text-sm hover:bg-primary-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
          >
            {isUploading ? (
              <>
                <div className="loading-dot"></div>
                <div className="loading-dot"></div>
                <div className="loading-dot"></div>
              </>
            ) : (
              <>
                <IoCloudUpload size={18} />
                Upload {selectedFiles.length} file(s)
              </>
            )}
          </button>
        </div>
      )}
    </div>
  );
}

export default FileUploader;
