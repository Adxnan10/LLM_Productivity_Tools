### Question Re-writer
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from config.env_setup import openai_api_key



# LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=openai_api_key)

# Prompt
system = """You a question re-writer that converts an input question to a better version that is optimized \n 
     for vectorstore retrieval. Look at the input and try to reason about the underlying semantic intent / meaning."""
re_write_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        (
            "human",
            "Here is the initial question: \n\n {question} \n Formulate an improved question.",
        ),
    ]
)
question = "agent memory"
question_rewriter = re_write_prompt | llm | StrOutputParser()
print(question_rewriter.invoke({"question": question}))