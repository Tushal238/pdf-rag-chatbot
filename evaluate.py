
from retriever import retrieve_chunks
from generator import generate_answer


TEST_CASES = [
    {
        "question": "What is retrieval augmented generation?",
        "expected_source": "rag_guide.pdf"
    },
    {
        "question": "What are embeddings and vector databases?",
        "expected_source": "rag_guide.pdf"
    },
    {
        "question": "What are the limitations of RAG?",
        "expected_source": "rag_guide.pdf"
    }
]


def run_evaluation():
    total = len(TEST_CASES)
    source_hits = 0

    print("=" * 60)
    print("RAG CHATBOT EVALUATION")
    print("=" * 60)

    for index, test in enumerate(TEST_CASES, start=1):
        question = test["question"]
        expected_source = test["expected_source"]

        print(f"\nTest {index}/{total}")
        print(f"Question: {question}")

        chunks = retrieve_chunks(question, top_k=5)

        source_found = any(
            chunk["source"].lower() == expected_source.lower()
            for chunk in chunks
        )

        if source_found:
            source_hits += 1

        print(f"Retrieved chunks: {len(chunks)}")
        print(f"Expected source found: {source_found}")

        for chunk in chunks:
            print(
                f"  - {chunk['source']} | "
                f"Page {chunk['page']} | "
                f"Distance {chunk['distance']:.4f}"
            )

        answer = generate_answer(question, chunks)

        print("\nGenerated answer:")
        print(answer)
        print("-" * 60)

    source_hit_rate = (source_hits / total) * 100

    print("\nEVALUATION SUMMARY")
    print(f"Total test cases: {total}")
    print(f"Expected source found: {source_hits}/{total}")
    print(f"Source hit rate: {source_hit_rate:.2f}%")


if __name__ == "__main__":
    run_evaluation()
