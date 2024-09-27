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
    print(f"Database initialized at {Config.CHROMA_PATH}")
    print(f"db: {db}")
    return db

def add_to_chroma(chunks: list[Document]):
    """Add documents to the Chroma database."""
    # Load the existing database.   
    db = get_db_connection()    
    print("Database connection established.")
    # Calculate Page IDs.
    chunks_with_ids = calculate_chunk_ids(chunks)

    # Add or Update the documents.
    existing_items = db.get(include=[])  # IDs are always included by default
    existing_ids = set(existing_items["ids"])
    print(f"Number of existing documents in DB: {len(existing_ids)}")

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
            db.add_documents(new_chunks, ids=new_chunk_ids)
            print("✅ Documents added")
        except Exception as e:
            print(f"Error adding documents: {e}")
        # db.persist()
        print("✅ Documents database persisted.")
    else:
        print("✅ No new documents to add")

def clear_database():
    """ Clear DB """
    if os.path.exists(Config.CHROMA_PATH):
        shutil.rmtree(Config.CHROMA_PATH)
