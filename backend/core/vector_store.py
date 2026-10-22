from langchain_community.vectorstores import Chroma
from core.embeddings import get_embedding_model
from config import VECTOR_STORE_PATH

# I chose ChromaDB because:
# - It's completely free and open-source
# - It stores data locally on your hard drive (no cloud needed)
# - It's the most popular vector database for learning RAG
# - Data persists between restarts (saved to data/vector_store/)

# This variable holds the ChromaDB instance (we create it once and reuse)
_vector_store = None


def get_vector_store():
    """Get or create the ChromaDB vector store. Creates only once (cached)."""
    global _vector_store

    if _vector_store is None:
        print("Connecting to ChromaDB vector store...")

        embedding_model = get_embedding_model()

        # Connect to ChromaDB (creates the database if it doesn't exist)
        _vector_store = Chroma(
            collection_name="pdf_documents",    # Name of our collection in the database
            embedding_function=embedding_model,  # The model that converts text to vectors
            persist_directory=VECTOR_STORE_PATH   # Where to save the database files
        )

        print(f"ChromaDB connected! Storage path: {VECTOR_STORE_PATH}")

    return _vector_store


def add_documents_to_store(chunks):
    """Add text chunks to the vector database."""
    if not chunks:
        print("No chunks to add.")
        return 0

    store = get_vector_store()

    # Add all chunks to ChromaDB
    # ChromaDB automatically converts text to vectors using our embedding model
    store.add_documents(chunks)

    total = store._collection.count()
    print(f"Added {len(chunks)} chunks. Total chunks in database: {total}")
    return len(chunks)


def search_similar(query, k=20):
    """Search for the most similar chunks to the query."""
    store = get_vector_store()

    # search_type="similarity" uses cosine similarity to find matching chunks
    # k=20 means return top 20 results (we'll rerank later to pick best 5)
    results = store.similarity_search_with_relevance_scores(query, k=k)

    print(f"Found {len(results)} similar chunks for query: '{query[:50]}...'")
    return results


def clear_vector_store():
    """Delete all data from the vector store (used when rebuilding the index)."""
    global _vector_store

    store = get_vector_store()

    # Get all document IDs and delete them
    collection = store._collection
    all_ids = collection.get()["ids"]

    if all_ids:
        collection.delete(ids=all_ids)
        print(f"Cleared {len(all_ids)} chunks from vector store.")
    else:
        print("Vector store is already empty.")

    # Reset the cached instance so it gets recreated fresh
    _vector_store = None


def get_document_count():
    """Get the total number of chunks stored in the database."""
    store = get_vector_store()
    return store._collection.count()
