from groq import Groq
from core.retriever import retrieve_and_rerank
from config import GROQ_API_KEY, LLM_MODEL, TEMPERATURE

# I chose Groq API because:
# - It's free and gives access to powerful open-source LLMs
# - It's incredibly fast (uses custom LPU chips)
# - If Groq ever goes down, we can swap to OpenAI or Ollama by changing just this file

# The system prompt tells the LLM exactly how to behave
# This is our main guardrail against hallucination
SYSTEM_PROMPT = """You are a helpful assistant for Pimpri Chinchwad College of Engineering (PCCOE), Department of MCA.

STRICT RULES:
1. Answer ONLY based on the provided document context below.
2. Do NOT use any outside knowledge, general knowledge, or information from your training data.
3. If the answer is NOT found in the provided context, respond EXACTLY with:
   "I cannot answer this question because the information was not found in our uploaded department documents. I am restricted to answering questions strictly from the college/department knowledge base."
4. Always cite the source document name and page number when answering.
5. Keep your answers clear, accurate, and professional.
6. If the context partially answers the question, provide what you can and mention that some information may be incomplete.
7. Be THOROUGH — when listing items (subjects, courses, topics, etc.), include ALL items found across ALL the context chunks. Do not stop early.
8. Look carefully at ALL provided context sources, not just the first few.

DOCUMENT CONTEXT:
{context}
"""

# The out-of-scope message (shown when question can't be answered from documents)
OUT_OF_SCOPE_MESSAGE = (
    "I cannot answer this question because the information was not found in our "
    "uploaded department documents. I am restricted to answering questions strictly "
    "from the college/department knowledge base."
)


def format_context(chunks):
    """Format the retrieved chunks into a readable context string for the LLM."""
    context_parts = []

    for i, chunk in enumerate(chunks, 1):
        source = chunk["metadata"].get("source_file", "Unknown")
        page = chunk["metadata"].get("page", "?")

        context_parts.append(
            f"[Source {i}: {source}, Page {int(page) + 1}]\n{chunk['content']}\n"
        )

    return "\n---\n".join(context_parts)


def format_sources(chunks):
    """Extract unique sources from chunks for the response."""
    sources = []
    seen = set()

    for chunk in chunks:
        source = chunk["metadata"].get("source_file", "Unknown")
        page = chunk["metadata"].get("page", "?")
        key = f"{source}_page_{page}"

        if key not in seen:
            seen.add(key)
            sources.append({
                "file": source,
                "page": int(page) + 1,  # Convert from 0-indexed to 1-indexed
                "snippet": chunk["content"][:150] + "..."  # Short preview of the text
            })

    return sources


def generate_answer(question):
    """
    Main function: Takes a user question and returns an answer with sources.

    Flow:
    1. Retrieve relevant chunks from ChromaDB
    2. Rerank chunks using CrossEncoder
    3. Check if the question is in-scope
    4. If in-scope: send to Groq LLM with context
    5. If out-of-scope: return the standard out-of-scope message
    """

    # Step 1 & 2: Retrieve and rerank
    is_in_scope, top_chunks = retrieve_and_rerank(question)

    # Step 3: If out-of-scope, return the guardrail message immediately
    # Don't even bother sending to the LLM — this saves API calls and prevents hallucination
    if not is_in_scope:
        return {
            "answer": OUT_OF_SCOPE_MESSAGE,
            "sources": [],
            "is_in_scope": False
        }

    # Step 4: Format the context from our top chunks
    context = format_context(top_chunks)
    sources = format_sources(top_chunks)

    # Step 5: Send to Groq LLM
    try:
        client = Groq(api_key=GROQ_API_KEY)

        # Build the messages with our strict system prompt + context
        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT.format(context=context)
            },
            {
                "role": "user",
                "content": question
            }
        ]

        # Call Groq API
        print(f"Sending to Groq LLM ({LLM_MODEL})...")
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=messages,
            temperature=TEMPERATURE,
            max_tokens=2048
        )

        answer = response.choices[0].message.content
        print("Answer generated successfully!")

        return {
            "answer": answer,
            "sources": sources,
            "is_in_scope": True
        }

    except Exception as e:
        print(f"Error calling Groq API: {e}")
        return {
            "answer": f"Sorry, an error occurred while generating the answer: {str(e)}",
            "sources": [],
            "is_in_scope": True
        }
