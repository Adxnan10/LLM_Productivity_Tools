"""
This module implements a retrieval grading pipeline that evaluates the relevance of retrieved documents to a user's query. The grader ensures that only relevant documents are processed further, filtering out erroneous retrievals based on semantic meaning and keyword matching.

At the moment I am only following this guideline: https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_adaptive_rag/#create-index
TODO: I will change it later to be more modular such that it can be more reusable.

"""

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from index_builder import retriever
from pydantic import BaseModel, Field


# Data model
class GradeDocuments(BaseModel):
    """Binary score for relevance check on retrieved documents."""

    binary_score: str = Field(
        description="Documents are relevant to the question, 'yes' or 'no'"
    )


# LLM with function call
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
structured_llm_grader = llm.with_structured_output(GradeDocuments)

# Prompt
system = """You are a grader assessing relevance of a retrieved document to a user question. \n 
    If the document contains keyword(s) or semantic meaning related to the user question, grade it as relevant. \n
    It does not need to be a stringent test. The goal is to filter out erroneous retrievals. \n
    Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question."""
grade_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "Retrieved document: \n\n {document} \n\n User question: {question}"),
    ]
)

retrieval_grader = grade_prompt | structured_llm_grader
question = "agent memory"
docs = retriever.invoke(question)
doc_txt = docs[1].page_content
print(retrieval_grader.invoke({"question": question, "document": doc_txt}))
