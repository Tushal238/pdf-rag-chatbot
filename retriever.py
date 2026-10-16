
import chromadb
from sentence_transformers import SentenceTransformer

DB_PATH = "chroma_db"
COLLECTION_NAME = "pdf_knowledge"
MODEL_NAME = "all-MiniLM-L6-v2"
MAX_COSINE_DISTANCE = 0.60


def retrieve_chunks(question, top_k=5):
    """Retrieve relevant chunks from indexed PDFs."""

    if not question or not question.strip():
        return []

    client = chromadb.PersistentClient(path=DB_PATH)

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}
    )

    count = collection.count()

    if count == 0:
        return []

    model = SentenceTransformer(MODEL_NAME)

    question_embedding = model.encode(
        question.strip(),
        normalize_embeddings=True
    ).tolist()

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=min(top_k, count),
        include=["documents", "metadatas", "distances"]
    )

    chunks = []

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    for text, metadata, distance in zip(
        documents, metadatas, distances
    ):
        if distance > MAX_COSINE_DISTANCE:
            continue

        chunks.append({
            "text": text,
            "source": metadata.get("source", "Unknown"),
            "page": metadata.get("page", "Unknown"),
            "distance": distance
        })

    return chunks


if __name__ == "__main__":
    question = input(
        "Ask a question about your PDFs: "
    ).strip()

    if not question:
        print("Please enter a question.")
    else:
        results = retrieve_chunks(question)

        if not results:
            print("No sufficiently similar chunks found.")
        else:
            print(f"Relevant chunks found: {len(results)}")

            for index, chunk in enumerate(results, start=1):
                print(f"\n--- Result {index} ---")
                print(f"Source: {chunk['source']}")
                print(f"Page: {chunk['page']}")
                print(
                    f"Cosine distance: "
                    f"{chunk['distance']:.4f}"
                )
                print(chunk["text"])
