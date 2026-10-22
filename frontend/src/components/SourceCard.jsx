import { IoDocumentText } from "react-icons/io5";

// Shows the source PDF name, page number, and a text snippet
function SourceCard({ source }) {
  return (
    <div className="bg-gray-50 border border-gray-200 rounded-lg p-2 ml-1 flex items-start gap-2 hover:bg-gray-100 transition-colors cursor-default">
      {/* Document icon */}
      <div className="w-6 h-6 bg-primary-100 rounded flex items-center justify-center flex-shrink-0 mt-0.5">
        <IoDocumentText className="text-primary-600" size={14} />
      </div>

      {/* Source details */}
      <div className="min-w-0 flex-1">
        <p className="text-xs font-semibold text-gray-700 truncate">
          {source.file}
        </p>
        <p className="text-xs text-primary-600 font-medium">
          Page {source.page}
        </p>
        {source.snippet && (
          <p className="text-xs text-gray-500 mt-1 line-clamp-2">
            {source.snippet.startsWith("[TABLE DATA]") ? (
              <span>
                <span className="inline-block bg-primary-100 text-primary-700 text-[10px] font-semibold px-1.5 py-0.2 rounded mr-1">
                  Table
                </span>
                {source.snippet.replace(/^\[TABLE DATA\]\s*/, "").replace(/\s*\|\s*/g, " · ")}
              </span>
            ) : (
              source.snippet
            )}
          </p>
        )}
      </div>
    </div>
  );
}

export default SourceCard;
