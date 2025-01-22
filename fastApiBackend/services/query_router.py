"""
query_router module sets up a query router using LangChain and OpenAI GPT models to determine the appropriate datasource
for user questions. It routes queries to either a vectorstore (for specific topics) or web search.
"""
from typing import Literal
from langchain_core.prompts import ChatPromptTemplate
from llm_instance import llm
from pydantic import BaseModel, Field


# Data model
class RouteQuery(BaseModel):  # TODO will be moved to pydantic_models
    """Route a user query to the most relevant datasource."""

    datasource: Literal["vectorstore", "web_search"] = Field(
        ...,
        description="Given a user question choose to route it to web search or a vectorstore.",
    )


structured_llm_router = llm.with_structured_output(RouteQuery)

# Prompt
system = """You are an expert at routing a user question to a vectorstore or web search.
The vectorstore contains documents related to agents, prompt engineering, and adversarial attacks.
Use the vectorstore for questions on these topics. Otherwise, use web-search."""
route_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "{question}"),
    ]
)

question_router = route_prompt | structured_llm_router
