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


LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")


PPLX_API_KEY = os.getenv("PPLX_API_KEY")
PPLX_API_URL = os.getenv("PPLX_API_URL", "https://api.perplexity.ai")
PPLX_MODEL = os.getenv("PPLX_MODEL", "sonar")
PPLX_INSIGHTS_MODEL = os.getenv("PPLX_INSIGHTS_MODEL", "sonar-pro")
