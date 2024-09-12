import os
import shutil
from langchain.docstore.document import Document
from langchain.vectorstores.chroma import Chroma
from src.db.chunks import calculate_chunk_ids
from src.embedds.get_embedds import get_embeddings

CHROMA_PATH = "chroma"

def add_to_chroma(chunks: list[Document]):
    """Add documents to the Chroma database."""
    # Load the existing database.
    db = Chroma(
        persist_directory=CHROMA_PATH, embedding_function= get_embeddings()
    )

    # Calculate Page IDs.
    chunks_with_ids = calculate_chunk_ids(chunks)

    # Add or Update the documents.
    existing_items = db.get(include=[])  # IDs are always included by default
    existing_ids = set(existing_items["ids"])
    print(f"Number of existing documents in DB: {len(existing_ids)}")

    # Only add documents that don't exist in the DB.
    new_chunks = []
    for chunk in chunks_with_ids:
        if chunk.metadata["id"] not in existing_ids:
            new_chunks.append(chunk)

    if len(new_chunks):
        print(f"👉 Adding new documents: {len(new_chunks)}")
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        db.add_documents(new_chunks, ids=new_chunk_ids)
        db.persist()
    else:
        print("✅ No new documents to add")
        
        

def clear_database():
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)