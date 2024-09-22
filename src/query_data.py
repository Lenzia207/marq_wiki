# import argparse
from dataclasses import dataclass
from typing import List
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama
from src.embedds.get_embedds import get_embeddings
from src.constants.prompt_template import PROMPT_TEMPLATE_ADVANCED

CHROMA_PATH = "chroma"

@dataclass
class QueryResponse:
    query_text: str
    response_text: str
    sources: List[str]


def query_rag(query_text: str) -> QueryResponse:
    """ query_rag """
    # Prepare the DB.
    embedding_function = get_embeddings()
    if embedding_function is None:
            print("Failed to initialize embeddings.")
            return
        
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_score(query_text, k=3)

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE_ADVANCED)
    prompt = prompt_template.format(context=context_text, question=query_text)
    # print(prompt)

    model = Ollama(model="llama3.1:8b")
    response_text = model.invoke(prompt)

    sources = [doc.metadata.get("id", None) for doc, _score in results]
    print(f"Response: {response_text}\nSources: {sources}")
    
    return QueryResponse(
    query_text=query_text, response_text=response_text, sources=sources
    )
