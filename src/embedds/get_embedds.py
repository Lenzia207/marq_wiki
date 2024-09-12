from langchain_community.embeddings import OllamaEmbeddings

def get_embeddings():
    """Get embeddings for chunks."""
    try:
        # Initialize OllamaEmbeddings
        embedding = OllamaEmbeddings(model="llama3.1:8b")
        return embedding
    except Exception as e:
        print(f"Error initializing OllamaEmbeddings: {e}")
        return None