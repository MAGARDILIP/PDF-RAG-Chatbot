import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# === Groq API Settings ===
# I chose Groq because it gives free access to open-source LLMs at very fast speed
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LLM_MODEL = "openai/gpt-oss-20b"
TEMPERATURE = 0.1  # Low temperature = more factual, less creative answers

# === Embedding Model Settings ===
# I chose BAAI/bge-small-en-v1.5 because it's small, fast, and runs locally for free
# It converts text into 384-dimensional vectors
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"

# === Reranker Model Settings ===
# CrossEncoder reads the question AND document together for much better accuracy
# I chose ms-marco-MiniLM because it's lightweight and accurate
RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"

# === Text Chunking Settings ===
# 1200 characters per chunk captures full tables/lists (like semester subjects)
# Larger chunks = more context per chunk, fewer splits in the middle of content
CHUNK_SIZE = 1200
# 200 character overlap ensures no information is lost between chunk boundaries
CHUNK_OVERLAP = 200

# === Retrieval Settings ===
# First retrieve top 30 candidates from ChromaDB (cast a wider net)
INITIAL_RETRIEVAL_COUNT = 30
# Then reranker picks the best 10 from those 30 (more context for complete answers)
TOP_K = 10
# If the best chunk's similarity score is below this, the question is out-of-scope
# CrossEncoder outputs logit scores (-11 to +11), NOT 0-1 probabilities
# Lowered to -10.0 to be permissive; the LLM system prompt is the real guardrail
SIMILARITY_THRESHOLD = -10.0

# === File Paths ===
# Where uploaded PDFs are stored on disk
PDF_FOLDER = os.path.join(os.path.dirname(__file__), "data", "pdfs")
# Where ChromaDB stores the vector database files
VECTOR_STORE_PATH = os.path.join(os.path.dirname(__file__), "data", "vector_store")

# === Google OAuth Settings ===
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI", "http://localhost:5173/auth/callback")
# Only emails ending with this domain can access the chatbot
ALLOWED_EMAIL_DOMAIN = "pccoepune.org"

# === Server Settings ===
# Frontend runs on port 5173 (Vite default), backend on port 8000
BACKEND_PORT = 8000
FRONTEND_URL = "http://localhost:5173"

# Create data folders if they don't exist
os.makedirs(PDF_FOLDER, exist_ok=True)
os.makedirs(VECTOR_STORE_PATH, exist_ok=True)

# Quick check: warn if API key is missing
if not GROQ_API_KEY or GROQ_API_KEY == "your_groq_api_key_here":
    print("WARNING: GROQ_API_KEY is not set! Please update your .env file.")
    print("Get your free key from: https://console.groq.com/keys")
