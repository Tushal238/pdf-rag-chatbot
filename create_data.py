
from pathlib import Path
import pymupdf

output_dir = Path("data")
output_dir.mkdir(exist_ok=True)

pages = [
    {
        "title": "Introduction to Artificial Intelligence",
        "content": """
Artificial Intelligence (AI) is a field of computer science
that focuses on building systems capable of performing tasks
that normally require human intelligence.

Machine Learning is a subset of AI that allows computers to
learn patterns from data. Deep Learning is a subset of Machine
Learning that uses neural networks with multiple layers.
"""
    },
    {
        "title": "Retrieval-Augmented Generation",
        "content": """
Retrieval-Augmented Generation, also called RAG, combines
information retrieval with text generation using a language model.

A RAG system retrieves relevant information from an external
knowledge source and provides that information to a language
model as context before generating an answer.

RAG can help language models answer questions using private
documents and updated information without retraining the model.
"""
    },
    {
        "title": "Embeddings and Vector Databases",
        "content": """
An embedding represents text as a numerical vector.
Embedding models map semantically similar pieces of text
to nearby regions of a vector space.

A vector database stores embeddings and supports similarity
search. Examples include Chroma, Qdrant and Pinecone.

Cosine similarity is one measure used to compare the direction
of two vectors. It is commonly used in semantic retrieval.
"""
    },
    {
        "title": "Chunking and Retrieval",
        "content": """
Chunking divides a long document into smaller pieces of text.
These chunks are indexed separately to make retrieval more useful.

Chunk size affects how much context is available to the language
model. Overlap can help preserve information across chunk boundaries.

Top-k retrieval selects a specified number of candidate chunks.
A reranker can reorder retrieved candidates by relevance.
"""
    },
    {
        "title": "Limitations and Evaluation",
        "content": """
RAG does not guarantee correct answers. Incorrect or irrelevant
retrieved passages can lead to inaccurate responses.

RAG systems should be evaluated for retrieval relevance,
answer correctness, faithfulness to the supplied context,
latency and cost.

A reliable chatbot should acknowledge when the available
documents do not contain enough information to answer a question.
"""
    }
]

output_path = output_dir / "rag_guide.pdf"

with pymupdf.open() as pdf:
    for item in pages:
        page = pdf.new_page()
        page.insert_text(
            (50, 55),
            item["title"],
            fontsize=18,
            fontname="helv"
        )
        page.insert_textbox(
            pymupdf.Rect(50, 90, 545, 760),
            item["content"].strip(),
            fontsize=11,
            fontname="helv",
            lineheight=1.5
        )

    pdf.save(output_path)

print(f"Sample PDF created successfully: {output_path}")
print(f"Total pages created: {len(pages)}")
