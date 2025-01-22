from langchain_community.tools.tavily_search import TavilySearchResults
from config.env_setup import tavily_api_key

web_search_tool = TavilySearchResults(k=3, tavily_api_key=tavily_api_key)
