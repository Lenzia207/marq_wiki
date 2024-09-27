import os
import shutil
from langchain.docstore.document import Document
from langchain_chroma import Chroma
from src.db.chunks import calculate_chunk_ids
from src.embedds.get_embedds import get_embeddings
from src.config.config import Config


def get_db_connection():
    """Get a connection to the Chroma database."""
    if not os.path.exists(Config.CHROMA_PATH):
        os.makedirs(Config.CHROMA_PATH)
    db = Chroma(persist_directory=Config.CHROMA_PATH, embedding_function=get_embeddings())
    return db

def add_to_chroma(chunks: list[Document], batch_size=10):
    """Add documents to the Chroma database."""
    # Load the existing database.
    db = get_db_connection()    
    # Calculate Page IDs.
    chunks_with_ids = calculate_chunk_ids(chunks)

    # Add or Update the documents.
    existing_items = db.get(include=[])  # IDs are always included by default
    existing_ids = set(existing_items["ids"])

    # Only add documents that don't exist in the DB.
    new_chunks = []
    for chunk in chunks_with_ids:
        print(f"Adding chunk: {chunk.metadata['id']}")
        if chunk.metadata["id"] not in existing_ids:
            new_chunks.append(chunk)
        else:
            print(f"Chunk with ID {chunk.metadata['id']} already exists in DB.")
            
    # print(f"New chunks to add: {new_chunks}")
    if new_chunks:
        print(f"👉 Adding new documents: {len(new_chunks)}")
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        try:
            # Add documents in batches to avoid memory issues.
            # This is especially important when adding large documents.
            for i in range(0, len(new_chunks), batch_size):
                batch_chunks = new_chunks[i:i + batch_size]
                batch_ids = new_chunk_ids[i:i + batch_size]
                print(f"Adding batch {i // batch_size + 1}: {len(batch_chunks)} documents")
                db.add_documents(batch_chunks, ids=batch_ids)
                print(f"✅ Batch {i // batch_size + 1} added")
            print("✅ All documents added")
        except Exception as e:
            print(f"Error adding documents: {e}")
    else:
        print("✅ No new documents to add")

def clear_database():
    """ Clear DB """
    if os.path.exists(Config.CHROMA_PATH):
        shutil.rmtree(Config.CHROMA_PATH)
