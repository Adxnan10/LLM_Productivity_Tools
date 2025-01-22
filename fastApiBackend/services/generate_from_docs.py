"""
This module implements generation pipeline based on context (relevant docs)
"""
from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from llm_instance import llm

# Prompt
prompt = hub.pull("rlm/rag-prompt")


# Post-processing
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


# Chain
rag_chain = prompt | llm | StrOutputParser()
