import os
import glob
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain_community.document_loaders import PyPDFDirectoryLoader
from src.config.config import Config

def split_documents(documents: list[Document]):
    """Split documents into chunks."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=80,
        length_function=len,
        is_separator_regex=False,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split documents into {len(chunks)} chunks.")
    return chunks

def load_documents():
    """Load documents from the data directory."""
    loader = PyPDFDirectoryLoader(Config.DATA_PATH)
    pages =  loader.load_and_split()
    print(f"Loaded {len(pages)} pages from documents.")
    return pages
