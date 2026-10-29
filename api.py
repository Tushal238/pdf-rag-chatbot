
from fastapi import UploadFile, File, HTTPException
from ingest import index_pdf_bytes
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ingest import get_collection, delete_pdf
from fastapi import HTTPException
from retriever import retrieve_chunks
from generator import generate_answer

app = FastAPI(title="DocuMind AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    question: str


@app.get("/")
def health_check():
    return {
        "status": "ok",
        "message": "DocuMind AI API is running"
    }


@app.post("/api/chat")
def chat(request: ChatRequest):
    question = request.question.strip()

    if not question:
        return {"answer": "Please enter a question.", "sources": []}

    chunks = retrieve_chunks(question)
    answer = generate_answer(question, chunks)

    sources = [
        {
            "source": chunk.get("source", "Unknown"),
            "page": chunk.get("page", "Unknown"),
            "text": chunk.get("text", "")
        }
        for chunk in chunks
    ]

    return {"answer": answer, "sources": sources}

@app.post("/api/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Please upload a PDF file."
        )

    pdf_bytes = await file.read()

    if not pdf_bytes:
        raise HTTPException(
            status_code=400,
            detail="The uploaded PDF is empty."
        )

    try:
        result = index_pdf_bytes(pdf_bytes, file.filename)
        return {
            "message": f"{file.filename} uploaded and indexed successfully.",
            "filename": file.filename,
            "result": result
        }
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"PDF indexing failed: {str(exc)}"
        )

@app.get("/api/documents")
def list_documents():
    collection = get_collection()
    result = collection.get(include=["metadatas"])

    documents = {}

    for metadata in result.get("metadatas", []) or []:
        filename = metadata.get("source")
        if filename:
            documents[filename] = {
                "filename": filename
            }

    return {"documents": list(documents.values())}


@app.delete("/api/documents/{filename}")
def remove_document(filename: str):
    try:
        result = delete_pdf(filename)
        return {
            "message": f"{filename} removed successfully.",
            "result": result
        }
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Could not delete document: {exc}"
        )
