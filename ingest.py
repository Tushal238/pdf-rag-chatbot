
import hashlib

import chromadb
import pymupdf
from sentence_transformers import SentenceTransformer


# Configuration
CHUNK_SIZE = 120
CHUNK_OVERLAP = 30

DB_PATH = "chroma_db"
COLLECTION_NAME = "pdf_knowledge"
MODEL_NAME = "all-MiniLM-L6-v2"


def get_collection():
    """Connect to the persistent ChromaDB collection."""
    client = chromadb.PersistentClient(path=DB_PATH)

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}
    )

    return collection


def chunk_text(text):
    """Split text into overlapping word-based chunks."""
    words = text.split()
    chunks = []

    start = 0

    while start < len(words):
        end = start + CHUNK_SIZE
        chunk = " ".join(words[start:end])

        if chunk.strip():
            chunks.append(chunk)

        if end >= len(words):
            break

        start = end - CHUNK_OVERLAP

    return chunks


def index_pdf_bytes(pdf_bytes, filename):
    """
    Extract text from an uploaded PDF, create chunks,
    generate embeddings, and store them in ChromaDB.

    Reprocessing the same filename replaces its old chunks.
    """

    collection = get_collection()

    document = pymupdf.open(
        stream=pdf_bytes,
        filetype="pdf"
    )

    try:
        documents = []
        metadatas = []
        ids = []

        # Create a unique prefix for this PDF content.
        file_hash = hashlib.sha256(
            pdf_bytes
        ).hexdigest()[:12]

        # Extract text page by page.
        for page_number, page in enumerate(
            document, start=1
        ):
            text = page.get_text("text").strip()

            if not text:
                continue

            chunks = chunk_text(text)

            for chunk_number, chunk in enumerate(chunks):
                documents.append(chunk)

                metadatas.append({
                    "source": filename,
                    "page": page_number
                })

                ids.append(
                    f"{file_hash}_page{page_number}"
                    f"_chunk{chunk_number}"
                )

        # Do not delete existing data if the new PDF
        # contains no extractable text.
        if not documents:
            return 0

        # Generate embeddings for every chunk.
        model = SentenceTransformer(MODEL_NAME)

        embeddings = model.encode(
            documents,
            normalize_embeddings=True
        ).tolist()

        # Remove old chunks for this filename.
        # This also handles PDFs with fewer chunks
        # than their previous versions.
        collection.delete(
            where={"source": filename}
        )

        # Store the latest chunks and metadata.
        collection.upsert(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
            embeddings=embeddings
        )

        return len(documents)

    finally:
        document.close()

def delete_pdf(filename):
    """Delete all indexed chunks belonging to a PDF filename."""

    collection = get_collection()

    collection.delete(
        where={"source": filename}
    )

    return True


if __name__ == "__main__":
    print("Multi-PDF ingestion module is ready.")
    print(f"Database: {DB_PATH}")
    print(f"Collection: {COLLECTION_NAME}")
