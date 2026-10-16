
import chromadb
from sentence_transformers import SentenceTransformer


DB_PATH = "chroma_db"
COLLECTION_NAME = "pdf_knowledge"
MODEL_NAME = "all-MiniLM-L6-v2"


def retrieve_chunks(question, top_k=5):
    """Retrieve the most relevant chunks for a question."""

    client = chromadb.PersistentClient(path=DB_PATH)

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}
    )

    if collection.count() == 0:
        return []

    model = SentenceTransformer(MODEL_NAME)

    question_embedding = model.encode(
        question,
        normalize_embeddings=True
    ).tolist()

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=min(top_k, collection.count()),
        include=[
            "documents",
            "metadatas",
            "distances"
        ]
    )

    chunks = []

    for i, text in enumerate(results["documents"][0]):
        metadata = results["metadatas"][0][i]
        distance = results["distances"][0][i]

        chunks.append({
            "text": text,
            "source": metadata.get("source", "Unknown"),
            "page": metadata.get("page", "Unknown"),
            "distance": distance
        })

    return chunks


if __name__ == "__main__":
    question = input("Ask a question about your PDFs: ")

    results = retrieve_chunks(question)

    if not results:
        print("No indexed documents found.")
    else:
        for index, chunk in enumerate(results, start=1):
            print(f"\n--- Result {index} ---")
            print(f"Source: {chunk['source']}")
            print(f"Page: {chunk['page']}")
            print(f"Cosine distance: {chunk['distance']:.4f}")
            print(chunk["text"])
