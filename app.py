
import streamlit as st

from ingest import index_pdf_bytes, delete_pdf
from retriever import retrieve_chunks
from generator import generate_answer
from document_tools import generate_document_summary, compare_documents


# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="DocuMind AI",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ==================================================
# PREMIUM LIGHT THEME
# ==================================================

st.markdown(
    """
    <style>
    @import url(
        'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
    );

    :root {
        --primary: #4F46E5;
        --text: #202A44;
        --muted: #68738A;
        --border: #E5E9F2;
        --background: #F7F8FC;
    }

    .stApp {
        background: var(--background);
        color: var(--text);
        font-family: 'Inter', sans-serif;
    }

    [data-testid="stHeader"] {
        background: rgba(247, 248, 252, 0.9);
    }

    [data-testid="stSidebar"] {
        background: #FFFFFF;
        border-right: 1px solid var(--border);
    }

    .brand {
        font-size: 1.65rem;
        font-weight: 800;
        letter-spacing: -0.8px;
        color: var(--text);
    }

    .brand span {
        color: var(--primary);
    }

    .hero {
        background: linear-gradient(
            120deg,
            #FFFFFF 0%,
            #EFF2FF 65%,
            #F6F0FF 100%
        );
        border: 1px solid #E3E7FA;
        border-radius: 23px;
        padding: 28px 30px;
        margin: 10px 0 24px 0;
        box-shadow: 0 8px 28px rgba(48, 58, 110, 0.05);
    }

    .hero-label {
        color: var(--primary);
        font-weight: 700;
        font-size: 0.76rem;
        letter-spacing: 1.3px;
        text-transform: uppercase;
    }

    .hero h1 {
        color: var(--text);
        font-size: clamp(1.8rem, 4vw, 2.65rem);
        font-weight: 800;
        letter-spacing: -1.2px;
        line-height: 1.2;
        margin: 12px 0;
    }

    .hero p {
        color: var(--muted);
        font-size: 0.97rem;
        line-height: 1.7;
        max-width: 720px;
        margin-bottom: 0;
    }

    .section-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: var(--text);
        margin: 12px 0;
    }

    .metric-card {
        background: #FFFFFF;
        border: 1px solid var(--border);
        border-radius: 15px;
        padding: 17px;
        min-height: 100px;
        box-shadow: 0 3px 12px rgba(30, 41, 80, 0.025);
    }

    .metric-label {
        font-size: 0.8rem;
        color: var(--muted);
        margin-bottom: 8px;
    }

    .metric-value {
        color: var(--text);
        font-size: 1.55rem;
        font-weight: 800;
    }

    .feature-card {
        background: #FFFFFF;
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 18px;
        min-height: 125px;
        transition: transform 0.2s ease;
    }

    .feature-card:hover {
        transform: translateY(-3px);
    }

    .feature-icon {
        font-size: 1.4rem;
        margin-bottom: 8px;
    }

    .feature-title {
        font-size: 0.95rem;
        font-weight: 700;
        color: var(--text);
        margin-bottom: 5px;
    }

    .feature-description {
        color: var(--muted);
        font-size: 0.82rem;
        line-height: 1.55;
    }

    .stButton > button {
        border-radius: 11px;
        font-weight: 600;
        min-height: 40px;
        transition: all 0.2s ease;
    }

    .stButton > button[kind="primary"] {
        background: linear-gradient(110deg, #4F46E5, #6D5DFB);
        border: none;
        color: white;
    }

    .stButton > button[kind="primary"]:hover {
        box-shadow: 0 5px 15px rgba(79, 70, 229, 0.22);
    }

    [data-testid="stChatMessage"] {
        background: #FFFFFF;
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 12px 16px;
    }

    [data-testid="stExpander"] {
        background: #FFFFFF;
        border: 1px solid var(--border);
        border-radius: 12px;
    }

    [data-testid="stFileUploader"] {
        background: #F8F9FF;
        border: 1px dashed #C9D0F5;
        border-radius: 13px;
        padding: 8px;
    }

    .footer {
        text-align: center;
        color: #929BB0;
        font-size: 0.78rem;
        padding: 25px 0 10px 0;
    }

    
    /* DocuMind AI: premium 3D depth and motion */
    html { scroll-behavior: smooth; }
    .stApp {
        background:
            radial-gradient(ellipse at 8% 5%, rgba(91,76,230,.16), transparent 34%),
            radial-gradient(ellipse at 92% 12%, rgba(14,165,233,.10), transparent 32%),
            linear-gradient(145deg, #080D1D 0%, #10172B 48%, #0B1222 100%);
        color: #EDF2FF; font-family: 'Inter', sans-serif;
    }
    [data-testid="stHeader"] { background: rgba(8,13,29,.72); backdrop-filter: blur(18px); }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(17,24,43,.98), rgba(10,16,31,.98));
        border-right: 1px solid rgba(148,163,184,.17);
    }
    [data-testid="stSidebar"] * { color: #E5EBFF; }
    .brand, .section-title, .hero h1, .metric-value, .feature-title { color: #F4F7FF; }
    .brand span { color: #B8AEFF; text-shadow: 0 0 22px rgba(139,92,246,.55); }
    .hero {
        position: relative; overflow: hidden;
        background: radial-gradient(circle at 85% 18%, rgba(139,92,246,.28), transparent 28%),
                    linear-gradient(135deg, rgba(30,41,78,.96), rgba(17,25,48,.92));
        border: 1px solid rgba(167,139,250,.30); border-radius: 26px; padding: 32px;
        margin: 10px 0 26px; box-shadow: 0 22px 60px rgba(0,0,0,.26), inset 0 1px 0 rgba(255,255,255,.10);
        transition: transform 320ms ease, box-shadow 320ms ease, border-color 320ms ease;
        animation: documind-fade-up 650ms ease both;
    }
    .hero:hover {
        transform: perspective(1200px) rotateX(1deg) translateY(-2px);
        box-shadow: 0 28px 72px rgba(0,0,0,.34), 0 0 34px rgba(99,102,241,.10);
        border-color: rgba(167,139,250,.48);
    }
    .hero-label { color: #B8AEFF; }
    .hero p, .metric-label, .feature-description { color: #AAB6D1; }
    .metric-card, .feature-card {
        background: linear-gradient(145deg, rgba(28,38,67,.96), rgba(17,25,46,.96));
        border: 1px solid rgba(148,163,184,.18); border-radius: 18px;
        box-shadow: 0 14px 30px rgba(0,0,0,.18), inset 0 1px 0 rgba(255,255,255,.055);
        transform: perspective(1000px) translateZ(0);
        transition: transform 260ms cubic-bezier(.2,.8,.2,1), box-shadow 260ms ease, border-color 260ms ease;
        animation: documind-fade-up 550ms ease both;
    }
    .metric-card:hover, .feature-card:hover {
        transform: perspective(1000px) translateY(-6px) rotateX(1deg) rotateY(-.5deg);
        border-color: rgba(129,140,248,.48);
        box-shadow: 0 24px 44px rgba(0,0,0,.30), 0 0 24px rgba(99,102,241,.10), inset 0 1px 0 rgba(255,255,255,.10);
    }
    .metric-value { text-shadow: 0 0 20px rgba(129,140,248,.18); }
    .feature-icon { filter: drop-shadow(0 0 10px rgba(129,140,248,.26)); }
    .stButton > button {
        border-radius: 12px; border: 1px solid rgba(148,163,184,.22);
        background: rgba(30,41,69,.82); color: #EEF2FF; min-height: 42px;
        box-shadow: 0 6px 16px rgba(0,0,0,.12);
        transition: transform 180ms ease, box-shadow 220ms ease, border-color 220ms ease, filter 220ms ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px); border-color: rgba(167,139,250,.60);
        box-shadow: 0 10px 24px rgba(79,70,229,.20); filter: brightness(1.08);
    }
    .stButton > button:active { transform: translateY(0) scale(.985); }
    .stButton > button[kind="primary"] {
        background: linear-gradient(115deg, #635BFF 0%, #8B5CF6 52%, #3B82F6 100%);
        border: 1px solid rgba(196,181,253,.42); color: white;
        box-shadow: 0 9px 24px rgba(99,91,255,.28);
    }
    .stButton > button[kind="primary"]:hover { box-shadow: 0 13px 32px rgba(99,91,255,.38); }
    [data-testid="stChatMessage"] {
        background: linear-gradient(145deg, rgba(26,36,62,.96), rgba(16,24,44,.96));
        border: 1px solid rgba(148,163,184,.17); border-radius: 17px;
        box-shadow: 0 10px 24px rgba(0,0,0,.14); animation: documind-fade-up 320ms ease both;
    }
    [data-testid="stExpander"], [data-testid="stFileUploader"] {
        background: rgba(20,29,52,.72); border: 1px solid rgba(148,163,184,.20); border-radius: 14px;
    }
    [data-testid="stTabs"] [role="tablist"] { gap: 8px; border-bottom: 1px solid rgba(148,163,184,.18); }
    [data-testid="stTabs"] button[role="tab"] { border-radius: 12px 12px 0 0; color: #AAB6D1; transition: background 200ms ease, color 200ms ease; }
    [data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
        color: #FFFFFF; background: linear-gradient(180deg, rgba(99,91,255,.20), rgba(99,91,255,.04));
        border-bottom-color: #8B5CF6;
    }
    [data-testid="stMarkdownContainer"] p, [data-testid="stMarkdownContainer"] li { color: #D5DEF3; line-height: 1.72; }
    [data-testid="stCaptionContainer"], .footer { color: #8795B4; }
    [data-testid="stTextInput"] input, [data-testid="stChatInput"] textarea,
    [data-testid="stSelectbox"] div[data-baseweb="select"] > div {
        background: rgba(15,23,42,.88); color: #F1F5FF; border-color: rgba(148,163,184,.24); border-radius: 12px;
    }
    [data-testid="stProgress"] > div > div { background: linear-gradient(90deg, #6366F1, #A78BFA, #38BDF8); }
    .footer { border-top: 1px solid rgba(148,163,184,.13); margin-top: 28px; }
    @keyframes documind-fade-up {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @media (prefers-reduced-motion: reduce) {
        *, *::before, *::after { animation-duration: .01ms !important; animation-iteration-count: 1 !important; scroll-behavior: auto !important; transition-duration: .01ms !important; }
    }
    @media (max-width: 768px) { .hero { padding: 22px; border-radius: 20px; } .metric-card, .feature-card { border-radius: 14px; } }

    </style>
    """,
    unsafe_allow_html=True,
)


# ==================================================
# SESSION STATE
# ==================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "indexed_files" not in st.session_state:
    st.session_state.indexed_files = []

if "summary_results" not in st.session_state:
    st.session_state.summary_results = {}

if "pending_question" not in st.session_state:
    st.session_state.pending_question = None


# ==================================================
# HELPER FUNCTIONS
# ==================================================

def make_sources(chunks):
    """Prepare source information for display and history."""

    return [
        {
            "source": chunk.get("source", "Unknown"),
            "page": chunk.get("page", "Unknown"),
            "distance": chunk.get("distance"),
            "text": chunk.get("text", ""),
        }
        for chunk in chunks
    ]


def render_sources(sources):
    """Display retrieved PDF passages."""

    if not sources:
        st.caption("No source passages were retrieved.")
        return

    with st.expander(
        f"📚 Retrieved sources ({len(sources)})",
        expanded=False,
    ):
        for source in sources:
            st.markdown(
                f"**📄 {source['source']}** · "
                f"Page {source['page']}"
            )

            if source.get("distance") is not None:
                st.caption(
                    "Cosine distance: "
                    f"{source['distance']:.4f}"
                )

            if source.get("text"):
                st.markdown(
                    f"> {source['text']}"
                )

            st.divider()


# ==================================================
# SIDEBAR: UPLOAD AND DOCUMENT MANAGEMENT
# ==================================================

with st.sidebar:
    st.markdown(
        '<div class="brand">📘 DocuMind<span> AI</span></div>',
        unsafe_allow_html=True,
    )

    st.caption("Your intelligent document workspace")
    st.divider()

    st.markdown("### 📂 Document manager")

    uploaded_files = st.file_uploader(
        "Upload PDF documents",
        type=["pdf"],
        accept_multiple_files=True,
        key="pdf_uploader",
    )

    if st.button(
        "✨ Process documents",
        type="primary",
        use_container_width=True,
    ):
        if not uploaded_files:
            st.warning("Please upload at least one PDF.")
        else:
            progress = st.progress(0)
            processed_files = []
            failures = []
            total_chunks = 0

            for index, uploaded_file in enumerate(uploaded_files):
                try:
                    with st.spinner(
                        f"Indexing {uploaded_file.name}..."
                    ):
                        chunk_count = index_pdf_bytes(
                            uploaded_file.getvalue(),
                            uploaded_file.name,
                        )

                    if chunk_count > 0:
                        processed_files.append(uploaded_file.name)
                        total_chunks += chunk_count
                    else:
                        failures.append(
                            f"{uploaded_file.name}: no extractable text"
                        )

                except Exception as error:
                    failures.append(
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
                    f"Processed {len(processed_files)} PDF(s), "
                    f"{total_chunks} chunks."
                )

            for failure in failures:
                st.warning(failure)

    st.divider()
    st.markdown("### 📚 Indexed in this session")

    if st.session_state.indexed_files:
        for filename in list(st.session_state.indexed_files):
            with st.container(border=True):
                st.markdown(f"📄 **{filename}**")

                if st.button(
                    "🗑️ Remove document",
                    key=f"remove_{filename}",
                    use_container_width=True,
                ):
                    try:
                        delete_pdf(filename)

                        st.session_state.indexed_files.remove(filename)

                        # Remove stale summaries for this document.
                        st.session_state.summary_results.pop(
                            filename, None
                        )

                        # Remove chat messages whose sources include
                        # the deleted document.
                        cleaned_messages = []

                        for message in st.session_state.messages:
                            message_sources = message.get(
                                "sources", []
                            )

                            if not any(
                                source.get("source") == filename
                                for source in message_sources
                            ):
                                cleaned_messages.append(message)

                        st.session_state.messages = cleaned_messages

                        st.success(f"Removed {filename}")
                        st.rerun()

                    except Exception as error:
                        st.error(
                            f"Could not remove document: {error}"
                        )
    else:
        st.caption(
            "Upload and process a PDF to get started."
        )

    st.divider()

    if st.button(
        "🧹 Clear conversation",
        use_container_width=True,
    ):
        st.session_state.messages = []
        st.rerun()

    st.caption(
        "Local RAG pipeline · ChromaDB · Ollama"
    )


# ==================================================
# MAIN HEADER
# ==================================================

st.markdown(
    """
    <div class="hero">
        <div class="hero-label">YOUR AI DOCUMENT WORKSPACE</div>
        <h1>Understand your documents.<br>Get answers with evidence.</h1>
        <p>
            Ask questions about your PDFs, generate structured
            summaries, and inspect the source passages behind answers.
            Your configured local AI pipeline powers the experience.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ==================================================
# DASHBOARD METRICS
# ==================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">📄 Documents in session</div>
            <div class="metric-value">
                {len(st.session_state.indexed_files)}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">💬 Chat messages</div>
            <div class="metric-value">
                {len(st.session_state.messages)}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-label">🧠 Intelligence tools</div>
            <div class="metric-value">02</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ==================================================
# FEATURE CARDS
# ==================================================

st.markdown(
    '<div class="section-title">Explore your documents</div>',
    unsafe_allow_html=True,
)

feature1, feature2, feature3 = st.columns(3)

with feature1:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">💬</div>
            <div class="feature-title">Ask questions</div>
            <div class="feature-description">
                Search indexed PDFs using natural language and
                inspect supporting source passages.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with feature2:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">✨</div>
            <div class="feature-title">Summarize documents</div>
            <div class="feature-description">
                Generate an overview, key points, important details
                and a conclusion from a selected PDF.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with feature3:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">🔎</div>
            <div class="feature-title">Compare documents</div>
            <div class="feature-description">
                Multi-PDF comparison is the next feature planned
                for this workspace.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ==================================================
# WORKSPACE TABS
# ==================================================

tab_chat, tab_summary, tab_compare = st.tabs(
    ["Chat with PDFs", "Summarize PDF", "Compare PDFs"]
)


# ==================================================
# CHAT TAB
# ==================================================

with tab_chat:
    st.markdown(
        '<div class="section-title">Ask your documents</div>',
        unsafe_allow_html=True,
    )

    st.caption(
        "Answers are generated from the retrieved PDF context. "
        "Check the source passages to verify important information."
    )

    suggestions = [
        "What is retrieval augmented generation?",
        "What are embeddings and vector databases?",
        "What are the limitations of RAG?",
    ]

    suggestion_columns = st.columns(3)

    for index, suggestion in enumerate(suggestions):
        with suggestion_columns[index]:
            if st.button(
                suggestion,
                key=f"chat_suggestion_{index}",
                use_container_width=True,
            ):
                st.session_state.pending_question = suggestion
                st.rerun()

    st.divider()

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

            if message["role"] == "assistant":
                render_sources(message.get("sources", []))

    typed_question = st.chat_input(
        "Ask a question about your PDFs...",
        key="pdf_chat_input",
    )

    pending_question = st.session_state.pending_question
    st.session_state.pending_question = None

    question = typed_question or pending_question

    if question:
        st.session_state.messages.append(
            {
                "role": "user",
                "content": question,
            }
        )

        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner(
                "Searching PDFs and generating an answer..."
            ):
                try:
                    chunks = retrieve_chunks(
                        question,
                        top_k=5,
                    )

                    answer = generate_answer(
                        question,
                        chunks,
                    )

                    st.markdown(answer)

                    sources = make_sources(chunks)
                    render_sources(sources)

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": answer,
                            "sources": sources,
                        }
                    )

                except Exception as error:
                    error_message = (
                        "I could not complete the request. "
                        "Check that Ollama is running and the "
                        "indexed document data is available."
                    )

                    st.error(error_message)
                    st.caption(str(error))

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": error_message,
                            "sources": [],
                        }
                    )


# ==================================================
# SUMMARY TAB
# ==================================================

with tab_summary:
    st.markdown(
        '<div class="section-title">✨ Document summary</div>',
        unsafe_allow_html=True,
    )

    st.caption(
        "Generate a structured summary from the indexed content "
        "of one selected PDF."
    )

    if not st.session_state.indexed_files:
        st.info(
            "Upload and process a PDF using the sidebar first."
        )

    else:
        selected_pdf = st.selectbox(
            "Choose a document",
            options=st.session_state.indexed_files,
            key="summary_pdf_selection",
        )

        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">📖</div>
                <div class="feature-title">Structured summary</div>
                <div class="feature-description">
                    Overview · Key points · Important details · Conclusion
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button(
            "✨ Generate summary",
            type="primary",
            use_container_width=True,
            key="generate_pdf_summary",
        ):
            with st.spinner(
                "Reading indexed content and generating summary..."
            ):
                try:
                    result = generate_document_summary(
                        selected_pdf
                    )

                    st.session_state.summary_results[
                        selected_pdf
                    ] = result

                except Exception as error:
                    st.session_state.summary_results[
                        selected_pdf
                    ] = {
                        "success": False,
                        "content": str(error),
                        "pages": [],
                    }

        summary_result = st.session_state.summary_results.get(
            selected_pdf
        )

        if summary_result:
            st.divider()

            if summary_result.get("success"):
                st.success("Summary generated successfully.")

                st.markdown(
                    summary_result.get("content", "")
                )

                pages = summary_result.get("pages", [])

                if pages:
                    st.caption(
                        "Indexed pages used: "
                        + ", ".join(str(page) for page in pages)
                    )

                st.download_button(
                    "⬇️ Download summary",
                    data=summary_result.get("content", ""),
                    file_name="document_summary.md",
                    mime="text/markdown",
                    use_container_width=True,
                )

            else:
                st.error(
                    summary_result.get(
                        "content",
                        "Could not generate summary.",
                    )
                )


with tab_compare:
    st.subheader("Compare Two PDFs")
    st.write(
        "Do indexed documents select karo aur unke similarities "
        "aur differences analyze karo."
    )

    pdf_options = st.session_state.get("indexed_files", [])

    if len(pdf_options) < 2:
        st.info(
            "Comparison ke liye kam se kam 2 PDFs index karo. "
            "Sidebar se PDFs upload aur process kar sakte ho."
        )
    else:
        col_a, col_b = st.columns(2)

        with col_a:
            file_a = st.selectbox(
                "First PDF",
                options=pdf_options,
                key="compare_pdf_a",
            )

        with col_b:
            other_options = [
                filename
                for filename in pdf_options
                if filename != file_a
            ]

            file_b = st.selectbox(
                "Second PDF",
                options=other_options,
                key="compare_pdf_b",
            )

        if st.button(
            "Compare Documents",
            type="primary",
            use_container_width=True,
        ):
            with st.spinner(
                "AI is comparing both documents. Please wait..."
            ):
                result = compare_documents(file_a, file_b)

            if result["success"]:
                st.session_state["comparison_result"] = {
                    "file_a": file_a,
                    "file_b": file_b,
                    "content": result["content"],
                    "pages": result["pages"],
                }
            else:
                st.error(result["content"])

        comparison = st.session_state.get("comparison_result")

        if comparison:
            if (
                comparison["file_a"] in pdf_options
                and comparison["file_b"] in pdf_options
            ):
                st.markdown(
                    f"### {comparison['file_a']} vs "
                    f"{comparison['file_b']}"
                )
                st.markdown(comparison["content"])

                st.caption(
                    "Indexed pages available — "
                    f"{comparison['file_a']}: "
                    f"{len(comparison['pages'].get(comparison['file_a'], []))}, "
                    f"{comparison['file_b']}: "
                    f"{len(comparison['pages'].get(comparison['file_b'], []))}"
                )

                st.download_button(
                    "Download Comparison",
                    data=comparison["content"],
                    file_name="pdf_comparison.md",
                    mime="text/markdown",
                    use_container_width=True,
                )

/* Improve chat input styling for dark theme */
[data-testid="stChatInput"] {
    background: rgba(20, 29, 52, 0.96) !important;
    border: 1px solid rgba(148, 163, 184, 0.28) !important;
    border-radius: 16px !important;
    box-shadow: 0 10px 28px rgba(0, 0, 0, 0.22) !important;
}

[data-testid="stChatInput"] textarea {
    background: transparent !important;
    color: #F1F5FF !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #94A3B8 !important;
}

[data-testid="stChatInput"] button {
    background: linear-gradient(135deg, #6366F1, #8B5CF6) !important;
    color: white !important;
    border-radius: 10px !important;
}

/* Smooth tab interaction */
[data-testid="stTabs"] button[role="tab"] {
    transition: all 220ms ease !important;
}

[data-testid="stTabs"] button[role="tab"]:hover {
    background: rgba(139, 92, 246, 0.12) !important;
    color: #FFFFFF !important;
}
# ==================================================
# FOOTER
# ==================================================

st.markdown(
    """
    <div class="footer">
        DocuMind AI · Streamlit · ChromaDB · Ollama
    </div>
    """,
    unsafe_allow_html=True,
)

