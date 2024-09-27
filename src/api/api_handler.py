from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
import uvicorn
import sys
import os
import shutil
src_path = os.path.join(os.path.dirname(__file__), '..', '..')
sys.path.append(src_path)
from src.query_data import query_rag, QueryResponse
from fastapi.middleware.cors import CORSMiddleware
from src.config.config import Config
from src.documents.handle_documents import split_documents, load_documents
from src.db.handle_db import add_to_chroma

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SubmitQueryRequest(BaseModel):
    query_text: str


@app.get("/")
def index():
    """Return a welcome message."""
    return {"Hello": "World"}

@app.post("/upload-document")
async def upload_document(file: UploadFile = File(...)):
    """Upload a document to the data folder."""
    data_folder = os.path.join(src_path, Config.DATA_PATH)
    file_path = os.path.join(data_folder, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    # Update the database
    documents = load_documents()
    chunks = split_documents(documents)
    add_to_chroma(chunks)
    
    return {"filename": file.filename,"message": "File uploaded and database update started"}


@app.post("/submit_input")
def submit_input_endpoint(request: SubmitQueryRequest) -> QueryResponse:
    """Submit a query to the RAG model."""
    response = query_rag(request.query_text)
    return response

if __name__ == "__main__":
    # Run this as a server directly.
    PORT = 8000
    print(f"Running the FastAPI server on port {PORT}.")
    uvicorn.run("api_handler:app", host="127.0.0.1", port=PORT)
