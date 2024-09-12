from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain_community.document_loaders import PyPDFDirectoryLoader
import os

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the data folder
DATA_PATH = os.path.join(current_dir, '..', 'data')

def split_documents(documents: list[Document]):
    """Split documents into chunks."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=80,
        length_function=len,
        is_separator_regex=False,
    )
    return text_splitter.split_documents(documents)

def load_documents():
    """Load documents from the data directory."""
    loader = PyPDFDirectoryLoader(DATA_PATH)
    pages =  loader.load_and_split()
    return pages

documents = load_documents()

print(documents)

