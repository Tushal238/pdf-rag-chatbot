
from retriever import retrieve_chunks
from generator import generate_answer


TEST_CASES = [
    {
        "question": "What is retrieval augmented generation?",
        "expected_source": "rag_guide.pdf",
        "should_retrieve": True,
    },
    {
        "question": "What are embeddings and vector databases?",
        "expected_source": "rag_guide.pdf",
        "should_retrieve": True,
    },
    {
        "question": "What are the limitations of RAG?",
        "expected_source": "rag_guide.pdf",
        "should_retrieve": True,
    },
    {
        "question": "Who won the FIFA World Cup in 2018?",
        "expected_source": None,
        "should_retrieve": False,
    },
]


def run_evaluation():
    answerable_tests = [
        test for test in TEST_CASES if test["should_retrieve"]
    ]
    fallback_tests = [
        test for test in TEST_CASES if not test["should_retrieve"]
    ]

    hits = 0
    reciprocal_ranks = []
    best_match_distances = []
    fallback_passes = 0

    print("=" * 65)
    print("RAG CHATBOT EVALUATION")
    print("=" * 65)

    for index, test in enumerate(TEST_CASES, start=1):
        question = test["question"]
        expected_source = test["expected_source"]

        print(f"\nTest {index}/{len(TEST_CASES)}")
        print(f"Question: {question}")

        chunks = retrieve_chunks(question, top_k=5)
        print(f"Retrieved chunks: {len(chunks)}")

        for rank, chunk in enumerate(chunks, start=1):
            print(
                f"  {rank}. {chunk['source']} | "
                f"Page {chunk['page']} | "
                f"Distance {chunk['distance']:.4f}"
            )

        if test["should_retrieve"]:
            matching = [
                (rank, chunk)
                for rank, chunk in enumerate(chunks, start=1)
                if chunk["source"].lower()
                == expected_source.lower()
            ]

            if matching:
                hits += 1
                first_rank = matching[0][0]
                reciprocal_ranks.append(1 / first_rank)

                best_distance = min(
                    chunk["distance"]
                    for _, chunk in matching
                )
                best_match_distances.append(best_distance)

                print(f"Expected source: PASS (rank {first_rank})")
                print(f"Best-match distance: {best_distance:.4f}")
            else:
                reciprocal_ranks.append(0)
                print("Expected source: FAIL")

            answer = generate_answer(question, chunks)
            print("\nGenerated answer:")
            print(answer)

        else:
            answer = generate_answer(question, chunks)
            print("\nGenerated answer:")
            print(answer)

            expected_fallback = (
                "I could not find sufficiently relevant information "
                "in the uploaded PDFs to answer this question."
            )

            if not chunks and " ".join(answer.split()) == expected_fallback:
                fallback_passes += 1
                print("Out-of-context test: PASS")
            else:
                print("Out-of-context test: FAIL")

        print("-" * 65)

    total_answerable = len(answerable_tests)
    hit_rate = (
        hits / total_answerable * 100
        if total_answerable else 0
    )
    mrr = (
        sum(reciprocal_ranks) / total_answerable
        if total_answerable else 0
    )

    print("\nEVALUATION SUMMARY")
    print(f"Total test cases: {len(TEST_CASES)}")
    print(
        f"Hit@5: {hits}/{total_answerable} "
        f"({hit_rate:.2f}%)"
    )
    print(f"MRR@5: {mrr:.4f}")
    print(
        f"Out-of-context tests passed: "
        f"{fallback_passes}/{len(fallback_tests)}"
    )

    if best_match_distances:
        average_distance = (
            sum(best_match_distances) / len(best_match_distances)
        )
        print(f"Average best-match distance: {average_distance:.4f}")
    else:
        print("Average best-match distance: N/A")


if __name__ == "__main__":
    run_evaluation()
