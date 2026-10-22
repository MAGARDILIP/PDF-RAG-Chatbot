import { IoPersonCircle, IoSparkles } from "react-icons/io5";
import SourceCard from "./SourceCard";

// Individual chat message bubble (user or bot)
function ChatMessage({ message }) {
  const isUser = message.role === "user";

  return (
    <div className={`flex gap-3 animate-fade-in-up ${isUser ? "justify-end" : "justify-start"}`}>
      {/* Bot avatar (only for bot messages) */}
      {!isUser && (
        <div className="w-8 h-8 rounded-full bg-primary-500 flex items-center justify-center flex-shrink-0 mt-1">
          <IoSparkles className="text-white" size={16} />
        </div>
      )}

      {/* Message content */}
      <div className={`max-w-[75%] ${isUser ? "order-1" : ""}`}>
        <div
          className={`px-4 py-3 rounded-2xl text-sm leading-relaxed ${
            isUser
              ? "bg-primary-600 text-white rounded-br-md"
              : "bg-white text-gray-800 border border-gray-200 rounded-bl-md shadow-sm"
          }`}
        >
          {/* Render the message text with line breaks */}
          {message.content.split("\n").map((line, i) => (
            <p key={i} className={i > 0 ? "mt-2" : ""}>
              {line}
            </p>
          ))}
        </div>

        {/* Source citations (only for bot messages that have sources) */}
        {!isUser && message.sources && message.sources.length > 0 && (
          <div className="mt-2 space-y-1">
            <p className="text-xs text-gray-500 font-medium ml-1">📄 Sources:</p>
            {message.sources.map((source, i) => (
              <SourceCard key={i} source={source} />
            ))}
          </div>
        )}

        {/* Out-of-scope indicator */}
        {!isUser && message.is_in_scope === false && (
          <div className="mt-2 ml-1">
            <span className="text-xs bg-amber-100 text-amber-700 px-2 py-1 rounded-full font-medium">
              ⚠️ Not found in documents
            </span>
          </div>
        )}
      </div>

      {/* User avatar (only for user messages) */}
      {isUser && (
        <div className="w-8 h-8 rounded-full bg-gray-300 flex items-center justify-center flex-shrink-0 mt-1">
          <IoPersonCircle className="text-gray-600" size={20} />
        </div>
      )}
    </div>
  );
}

export default ChatMessage;
