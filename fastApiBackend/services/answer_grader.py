from pydantic import BaseModel, Field
from llm_instance import llm
from langchain_core.prompts import ChatPromptTemplate


class AnswerGrader(BaseModel):
    binary_score: str = Field(description="Answer addresses the question. 'yes' or 'no'")


structured_llm_grader = llm.with_structured_output(AnswerGrader)
# prompt
system = """You are a grader assessing whether an answer addresses / resolves a question \n 
     Give a binary score 'yes' or 'no'. Yes' means that the answer resolves the question."""

answer_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "User question: \n\n {question} \n\n LLM generation: {generation}"),
    ]
)

answer_grader = answer_prompt | structured_llm_grader
