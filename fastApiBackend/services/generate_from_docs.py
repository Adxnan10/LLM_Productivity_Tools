"""
This module implements generation pipeline based on context (relevant docs) .

At the moment I am only following this guideline: https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_adaptive_rag/#create-index
TODO: I will change it later to be more modular such that it can be more reusable.

"""

from langchain_openai import ChatOpenAI
from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from retrieval_grader import docs, question

# Prompt
prompt = hub.pull("rlm/rag-prompt")

# LLM
llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)


# Post-processing
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


# Chain
rag_chain = prompt | llm | StrOutputParser()

# Run
generation = rag_chain.invoke({"context": docs, "question": question})
print(generation)