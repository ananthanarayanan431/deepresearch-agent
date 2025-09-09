import os

from dotenv import load_dotenv

load_dotenv()
# llm
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')


# tools
EXA_API_KEY = os.getenv("EXA_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# tracing
OPIK_API_KEY = os.getenv("OPIK_API_KEY")
