from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import CHUNK_SIZE, CHUNK_OVERLAP

# I chose RecursiveCharacterTextSplitter because:
# - It tries to split on natural boundaries (paragraphs, sentences, words)
# - It doesn't just chop text at exactly 800 characters blindly
# - The "recursive" part means it first tries to split by paragraphs (\n\n),
#   then by sentences (\n), then by words (" "), ensuring clean breaks


def split_documents(pages):
    """Split loaded PDF pages into smaller chunks for embedding."""

    # Create the splitter with our settings from config.py
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,       # 800 characters per chunk
        chunk_overlap=CHUNK_OVERLAP, # 150 character overlap between chunks
        length_function=len,         # Use character count (not token count)
        separators=["\n\n", "\n", " ", ""]  # Try paragraph first, then line, then word
    )

    # Split all pages into chunks
    # Each chunk keeps the metadata (source file, page number) from the original page
    chunks = splitter.split_documents(pages)

    # Add a unique ID to each chunk so we can track it
    for i, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = i

    print(f"Split {len(pages)} pages into {len(chunks)} chunks")
    print(f"  Chunk size: {CHUNK_SIZE} characters")
    print(f"  Overlap: {CHUNK_OVERLAP} characters")

    return chunks
