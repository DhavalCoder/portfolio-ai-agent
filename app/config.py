import os
from dotenv import load_dotenv

# Loads the variables from the .env file into the system environment
load_dotenv()

# We export them here so the rest of the app can easily import them
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
# Llama 3.1 8B Instant has 128,000 context window and the highest free-tier rate limits!
LLM_MODEL = os.getenv("LLM_MODEL", "groq/compound-mini")
