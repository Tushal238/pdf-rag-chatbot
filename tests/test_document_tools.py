
from document_tools import (
    get_document_chunks,
    build_document_context,
    compare_documents,
)


def test_build_document_context_includes_source_and_page():
    chunks = [
        {
            "text": "RAG combines retrieval and generation.",
            "source": "guide.pdf",
            "page": 2,
        }
    ]

    context = build_document_context(chunks)

    assert "guide.pdf" in context
    assert "Page: 2" in context
    assert "RAG combines retrieval and generation." in context


def test_build_document_context_empty_input():
    assert build_document_context([]) == ""


def test_compare_same_pdf_returns_validation_error():
    result = compare_documents("guide.pdf", "guide.pdf")

    assert result["success"] is False
    assert "different PDF" in result["content"]


def test_get_document_chunks_returns_a_list():
    # Uses the project's local ChromaDB collection.
    chunks = get_document_chunks("file-that-does-not-exist.pdf")

    assert isinstance(chunks, list)
    assert chunks == []
