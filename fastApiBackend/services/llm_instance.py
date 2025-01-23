from langchain_openai import ChatOpenAI
from config.env_setup import openai_api_key

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=openai_api_key, streaming=True)
