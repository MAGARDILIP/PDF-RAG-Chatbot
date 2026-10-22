from langchain_community.embeddings import HuggingFaceEmbeddings
from config import EMBEDDING_MODEL

# I chose BAAI/bge-small-en-v1.5 because:
# - It runs 100% locally on your PC (no API calls, no cost)
# - It's small (33 million parameters) so it loads fast even without a GPU
# - It produces 384-dimensional vectors (good balance of quality and speed)
# - "bge" stands for "BAAI General Embedding" — a well-tested model

# This variable holds the loaded model (we load it once and reuse)
_embedding_model = None


def get_embedding_model():
    """Load and return the embedding model. Loads only once (cached)."""
    global _embedding_model

    if _embedding_model is None:
        print(f"Loading embedding model: {EMBEDDING_MODEL}")
        print("(This may take a minute the first time — it downloads the model)")

        _embedding_model = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={"device": "cpu"},  # Use CPU (no GPU needed)
            encode_kwargs={"normalize_embeddings": True}  # Normalize for better cosine similarity
        )

        print("Embedding model loaded successfully!")

    return _embedding_model


def embed_text(text):
    """Convert a single text string into a vector (list of numbers)."""
    model = get_embedding_model()
    return model.embed_query(text)


def embed_texts(texts):
    """Convert a list of text strings into vectors."""
    model = get_embedding_model()
    return model.embed_documents(texts)
