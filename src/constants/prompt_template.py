PROMPT_TEMPLATE_ADVANCED = """
Based on the following context, extract the most relevant information to answer the question. Additionally, provide any other related insights or background information that may help elaborate on the topic:

{context}

---

Provide a detailed answer, including relevant points from the above context and additional relevant insights: {question}
"""


PROMPT_TEMPLATE_SIMPLE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

PROMPT_TEMPLATE = """
You are a highly knowledgeable assistant with access to a collection of documents. Answer the user's question using the most relevant information from the following context: 

{context}

But also incorporate your own general knowledge where applicable. 
If the documents do not contain all the needed information, provide additional context or insights from your own knowledge.

Question: {question}

Provide a detailed and comprehensive response based on both the documents and your own expertise.
"""