"""
query_router module sets up a query router using LangChain and OpenAI GPT models to determine the appropriate datasource
for user questions. It routes queries to either a vectorstore (for specific topics) or web search.

Key Components:
1. `RouteQuery`: A Pydantic model defining the routing decision structure.
2. `ChatOpenAI`: GPT-4 model with structured output for routing queries.
3. `ChatPromptTemplate`: Defines the system's instructions and human input for the routing logic.
4. `question_router`: A router object that combines the prompt and structured output logic.

At the moment I am only following this guideline: https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_adaptive_rag/#create-index
TODO: I will change it later to be more modular such that it can be more reusable.

"""
from typing import Literal

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from pydantic import BaseModel, Field
from config.env_setup import openai_api_key


# Data model
class RouteQuery(BaseModel): # TODO will be moved to pydantic_models
    """Route a user query to the most relevant datasource."""

    datasource: Literal["vectorstore", "web_search"] = Field(
        ...,
        description="Given a user question choose to route it to web search or a vectorstore.",
    )


# LLM with function call
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=openai_api_key)
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
print(
    question_router.invoke(
        {"question": "Who will the Bears draft first in the NFL draft?"}
    )
)
print(question_router.invoke({"question": "What are the types of agent memory?"}))