from langchain.embeddings import BedrockEmbeddings

def get_embeddings():
    """Get embeddings for chunks."""
    embedding = BedrockEmbeddings(
        credentials_profile_name="default", region_name="eu-west-1"
        
    )
    return embedding