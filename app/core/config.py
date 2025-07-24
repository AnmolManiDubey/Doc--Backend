import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_BASE_URL = "https://api.groq.com/openai/v1"
LLM_MODEL = "llama3-70b-8192"   # this is the usual model name; adjust if yours differs
