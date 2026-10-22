# RAG Interview Cheat Sheet & Learning Guide

> Keep this file handy before any interview or presentation. It covers the core concepts of RAG and exactly what you need to learn to defend this project on your resume.

---

## 1. The Most Important Question: "What is RAG?"
**RAG stands for Retrieval-Augmented Generation.**
- **Retrieval:** Searching a database (ChromaDB) to find relevant documents.
- **Augmented:** Taking those documents and adding them to the user's prompt as context.
- **Generation:** Asking the LLM (Groq/Qwen) to generate an answer based *only* on that context.

**Simple explanation for a recruiter:**
"RAG is a technique that gives AI a temporary memory. Instead of relying on what the AI learned during training, we give it a specific document to read, and ask it to answer questions based *only* on that document. This prevents hallucinations."

---

## 2. The 3 Phases of the RAG Pipeline
You must memorize these three phases. If they ask how your project works, say this:

### Phase A: Ingestion (Data Prep)
1. **Load:** PyPDF extracts raw text from the PDFs.
2. **Chunk:** We split the text into smaller pieces (800 characters) with overlap (150 chars). *Why? Because LLMs can't read 500 pages at once due to memory/token limits.*
3. **Embed:** We use an AI model (`SentenceTransformers`) to convert each text chunk into a list of numbers (a vector).
4. **Store:** We save these vectors in a vector database (`ChromaDB`).

### Phase B: Retrieval (Searching)
1. When a user asks a question, we convert the question into a vector using the *same* AI model.
2. ChromaDB compares the question vector to all document vectors using a mathematical formula called **Cosine Similarity**.
3. It returns the top 20 most similar chunks.
4. **Reranking (Bonus points!):** We use a second model (`CrossEncoder`) to re-score and re-order those 20 chunks, keeping only the top 5 absolute best matches.

### Phase C: Generation (Answering)
1. We take the top 5 chunks and inject them into a prompt.
2. The prompt says: *"Here is some context: [Top 5 chunks]. Now answer this question: [User Question]."*
3. We send this to Groq API. The LLM reads the context and generates the final answer.

---

## 3. Key Concepts You MUST Understand

### What is a Vector Embedding?
AI doesn't understand English words; it understands math. An embedding is a high-dimensional mathematical representation of a sentence's *meaning*. 
- For example, the vector for "Dog" and "Puppy" will look very similar mathematically, even though the letters are totally different. This is how "Semantic Search" works.

### What is Cosine Similarity?
It's a mathematical formula used to measure how similar two vectors are. If the angle between two vectors is small (cosine is close to 1), they have a similar meaning. If the angle is large (cosine close to 0), they are unrelated.

### Why do we Chunk with "Overlap"?
If we just cut a document every 800 characters, we might cut a sentence exactly in half:
- Chunk 1: "The capital of France is "
- Chunk 2: "Paris, a beautiful city."
If someone searches for "Capital of France", it might only retrieve Chunk 1, which doesn't contain the answer! By overlapping chunks by 150 characters, we ensure context is never broken.

### Why use a CrossEncoder (Reranker)?
Initial vector search (Bi-Encoder) is very fast but sometimes dumb. It might return a document that shares similar words but means something different. A CrossEncoder is slower but incredibly smart—it reads the question and the document *together* and gives a highly accurate relevance score. We use the fast method to find 20 candidates, and the smart method to pick the final 5.

---

## 4. Full-Stack Questions (Because you built a full app)

**Q: Why FastAPI?**
A: FastAPI is a modern Python framework designed specifically for building REST APIs. It is incredibly fast, has built-in data validation (using Pydantic), and handles asynchronous code automatically.

**Q: Why React over Streamlit?**
A: Streamlit is great for quick data science demos, but React is the industry standard for production applications. Using React allowed me to build a custom ChatGPT-style UI with better state management, proper API integration, and full control over styling with Tailwind CSS.

**Q: How did the frontend and backend talk to each other?**
A: They communicate via REST API. The React frontend sends a JSON payload via an HTTP POST request (e.g., using `fetch` or `axios`) to the FastAPI backend. FastAPI processes the request through the RAG pipeline and returns a JSON response containing the answer and the sources.

**Q: Did you face any CORS issues?**
*(CORS is a security feature in browsers. Since React runs on port 5173 and FastAPI runs on port 8000, the browser will block communication by default).*
A: Yes, I had to configure CORS Middleware in FastAPI to explicitly allow requests from my React frontend's port (localhost:5173).

---

## 5. Homework: What to Google before interviews
If you have an interview coming up, spend 10 minutes Googling these terms to familiarize yourself with how people talk about them:
1. *"Vector Embeddings explained simply"*
2. *"What is ChromaDB"*
3. *"LangChain vs LlamaIndex"* (We used LangChain)
4. *"RAG Hallucination prevention"*
5. *"FastAPI vs Flask"*
