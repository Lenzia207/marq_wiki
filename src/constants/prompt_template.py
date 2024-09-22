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