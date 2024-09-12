from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain.document_loaders import PyPDFDirectoryLoader
DATA_PATH = "../../data"

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

