
import logging

from dotenv import load_dotenv
from langchain_openai.chat_models import ChatOpenAI
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI

from deepresearch.config.env import OPENAI_API_KEY
from deepresearch.config.env import GOOGLE_API_KEY
from deepresearch.config.env import LLM_PROVIDER

load_dotenv()

logger = logging.getLogger(__name__)

class LlmService:
    @classmethod
    def get_model(cls):
        if LLM_PROVIDER=="openai":
            if not OPENAI_API_KEY:
                raise ValueError("Issue in OpenAI API Key!")

            try:
                model_name = "gpt-4o-mini"
                llm = ChatOpenAI(model=model_name, temperature=0.5)
                logger.info("Using OpenAI model")
                print("Using OpenAI model")
                return llm
            except Exception:
                return None
        elif LLM_PROVIDER=="google":
            if not GOOGLE_API_KEY:
                raise ValueError("Issue in Google API Key!")

            try:
                model_name = "gemini-2.5-flash"
                llm = ChatGoogleGenerativeAI(model=model_name, temperature=0.5)
                logger.info("Using Google model")
                return llm
            except Exception:
                return None
        else:
            raise ValueError("Invalid LLM Provider!")
   