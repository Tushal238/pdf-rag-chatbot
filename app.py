
import streamlit as st

from ingest import index_pdf_bytes
from retriever import retrieve_chunks
from generator import generate_answer
from ingest import index_pdf_bytes, delete_pdf

st.set_page_config(
    page_title="Multi-PDF RAG Chatbot",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Multi-PDF RAG Chatbot")
st.caption(
    "Ask questions across multiple PDFs using local AI."
)


# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "indexed_files" not in st.session_state:
    st.session_state.indexed_files = []


# Sidebar: PDF upload and indexing
with st.sidebar:
    st.header("📄 Document Manager")

    uploaded_files = st.file_uploader(
        "Upload PDF files",
        type=["pdf"],
        accept_multiple_files=True
    )

    if st.button("Process PDFs", type="primary"):
        if not uploaded_files:
            st.warning("Please upload at least one PDF.")
        else:
            progress = st.progress(0)
            processed_files = []
            failed_files = []
            total_chunks = 0

            for index, uploaded_file in enumerate(uploaded_files):
                try:
                    with st.spinner(
                        f"Processing {uploaded_file.name}..."
                    ):
                        chunk_count = index_pdf_bytes(
                            uploaded_file.getvalue(),
                            uploaded_file.name
                        )

                    if chunk_count > 0:
                        processed_files.append(
                            uploaded_file.name
                        )
                        total_chunks += chunk_count
                    else:
                        failed_files.append(
                            f"{uploaded_file.name}: no extractable text"
                        )

                except Exception as error:
                    failed_files.append(
                        f"{uploaded_file.name}: {error}"
                    )

                progress.progress(
                    (index + 1) / len(uploaded_files)
                )

            if processed_files:
                st.session_state.indexed_files = sorted(
                    set(st.session_state.indexed_files)
                    | set(processed_files)
                )

                st.success(
                    f"Processed {len(processed_files)} PDF(s). "
                    f"Indexed {total_chunks} chunks."
                )

            for failure in failed_files:
                st.warning(failure)

    st.divider()
    st.subheader("Indexed in this session")

    if st.session_state.indexed_files:
        for filename in st.session_state.indexed_files:
            st.write(f"📄 {filename}")
    else:
        st.caption(
            "No PDFs processed in this session yet."
        )

    st.caption(
        "Indexed document data is stored in ChromaDB."
    )

    if st.button("Clear chat"):
        st.session_state.messages = []
        st.rerun()


# Display previous conversation
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        sources = message.get("sources", [])

        if sources:
            with st.expander("📚 Retrieved sources"):
                for source in sources:
                    st.markdown(
                        f"**{source['source']}** — "
                        f"Page {source['page']}"
                    )

                    if source.get("distance") is not None:
                        st.caption(
                            "Cosine distance: "
                            f"{source['distance']:.4f}"
                        )


# Question input
question = st.chat_input(
    "Ask a question about your PDFs..."
)

if question:
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner(
            "Searching PDFs and generating an answer..."
        ):
            try:
                chunks = retrieve_chunks(
                    question,
                    top_k=5
                )

                answer = generate_answer(
                    question,
                    chunks
                )

                st.markdown(answer)

                sources = [
                    {
                        "source": chunk["source"],
                        "page": chunk["page"],
                        "distance": chunk.get("distance")
                    }
                    for chunk in chunks
                ]

                if sources:
                    with st.expander("📚 Retrieved sources"):
                        for source in sources:
                            st.markdown(
                                f"**{source['source']}** — "
                                f"Page {source['page']}"
                            )

                            if source.get("distance") is not None:
                                st.caption(
                                    "Cosine distance: "
                                    f"{source['distance']:.4f}"
                                )

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources
                })

            except Exception as error:
                st.error(
                    f"Something went wrong: {error}"
                )
