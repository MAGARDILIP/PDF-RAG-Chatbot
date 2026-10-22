# PDF RAG Chatbot — Complete Project Description

## 1. Problem Statement
Large Language Models (LLMs) like ChatGPT are incredibly smart, but they suffer from two major limitations:
1. **Hallucination:** They sometimes make up fake facts when they don't know the answer.
2. **Lack of Private Knowledge:** They cannot read your personal documents, offline files, or private company data.

When a user has a 500-page document (like a legal contract, a medical research paper, or an IT manual) and needs to find a specific answer, reading it manually takes hours. Standard LLMs cannot help because they haven't read that specific document.

## 2. Objectives
Our objective is to build a full-stack **Retrieval-Augmented Generation (RAG)** chatbot that solves these problems by:
1. Allowing users to upload multiple large PDF documents.
2. Converting the text into mathematical vectors (embeddings) and storing them in a local database.
3. Performing "semantic search" to find the exact paragraphs that contain the answer to the user's question.
4. Using an LLM to read ONLY those specific paragraphs and generate a human-readable, accurate answer.
5. Providing the exact source (page number and file name) so the user can verify the answer.

## 3. Why Our Project is Different (Defending Your Work)
If a professor asks, *"Aren't you just uploading a PDF and sending it to ChatGPT?"*, the answer is a strong **NO**. 

**You can tell your professor:**
> *"No, we are not just sending a PDF to ChatGPT. LLMs cannot read 500-page documents because of memory limits and cost. Instead, I built a full NLP pipeline. My code intelligently chunks the text, uses a local AI model to convert the text into mathematical vectors, stores them in a ChromaDB database, performs cosine-similarity semantic search, and then uses a second AI model (CrossEncoder) to re-rank the results for accuracy before an LLM even touches it."*

This proves that the core intelligence of the app was built by you, not just Groq. We built a React frontend and a Python FastAPI backend communicating via REST APIs, making it a true enterprise-grade full-stack application.

## 4. Enterprise Deployment (Company Handover)
If asked, *"Do companies have to upload PDFs every time?"*, the answer is **NO**.

**You can explain:**
> *"In a real company, employees do not upload PDFs every time they use it. An IT admin would run a script to ingest all 10,000 company documents into the ChromaDB vector database overnight. Because the database is saved permanently on the server's hard drive, employees just open the chat interface and start asking questions instantly. The 'Upload' button is just an admin tool to add new knowledge to the existing database dynamically."*

## 5. Glossary of Technical Terms (Cheat Sheet for You)
Since you will need to explain this project to recruiters and professors, here is a simple explanation of every technical word used in this project:

- **LLM (Large Language Model):** AI models like ChatGPT or Groq (Qwen). They are trained on the internet and are good at writing human-like text, but they don't know your private data.
- **NLP (Natural Language Processing):** The field of computer science that deals with teaching computers to understand human language. Our entire project is an "NLP pipeline."
- **RAG (Retrieval-Augmented Generation):** The name of the architecture we are building. It means: first, **Retrieve** the right document paragraph, then **Augment** (add) it to the prompt, and finally ask the LLM to **Generate** an answer.
- **Chunking:** Splitting a large 500-page PDF into tiny paragraphs (e.g., 800 characters each). We do this because AI cannot read 500 pages all at once. We also use "overlap" so if a sentence gets cut in half, the next chunk has the other half.
- **Embeddings / Vector Mathematics:** AI doesn't understand English; it understands numbers. An "embedding" is a way of converting a chunk of text into a list of numbers (a vector). For example, the word "King" might become `[0.1, 0.8, -0.2]`. If two vectors have similar numbers, it means the sentences have similar *meanings*.
- **ChromaDB (Vector Database):** A special type of database designed to store these number lists (vectors) permanently on the hard drive. Normal databases (like MySQL or MongoDB) store text; vector databases store AI numbers.
- **Cosine-Similarity Search:** The mathematical formula our database uses to find the right answer. When you ask a question, we turn your question into numbers (a vector) and find which document chunks have the most "similar" numbers.
- **CrossEncoder (Reranking):** An advanced AI technique. After the database finds the top 20 matches, it might make a few mistakes. We use a second, very strict AI model (CrossEncoder) to double-check those 20 matches and rank them perfectly from best to worst.
- **Prompt Engineering:** The strict instructions we write for the LLM. Instead of just asking it the question, we tell it: *"You are an assistant. Read ONLY this specific text I found. If the answer is not there, say you don't know."*

## 6. Do We Fully Depend on Groq?
No. The architecture is highly modular. The **only** thing Groq does is the final step: reading the retrieved context and formatting the final answer. The text extraction, embedding generation, database storage, and reranking all happen locally on your PC. 

We use Groq because it provides access to open-source models at incredibly fast speeds for free. If Groq goes down, we can swap it out for OpenAI or a local model (like Ollama) just by changing one line in the code.

## 7. Security and Data Integrity
When handling sensitive documents (like healthcare records or legal contracts), security is critical:
- **Local Storage:** The uploaded PDFs are stored locally on the server. They are NOT uploaded to the cloud.
- **Local Embeddings:** The text is converted into vectors and stored locally in ChromaDB.
- **No Training:** The LLM (Groq) is used only for inference. Our private data is not used to train their models.
- **Source Verification:** The chatbot always provides the source file and page number so the user can click and verify the original text themselves.
