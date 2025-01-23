import getpass
import os
from dotenv import load_dotenv

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
tavily_api_key = os.getenv("TAVILY_API_KEY")
postgres_url = os.getenv("POSTGRES_URL")
jwt_secret = os.getenv("JWT_SECRET")
jwt_algorithm = os.getenv("JWT_ALGORITHM")

