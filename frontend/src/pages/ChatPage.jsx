import { useState, useRef, useEffect } from "react";
import { IoSend, IoTrashOutline } from "react-icons/io5";
import ChatMessage from "../components/ChatMessage";
import { sendQuestion } from "../api/api";

function ChatPage() {
  // Restore messages from sessionStorage so they survive page navigation
  const [messages, setMessages] = useState(() => {
    try {
      const saved = sessionStorage.getItem("rag_chat_messages");
      return saved ? JSON.parse(saved) : [];
    } catch {
      return [];
    }
  });
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  // Auto-save messages to sessionStorage whenever they change
  useEffect(() => {
    try {
      sessionStorage.setItem("rag_chat_messages", JSON.stringify(messages));
    } catch (e) {
      console.error("Failed to save chat to sessionStorage:", e);
    }
  }, [messages]);

  // Clear chat messages
  function handleClearChat() {
    setMessages([]);
    try {
      sessionStorage.removeItem("rag_chat_messages");
    } catch (e) {}
  }

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // Focus input on page load
  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  // Send a question to the backend
  async function handleSend() {
    const question = input.trim();
    if (!question || isLoading) return;

    // Add user message to chat
    const userMessage = { role: "user", content: question };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      // Call the backend /chat endpoint
      const data = await sendQuestion(question);

      // Add bot response to chat
      const botMessage = {
        role: "assistant",
        content: data.answer,
        sources: data.sources,
        is_in_scope: data.is_in_scope,
      };
      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      // Handle errors
      const errorMessage = {
        role: "assistant",
        content: "Sorry, something went wrong. Please make sure the backend server is running and try again.",
        sources: [],
        is_in_scope: true,
      };
      setMessages((prev) => [...prev, errorMessage]);
      console.error("Chat error:", error);
    }

    setIsLoading(false);
  }

  // Handle Enter key press
  function handleKeyDown(e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  }

  return (
    <div className="flex flex-col h-full bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 px-6 py-4 flex items-center justify-between">
        <div>
          <h2 className="text-lg font-semibold text-gray-800">💬 Ask a Question</h2>
          <p className="text-xs text-gray-500">
            Ask questions about uploaded department documents
          </p>
        </div>
        {messages.length > 0 && (
          <button
            onClick={handleClearChat}
            className="flex items-center gap-1.5 text-xs text-gray-500 hover:text-red-600 px-3 py-1.5 rounded-lg border border-gray-200 hover:border-red-200 hover:bg-red-50 transition-colors"
            title="Clear current chat"
          >
            <IoTrashOutline size={14} />
            <span>Clear Chat</span>
          </button>
        )}
      </div>

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto px-6 py-4 space-y-4">
        {/* Welcome message when chat is empty */}
        {messages.length === 0 && (
          <div className="flex items-center justify-center h-full">
            <div className="text-center">
              <div className="w-16 h-16 bg-primary-100 rounded-2xl flex items-center justify-center mx-auto mb-4">
                <span className="text-3xl">🤖</span>
              </div>
              <h3 className="text-lg font-semibold text-gray-700">
                AI-Powered Document Query System
              </h3>
              <p className="text-sm text-gray-500 mt-2 max-w-md">
                Ask any question about uploaded PCCOE MCA department documents.
                I'll retrieve the answer and cite the exact source.
              </p>
              <div className="mt-6 space-y-2">
                <p className="text-xs text-gray-400 font-medium">Try asking:</p>
                {[
                  "What are the admission requirements?",
                  "How many total credits are required to complete the MCA programme?",
                  "What are the exam guidelines?",
                ].map((q, i) => (
                  <button
                    key={i}
                    onClick={() => setInput(q)}
                    className="block mx-auto text-sm text-primary-600 hover:text-primary-700 bg-primary-50 hover:bg-primary-100 px-4 py-2 rounded-lg transition-colors"
                  >
                    "{q}"
                  </button>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Chat messages */}
        {messages.map((msg, i) => (
          <ChatMessage key={i} message={msg} />
        ))}

        {/* Loading indicator */}
        {isLoading && (
          <div className="flex gap-3 animate-fade-in-up">
            <div className="w-8 h-8 rounded-full bg-primary-500 flex items-center justify-center flex-shrink-0">
              <span className="text-white text-xs">AI</span>
            </div>
            <div className="bg-white border border-gray-200 rounded-2xl rounded-bl-md px-4 py-3 shadow-sm">
              <div className="flex gap-1.5">
                <div className="loading-dot"></div>
                <div className="loading-dot"></div>
                <div className="loading-dot"></div>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="bg-white border-t border-gray-200 px-6 py-4">
        <div className="flex gap-3 max-w-4xl mx-auto">
          <input
            ref={inputRef}
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask a question about your documents..."
            disabled={isLoading}
            className="flex-1 border border-gray-300 rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent disabled:opacity-50 disabled:bg-gray-50"
          />
          <button
            onClick={handleSend}
            disabled={isLoading || !input.trim()}
            className="bg-primary-600 text-white px-5 py-3 rounded-xl hover:bg-primary-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
          >
            <IoSend size={18} />
          </button>
        </div>
        <p className="text-xs text-gray-400 text-center mt-2">
          Answers are generated strictly from uploaded department documents only
        </p>
      </div>
    </div>
  );
}

export default ChatPage;
