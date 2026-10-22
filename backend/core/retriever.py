from sentence_transformers import CrossEncoder
from core.vector_store import search_similar
from config import RERANKER_MODEL, INITIAL_RETRIEVAL_COUNT, TOP_K, SIMILARITY_THRESHOLD

# I chose CrossEncoder (ms-marco-MiniLM-L-6-v2) for reranking because:
# - Normal vector search (Bi-Encoder) is fast but sometimes returns wrong matches
# - CrossEncoder reads the question AND the document TOGETHER
# - This gives much more accurate relevance scores
# - We use the fast method to find 20 candidates, then CrossEncoder picks the best 5

# Load the reranker model once and reuse
_reranker = None


def get_reranker():
    """Load and return the CrossEncoder reranker model. Loads only once."""
    global _reranker

    if _reranker is None:
        print(f"Loading reranker model: {RERANKER_MODEL}")
        _reranker = CrossEncoder(RERANKER_MODEL)
        print("Reranker model loaded successfully!")

    return _reranker


def retrieve_and_rerank(query):
    """
    Two-stage retrieval:
    1. ChromaDB finds top 20 similar chunks (fast but rough)
    2. CrossEncoder reranks them and picks the best 5 (slow but accurate)

    Returns:
        - is_in_scope: True if the question can be answered from the documents
        - top_chunks: List of the best matching chunks with scores
    """

    # Stage 1: Get top 20 candidates from ChromaDB using cosine similarity
    raw_results = search_similar(query, k=INITIAL_RETRIEVAL_COUNT)

    # If no results found at all, the question is definitely out-of-scope
    if not raw_results:
        print("No results found in vector store. Question is out-of-scope.")
        return False, []

    # Stage 2: Rerank using CrossEncoder
    reranker = get_reranker()

    # Prepare pairs of (question, document_text) for the reranker
    pairs = [[query, doc.page_content] for doc, score in raw_results]

    # Get reranker scores (higher = more relevant)
    rerank_scores = reranker.predict(pairs)

    # Combine the original documents with their new reranker scores
    reranked = []
    for i, (doc, original_score) in enumerate(raw_results):
        reranked.append({
            "content": doc.page_content,
            "metadata": doc.metadata,
            "rerank_score": float(rerank_scores[i]),
            "original_score": float(original_score)
        })

    # Sort by reranker score (highest first) and take top K
    reranked.sort(key=lambda x: x["rerank_score"], reverse=True)
    top_chunks = reranked[:TOP_K]

    # Check if the best chunk's score is above our threshold
    # If the best match is still below the threshold, the question is out-of-scope
    best_score = top_chunks[0]["rerank_score"] if top_chunks else 0

    if best_score < SIMILARITY_THRESHOLD:
        print(f"Best rerank score ({best_score:.3f}) is below threshold ({SIMILARITY_THRESHOLD})")
        print("Question is OUT-OF-SCOPE — not found in uploaded documents.")
        return False, top_chunks

    print(f"Question is IN-SCOPE. Best rerank score: {best_score:.3f}")
    print(f"Returning top {len(top_chunks)} chunks for answer generation.")

    return True, top_chunks
