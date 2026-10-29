# DocuMind AI — Local PDF RAG Assistant

A document intelligence application that lets users ask questions about PDF files, generate structured summaries, and compare two documents using a locally running language model.

## Overview

DocuMind AI combines Retrieval-Augmented Generation (RAG), semantic search, vector storage, and local LLM inference to help users explore their documents through a Streamlit interface.

## Application Preview

### Dashboard
![DocuMind AI Dashboard](screenshots/dashboard.png)

### Chat with PDFs
![PDF Chat](screenshots/chat.png)

### PDF Summary
![PDF Summary](screenshots/summary.png)

### PDF Comparison
![PDF Comparison](screenshots/comparison.png)


## Features

- **PDF Upload and Indexing:** Extract and index PDF text for retrieval.
- **Ask Questions:** Ask natural-language questions about indexed documents.
- **Source Passages:** Inspect retrieved passages, filenames, and page references supporting answers.
- **PDF Summarization:** Generate structured summaries with an overview, key points, important details, and conclusion.
- **PDF Comparison:** Compare two PDFs for similarities, differences, and unique information.
- **Markdown Export:** Download generated summaries and comparisons.
- **Local LLM Inference:** Use Ollama with the `llama3.2:3b` model.
- **Interactive UI:** Use a Streamlit-based document workspace.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Streamlit | Web interface |
| ChromaDB | Vector database and persistent storage |
| Sentence Transformers | Text embeddings |
| Ollama | Local language model inference |
| Llama 3.2 3B | Answer generation, summarization, and comparison |
| PyMuPDF | PDF text extraction |

## Architecture

```text
                PDF Documents
                      |
                      v
             PDF Text Extraction
                      |
                      v
              Text Chunking
                      |
                      v
           Sentence Transformer
                 Embeddings
                      |
                      v
               ChromaDB Store
                      |
          +-----------+-----------+
          |           |           |
          v           v           v
       PDF Chat    Summarize    Compare PDFs
          |           |           |
          v           v           v
       Retrieve    Document     Two-document
       Relevant     Context      Contexts
       Chunks          |           |
          |            +-----+-----+
          +------------------+
                     |
                     v
               Ollama LLM
                     |
                     v
             Streamlit Results
```

## Project Structure

```text
pdf-rag-chatbot/
├── app.py
├── ingest.py
├── retriever.py
├── generator.py
├── document_tools.py
├── evaluate.py
├── create_data.py
├── requirements.txt
├── README.md
├── .gitignore
└── data/
    └── rag_guide.pdf
```

The `chroma_db/` directory stores the local vector database and should not be committed to Git.

## Requirements

- Python 3.11 or a compatible Python version supported by the installed dependencies
- Ollama installed and running
- Git
- Required Python packages listed in `requirements.txt`

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Tushal238/pdf-rag-chatbot.git
cd pdf-rag-chatbot
```

### 2. Create a virtual environment

Windows:

```cmd
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Install and start the Ollama model

Pull the model:

```bash
ollama pull llama3.2:3b
```

Ensure Ollama is running before using the application. If it is not running automatically, start it with:

```bash
ollama serve
```

If the model is already downloaded, you do not need to pull it again.

### 5. Launch the application

```bash
python -m streamlit run app.py --server.fileWatcherType none
```

Open the local URL shown in the terminal, usually:

`http://localhost:8501`

## How to Use

1. Open DocuMind AI in your browser.
2. Upload one or more PDF documents using the sidebar.
3. Click **Process documents** to extract, chunk, embed, and index the content.
4. Open **Chat with PDFs** to ask questions about your documents.
5. Inspect the retrieved source passages and page references.
6. Open **Summarize PDF** to generate a structured summary.
7. Open **Compare PDFs**, select two different indexed documents, and generate a comparison.
8. Download summaries and comparison results as Markdown files.

## Retrieval Evaluation

The project includes `evaluate.py` to evaluate retrieval behavior using test questions.

An earlier local evaluation reported:

- Hit@5: 100% across three answerable test cases
- MRR@5: 1.0000
- Out-of-context tests passed: 1/1

These results are from a small test set and do not guarantee general retrieval accuracy or answer correctness.

## Current Limitations

- Retrieval and generation quality depend on PDF text extraction, chunking, embeddings, and the local model.
- Scanned PDFs may require OCR if they do not contain extractable text.
- Summaries and comparisons are limited by the amount of document context supplied to the model.
- Local inference performance depends on available system resources.
- Generated answers should be checked against the original documents for important decisions.

## Future Improvements

- OCR support for scanned PDFs
- More comprehensive retrieval and answer evaluation
- Improved document management across application sessions
- Page-level source navigation
- More efficient processing of long documents
- Automated tests and deployment improvements

## Author

**Tushal**

- GitHub: [Tushal238](https://github.com/Tushal238)
- Project Repository: [PDF RAG Chatbot](https://github.com/Tushal238/pdf-rag-chatbot)

---

Built as a hands-on project exploring Retrieval-Augmented Generation, vector search, local LLMs, and document intelligence.

