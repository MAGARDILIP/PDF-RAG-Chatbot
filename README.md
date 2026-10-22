# AI-Powered Document Query System

> **MCA Semester III Mini Project**
> Pimpri Chinchwad College of Engineering (PCCOE), Pune
> Department of Master of Computer Application (MCA)

An intelligent document query system that lets authorized users upload PDF documents and ask natural-language questions. The system retrieves precise answers with source citations using a Retrieval-Augmented Generation (RAG) pipeline.

---

## 🏗️ Architecture

```
User Question
     │
     ▼
┌──────────────────────────────────────────────────┐
│              React + Vite Frontend               │
│   (Google OAuth Login → Chat → Upload → Stats)   │
└──────────────────────┬───────────────────────────┘
                       │ REST API (Bearer Token)
                       ▼
┌──────────────────────────────────────────────────┐
│              FastAPI Backend (Python)             │
│                                                  │
│  1. PDF Ingestion (pdfplumber)                   │
│  2. Text Chunking (LangChain RecursiveCharText)  │
│  3. Embedding (BAAI/bge-small-en-v1.5)           │
│  4. Vector Store (ChromaDB)                      │
│  5. Retrieval + CrossEncoder Reranking           │
│  6. LLM Answer Generation (Groq API)            │
│  7. Google OAuth (@pccoepune.org only)           │
└──────────────────────────────────────────────────┘
```

### RAG Pipeline Flow

1. **Upload & Parse** — PDFs are parsed with `pdfplumber` (tables extracted row-by-row).
2. **Chunk** — Text is split into 1200-char chunks with 200-char overlap.
3. **Embed** — Each chunk is embedded using `BAAI/bge-small-en-v1.5` (384-dim, runs locally).
4. **Store** — Embeddings are stored in ChromaDB (persistent, file-based).
5. **Retrieve** — Top 30 candidates retrieved via cosine similarity.
6. **Rerank** — `cross-encoder/ms-marco-MiniLM-L-6-v2` reranks and picks the best 10.
7. **Generate** — Groq LLM generates an answer strictly from the retrieved context.
8. **Guardrail** — Out-of-scope questions are rejected before reaching the LLM.

---

## ✨ Features

- **Natural Language Q&A** — Ask questions in plain English, get precise answers with page citations.
- **Table-Aware Extraction** — Structured tables (course lists, timetables) are parsed row-by-row, not garbled.
- **Two-Stage Retrieval** — Fast vector search + accurate CrossEncoder reranking.
- **Hallucination Guard** — Out-of-scope questions are blocked before reaching the LLM.
- **Google OAuth** — Restricted to `@pccoepune.org` institutional accounts only.
- **Document Management** — Upload, list, delete PDFs, and rebuild the knowledge base via the UI.
- **Real-Time Dashboard** — View indexed chunk count, document stats, and system status.

---

## 🛠️ Tech Stack

| Layer           | Technology                                  |
|-----------------|---------------------------------------------|
| Frontend        | React 18, Vite, Tailwind CSS, React Router  |
| Backend         | Python, FastAPI, Uvicorn                     |
| PDF Parsing     | pdfplumber (tables + text)                   |
| Embeddings      | BAAI/bge-small-en-v1.5 (sentence-transformers) |
| Reranker        | cross-encoder/ms-marco-MiniLM-L-6-v2        |
| Vector Database | ChromaDB (persistent, file-based)            |
| LLM             | Groq API (openai/gpt-oss-20b)               |
| Authentication  | Google OAuth 2.0 (Identity Services)         |

---

## 📁 Project Structure

```
PDF-RAG-Chatbot/
├── backend/
│   ├── main.py              # FastAPI app, routes, CORS
│   ├── config.py             # All configuration constants
│   ├── .env                  # API keys (Groq, Google OAuth)
│   ├── requirements.txt      # Python dependencies
│   ├── core/
│   │   ├── pdf_loader.py     # pdfplumber PDF + table extraction
│   │   ├── text_splitter.py  # LangChain recursive text chunking
│   │   ├── embeddings.py     # BGE-small embedding model loader
│   │   ├── vector_store.py   # ChromaDB operations (add, search, clear)
│   │   ├── retriever.py      # Two-stage retrieve + CrossEncoder rerank
│   │   ├── generator.py      # Groq LLM answer generation with guardrails
│   │   └── auth.py           # Google OAuth token verification & sessions
│   └── data/
│       ├── pdfs/             # Uploaded PDF files
│       └── vector_store/     # ChromaDB persistence directory
│
├── frontend/
│   ├── index.html            # Entry HTML with Google GIS script
│   ├── package.json          # Node dependencies
│   ├── vite.config.js        # Vite configuration
│   ├── tailwind.config.js    # Tailwind CSS configuration
│   ├── .env                  # VITE_GOOGLE_CLIENT_ID, VITE_API_BASE
│   ├── public/
│   │   └── favicon.svg       # App favicon (DQ gradient icon)
│   └── src/
│       ├── main.jsx          # React entry point
│       ├── App.jsx           # Router + auth guard
│       ├── index.css         # Global styles + animations
│       ├── api/
│       │   └── api.js        # Axios HTTP client with auth headers
│       ├── components/
│       │   ├── Sidebar.jsx       # Navigation sidebar with user profile
│       │   ├── ChatMessage.jsx   # Chat bubble component
│       │   ├── SourceCard.jsx    # Source citation card
│       │   └── FileUploader.jsx  # Drag-and-drop PDF uploader
│       └── pages/
│           ├── LoginPage.jsx     # Google OAuth sign-in page
│           ├── ChatPage.jsx      # Main Q&A chat interface
│           ├── UploadPage.jsx    # PDF upload + index rebuild
│           └── DashboardPage.jsx # System stats dashboard
│
└── README.md
```

---

## 🚀 Setup & Run

### Prerequisites

- Python 3.10+
- Node.js 18+
- A [Groq API key](https://console.groq.com/keys) (free)
- A [Google OAuth Client ID](https://console.cloud.google.com/apis/credentials) configured for `http://localhost:5173`

### 1. Backend Setup

```bash
cd backend

# Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Configure environment
# Edit .env and set your GROQ_API_KEY and GOOGLE_CLIENT_ID/SECRET

# Start the server
python main.py
```

The backend runs at **http://localhost:8000**. API docs at **http://localhost:8000/docs**.

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
# Edit .env and set VITE_GOOGLE_CLIENT_ID

# Start dev server
npm run dev
```

The frontend runs at **http://localhost:5173**.

### 3. Using the System

1. Open **http://localhost:5173** in your browser.
2. Sign in with your **@pccoepune.org** Google account.
3. Go to **Upload PDFs** → upload department PDF documents.
4. Click **Rebuild Index** to process documents into the knowledge base.
5. Go to **Chat** → ask questions about the uploaded documents.

---

## 📝 API Endpoints

| Method | Endpoint          | Auth | Description                        |
|--------|-------------------|------|------------------------------------|
| GET    | `/`               | No   | Health check                       |
| POST   | `/auth/google`    | No   | Authenticate with Google ID token  |
| GET    | `/auth/me`        | Yes  | Get current user info              |
| POST   | `/upload`         | Yes  | Upload PDF files                   |
| GET    | `/documents`      | Yes  | List uploaded PDFs                 |
| DELETE | `/document/{name}`| Yes  | Delete a specific PDF              |
| POST   | `/rebuild-index`  | Yes  | Rebuild the vector database        |
| POST   | `/chat`           | Yes  | Ask a question (RAG pipeline)      |
| GET    | `/stats`          | Yes  | Get system statistics              |

---

## 👨‍💻 Author

**Dilip Magar** (PRN: 125M1H055)
MCA Semester III, PCCOE Pune
Guide: Dr. Anjana Arakerimath
