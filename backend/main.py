import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from config import PDF_FOLDER, FRONTEND_URL, BACKEND_PORT
from core.pdf_loader import load_all_pdfs
from core.text_splitter import split_documents
from core.vector_store import (
    add_documents_to_store,
    clear_vector_store,
    get_document_count
)
from core.generator import generate_answer
from core.auth import (
    verify_google_id_token,
    create_session,
    get_current_user,
    SESSIONS
)

# === Create the FastAPI app ===
app = FastAPI(
    title="AI-Powered Document Query System API",
    description="RAG-based chatbot for PCCOE MCA Department with Google OAuth restricted to @pccoepune.org",
    version="1.0.0"
)

# === CORS Middleware ===
# This allows the React frontend (port 5173) to talk to the backend (port 8000)
# Without this, the browser blocks the requests for security reasons
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],  # Only allow our frontend
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)


# === Request/Response Models ===
# These define the shape of data the API expects and returns

class GoogleAuthRequest(BaseModel):
    id_token: str


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str
    sources: list
    is_in_scope: bool


# === Public Routes (no auth needed) ===

@app.get("/")
def root():
    """Health check — just confirms the server is running."""
    return {"message": "PDF RAG Chatbot API is running!", "status": "ok"}


# === Authentication Routes (Google OAuth) ===

@app.post("/auth/google")
def google_auth(payload: GoogleAuthRequest):
    """
    Authenticate user via Google ID token.
    Validates token with Google servers and enforces @pccoepune.org domain.
    Returns a session token for subsequent API calls.
    """
    user_info = verify_google_id_token(payload.id_token)
    session_token = create_session(user_info)
    print(f"User authenticated: {user_info['email']} ({user_info['name']})")
    return {
        "token": session_token,
        "user": user_info,
        "message": f"Welcome, {user_info['name']}!"
    }


@app.get("/auth/me")
def get_me(current_user: dict = Depends(get_current_user)):
    """Get current authenticated user info."""
    return {"user": current_user}


@app.post("/auth/logout")
def logout():
    """Log out user and invalidate session."""
    return {"message": "Logged out successfully"}


# === Protected Routes (require @pccoepune.org login) ===

@app.post("/upload")
async def upload_pdfs(
    files: list[UploadFile] = File(...),
    current_user: dict = Depends(get_current_user)
):
    """Upload one or more PDF files to the server."""
    uploaded = []
    errors = []

    for file in files:
        # Only accept PDF files
        if not file.filename.lower().endswith(".pdf"):
            errors.append(f"{file.filename} — not a PDF file, skipped")
            continue

        try:
            # Save the file to the pdfs folder
            file_path = os.path.join(PDF_FOLDER, file.filename)

            with open(file_path, "wb") as f:
                content = await file.read()
                f.write(content)

            uploaded.append(file.filename)
            print(f"Uploaded: {file.filename} by {current_user['email']}")

        except Exception as e:
            errors.append(f"{file.filename} — error: {str(e)}")

    return {
        "uploaded": uploaded,
        "errors": errors,
        "message": f"Successfully uploaded {len(uploaded)} file(s)"
    }


@app.get("/documents")
def list_documents(current_user: dict = Depends(get_current_user)):
    """List all uploaded PDF files."""
    if not os.path.exists(PDF_FOLDER):
        return {"documents": []}

    pdf_files = []
    for f in os.listdir(PDF_FOLDER):
        if f.lower().endswith(".pdf"):
            file_path = os.path.join(PDF_FOLDER, f)
            size_kb = round(os.path.getsize(file_path) / 1024, 1)
            pdf_files.append({
                "name": f,
                "size_kb": size_kb
            })

    return {"documents": pdf_files, "count": len(pdf_files)}


@app.delete("/document/{name}")
def delete_document(name: str, current_user: dict = Depends(get_current_user)):
    """Delete a specific PDF file."""
    file_path = os.path.join(PDF_FOLDER, name)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"File '{name}' not found")

    os.remove(file_path)
    print(f"Deleted: {name} by {current_user['email']}")

    return {"message": f"Deleted '{name}' successfully. Run /rebuild-index to update the knowledge base."}


@app.post("/rebuild-index")
def rebuild_index(current_user: dict = Depends(get_current_user)):
    """
    Process all PDFs and rebuild the vector database from scratch.
    Steps: Load PDFs → Split into chunks → Create embeddings → Store in ChromaDB
    """
    try:
        # Step 1: Clear old data
        print(f"Step 1: Clearing old vector store data (requested by {current_user['email']})...")
        clear_vector_store()

        # Step 2: Load all PDFs
        print("Step 2: Loading all PDF files...")
        pages = load_all_pdfs(PDF_FOLDER)

        if not pages:
            return {
                "message": "No PDF files found. Please upload some PDFs first.",
                "chunks_created": 0
            }

        # Step 3: Split into chunks
        print("Step 3: Splitting documents into chunks...")
        chunks = split_documents(pages)

        # Step 4: Add to vector store (embeddings are created automatically)
        print("Step 4: Creating embeddings and storing in ChromaDB...")
        count = add_documents_to_store(chunks)

        print(f"Index rebuild complete! {count} chunks indexed.")

        return {
            "message": "Knowledge base rebuilt successfully!",
            "pages_loaded": len(pages),
            "chunks_created": count
        }

    except Exception as e:
        print(f"Error rebuilding index: {e}")
        raise HTTPException(status_code=500, detail=f"Error rebuilding index: {str(e)}")


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest, current_user: dict = Depends(get_current_user)):
    """Ask a question and get an answer from the uploaded documents."""
    question = request.question.strip()

    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    # Check if there are any documents indexed
    doc_count = get_document_count()
    if doc_count == 0:
        return ChatResponse(
            answer="No documents have been indexed yet. Please upload PDFs and click 'Rebuild Index' first.",
            sources=[],
            is_in_scope=False
        )

    print(f"\nQuestion from {current_user['email']}: {question}")
    print(f"Searching through {doc_count} indexed chunks...")

    # Generate answer using our RAG pipeline
    result = generate_answer(question)

    return ChatResponse(
        answer=result["answer"],
        sources=result["sources"],
        is_in_scope=result["is_in_scope"]
    )


@app.get("/stats")
def get_stats(current_user: dict = Depends(get_current_user)):
    """Get system statistics."""
    # Count PDF files
    pdf_count = 0
    total_size_mb = 0

    if os.path.exists(PDF_FOLDER):
        for f in os.listdir(PDF_FOLDER):
            if f.lower().endswith(".pdf"):
                pdf_count += 1
                total_size_mb += os.path.getsize(os.path.join(PDF_FOLDER, f))

    total_size_mb = round(total_size_mb / (1024 * 1024), 2)

    # Count indexed chunks
    chunk_count = get_document_count()

    return {
        "pdf_count": pdf_count,
        "total_size_mb": total_size_mb,
        "indexed_chunks": chunk_count,
        "status": "ready" if chunk_count > 0 else "no_documents"
    }


# === Run the server ===
if __name__ == "__main__":
    import uvicorn
    print("Starting PDF RAG Chatbot API...")
    print(f"Server: http://localhost:{BACKEND_PORT}")
    print(f"API Docs: http://localhost:{BACKEND_PORT}/docs")
    uvicorn.run(app, host="0.0.0.0", port=BACKEND_PORT)
