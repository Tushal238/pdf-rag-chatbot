

\# Multi-PDF RAG Chatbot



A Retrieval-Augmented Generation (RAG) application that allows users

to upload multiple PDF documents and ask questions about their content

using a locally running Large Language Model.



\## Features



\- Upload multiple PDF documents.

\- Extract text from PDFs using PyMuPDF.

\- Split extracted text into overlapping chunks.

\- Generate embeddings using Sentence Transformers.

\- Store and retrieve document chunks using ChromaDB.

\- Generate context-grounded answers using Ollama and Llama 3.2.

\- Display source PDF names and page numbers.

\- View retrieval cosine distances.

\- Delete indexed documents.

\- Evaluate retrieval performance using test questions.

\- Interactive chat interface built with Streamlit.



\## Tech Stack



\- Python

\- Streamlit

\- PyMuPDF

\- Sentence Transformers

\- ChromaDB

\- Ollama

\- Llama 3.2



\## Project Structure



```text

pdf-rag-chatbot/

├── app.py

├── ingest.py

├── retriever.py

├── generator.py

├── evaluate.py

├── create\_data.py

├── requirements.txt

├── README.md

├── .gitignore

└── data/

&#x20;   └── rag\_guide.pdf

```



The `chroma\_db/` directory stores the local vector database.

It is excluded from Git using `.gitignore`.



\## How It Works



1\. Upload PDF documents through the Streamlit interface.

2\. Extract text from each PDF.

3\. Split the text into overlapping chunks.

4\. Convert chunks into vector embeddings.

5\. Store embeddings and metadata in ChromaDB.

6\. Retrieve relevant chunks for a user question.

7\. Pass the retrieved context to the local language model.

8\. Display the generated answer and retrieved source information.



\## Installation



\### 1. Clone the repository



```bash

git clone YOUR\_GITHUB\_REPOSITORY\_URL

cd pdf-rag-chatbot

```



Replace `YOUR\_GITHUB\_REPOSITORY\_URL` with your repository URL.



\### 2. Create and activate a virtual environment



Windows CMD:



```cmd

python -m venv venv

venv\\Scripts\\activate

```



\### 3. Install dependencies



```cmd

python -m pip install -r requirements.txt

```



\### 4. Install Ollama



Install Ollama from:



https://ollama.com/



Download the model:



```cmd

ollama pull llama3.2:3b

```



Make sure Ollama is running before asking questions.



\### 5. Start the application



```cmd

python -m streamlit run app.py --server.fileWatcherType none

```



Open the local URL displayed in the terminal, usually:



http://localhost:8501



\## Usage



1\. Upload one or more PDF files in the sidebar.

2\. Click \*\*Process PDFs\*\*.

3\. Enter a question in the chat input.

4\. Read the generated answer.

5\. Expand the retrieved sources section to inspect PDF names,

&#x20;  page numbers and cosine distances.



\## Evaluation



Run the basic retrieval evaluation script:



```cmd

python evaluate.py

```



The script checks whether expected PDF sources appear among

the retrieved chunks and prints generated answers.



\## Limitations



\- Scanned PDFs may require OCR before text can be extracted.

\- Answer quality depends on document quality and retrieval relevance.

\- The language model may occasionally produce unsupported information.

\- Cosine distance is a similarity signal, not a guarantee of correctness.

\- The application requires sufficient local resources to run the model.



\## Future Improvements



\- Better handling of duplicate filenames and document versions.

\- Improved retrieval filtering and ranking.

\- More comprehensive answer evaluation.

\- OCR support for scanned documents.

\- Exportable chat history.

\- Improved document inventory and management.



\## License



Choose and add an appropriate open-source license before distributing

the project.



