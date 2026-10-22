# PDF RAG Chatbot — Development Reference

> This file is a quick reference for the AI assistant while building this project.
> It contains all decisions made during planning.
> **IMPORTANT RULE:** Whatever is planned in an implementation plan (`implementation_plan.md`) MUST be documented in this file (`claude.md`).

## Project Summary
- **What:** Full-stack PDF Question-Answering Chatbot using RAG
- **For:** MCA Semester III Mini Project (MCA23702) + Semester IV Seminar (MCA24703)
- **Target Use Case (Mam's Requirements):**
  - **Restricted Access:** Only college users with a verified `@pccoepune.org` Google account can access the chatbot.
  - **Department Knowledge Base:** Designed to ingest college/department PDFs provided by faculty (mam).
  - **Strict Answering:** Fetches and generates answers strictly from those uploaded department PDFs (with source citations) rather than general LLM knowledge.
- **Seminar Title:** Domain-Specific Conversational AI for Institutional Knowledge Retrieval Using Retrieval-Augmented Generation (RAG) (see [SEMINAR_SYNOPSIS.md](file:///d:/Projects_2026/PDF-RAG-Chatbot/SEMINAR_SYNOPSIS.md))


## Tech Stack (Final Decisions)
| Layer | Technology |
|---|---|
| Frontend | React + Tailwind CSS v3 + Vite |
| Backend | Python + FastAPI |
| RAG Pipeline | LangChain + ChromaDB + SentenceTransformers |
| LLM | Groq API (model: qwen/qwen3-32b) |
| Embeddings | SentenceTransformer (BAAI/bge-small-en-v1.5) |
| Reranker | CrossEncoder (ms-marco-MiniLM-L-6-v2) |
| API Style | REST (JSON) |

## Out-of-Scope & Hallucination Prevention (Strict RAG Guardrail)
- **Strict Scope Rule:** If a user asks ANY question (even general knowledge) whose answer is **not found in the uploaded college/department PDFs**, the chatbot **MUST NOT** answer from general LLM knowledge.
- **Proper Out-of-Scope Message:** Instead of answering, the chatbot must return a clear, professional message such as:
  > *"I cannot answer this question because the information was not found in our uploaded department documents. I am restricted to answering questions strictly from the college/department knowledge base."*
- **Implementation Mechanism:**
  - **System Prompt Instruction:** Explicitly command the LLM: *"Answer based ONLY on the provided document context. If the answer is not present in the context, do NOT use outside knowledge. Reply exactly with the out-of-scope message."*
  - **Similarity Score Threshold:** If the top retrieved document chunks have low similarity/relevance scores, bypass the LLM and return the out-of-scope message immediately.

## Code Style Rules
- **Beginner-friendly** — write like an MCA student who is learning
- Simple comments: `# Load the PDF file`
- NO type hints: `def load_pdfs(folder):` not `def load_pdfs(folder: str) -> List:`
- NO complex docstrings
- NO logging module — use `print()`
- NO custom exception classes — use basic `try/except`
- Add comments explaining WHY choices were made: `# I chose ChromaDB because it's free and local`
- **Plan Synchronization:** Anything planned in an implementation plan MUST be recorded in `claude.md`.

## Folder Structure
```
PDF-RAG-Chatbot/
├── backend/
│   ├── main.py              # FastAPI app + routes
│   ├── config.py            # Settings
│   ├── requirements.txt
│   ├── .env                 # GROQ_API_KEY
│   ├── core/
│   │   ├── __init__.py
│   │   ├── pdf_loader.py
│   │   ├── text_splitter.py
│   │   ├── embeddings.py
│   │   ├── vector_store.py
│   │   ├── retriever.py
│   │   └── generator.py
│   └── data/
│       ├── pdfs/
│       └── vector_store/
│
├── frontend/
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   ├── index.html
│   └── src/
│       ├── App.jsx
│       ├── main.jsx
│       ├── index.css
│       ├── pages/
│       │   ├── ChatPage.jsx
│       │   ├── UploadPage.jsx
│       │   └── DashboardPage.jsx
│       ├── components/
│       │   ├── Sidebar.jsx
│       │   ├── ChatMessage.jsx
│       │   ├── FileUploader.jsx
│       │   └── SourceCard.jsx
│       └── api/
│           └── api.js
│
├── claude.md                # THIS FILE (dev reference)
├── PROJECT_DESCRIPTION.md   # Full project description
└── README.md                # Public-facing README
```

## API Endpoints
| Method | Endpoint | Purpose |
|---|---|---|
| POST | /upload | Upload PDF files |
| GET | /documents | List uploaded PDFs |
| DELETE | /document/{name} | Delete a PDF |
| POST | /rebuild-index | Process PDFs → embeddings |
| POST | /chat | Ask a question, get answer |
| GET | /stats | Get system statistics |

## Config Values
```python
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"
RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"
LLM_MODEL = "qwen/qwen3-32b"
CHUNK_SIZE = 800
CHUNK_OVERLAP = 150
TOP_K = 5
TEMPERATURE = 0.1
```

## Build Order
1. Backend: config.py → core/ modules → main.py routes
2. Test backend APIs
3. Frontend: React + Tailwind setup → Pages → Components → API calls
4. Connect frontend ↔ backend
5. Polish: styling, README, error handling

## UI Design
- ChatGPT-inspired: dark sidebar + light/dark chat area
- Sidebar: bg-gray-900
- Accent: indigo-500 / violet-500
- User bubble: bg-indigo-600 text-white
- Bot bubble: bg-white text-gray-800

## Chat History
- Session-only (React useState) — disappears on refresh
- Simpler for a student project

## Authentication & Access Control (Implementation Plan: Domain-Specific Google OAuth)
- **Goal:** Modify the application (`app.py`) to require users to log in with their Google accounts and verify that the user's email address ends with `@pccoepune.org` before granting access to the RAG Chatbot interface.

### 1. Google Cloud Setup Required
- Go to Google Cloud Console and create a new project.
- Go to **APIs & Services > OAuth consent screen**, choose "External" (or "Internal" if using a college Workspace admin account), and configure required details.
- Go to **Credentials > Create Credentials > OAuth client ID > Web application**.
- Add `http://localhost:8501` to **Authorized redirect URIs** (or server domain if deployed).
- Copy the generated **Client ID** and **Client Secret**.

### 2. Configuration (`.env`)
Append the following variables to `.env`:
```env
GOOGLE_CLIENT_ID="your_client_id_here"
GOOGLE_CLIENT_SECRET="your_client_secret_here"
REDIRECT_URI="http://localhost:8501"
```

### 3. Application Code Changes (`app.py`)
- **Imports:** Import `requests` and `urllib.parse` to handle OAuth2 token exchange with Google.
- **Authentication Logic:**
  - Check if the user is authenticated via `st.session_state`.
  - If not, check for an OAuth code in URL query parameters (returned after Google redirect).
  - Exchange the authorization code for an access token and fetch the user's profile/email.
  - Validate that the email ends with `@pccoepune.org`.
- **Login Screen:** If not authenticated and no authorization code is present, display a prominent "Login with Google" button pointing to the Google OAuth consent URL.
- **Access Protection:** Wrap existing UI tabs and chat interface inside an `if st.session_state.authenticated:` block so unauthorized users cannot access the chatbot or upload functionality.

### 4. Verification Plan
- **Manual Verification:**
  - Start app with `streamlit run app.py` and ensure the Login screen appears instead of the chatbot UI.
  - Authenticate with a valid `@pccoepune.org` account (access should be granted).
  - In an incognito window, attempt login with a standard `@gmail.com` account (should show "Access Denied").
