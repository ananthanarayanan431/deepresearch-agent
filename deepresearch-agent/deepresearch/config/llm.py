from dotenv import load_dotenv
from langchain_openai.chat_models import ChatOpenAI
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI

from deepresearch.config.env import OPENAI_API_KEY
from deepresearch.config.env import GOOGLE_API_KEY

load_dotenv()


class LlmService:
    @classmethod
    def get_model(cls, model_name: str = "gpt-4o-mini"):
        if not OPENAI_API_KEY:
            raise ValueError("Issue in OpenAI API Key!")

        try:
            llm = ChatOpenAI(model=model_name, temperature=0.5)
            return llm
        except Exception:
            return None
            
    @classmethod
    def get_openai_model(cls):
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI API Key is not Set!")
        try:
            llm = ChatOpenAI(model="gpt-4o-mini",temperature=0.5)
            return llm
        
        except Exception as Error:
            return None 
            
            
    @classmethod
    def get_gemini_model(cls):
        if not GOOGLE_API_KEY:
            raise ValueError('GOOGLE API KEY is not Set!')
        
        try:
            llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.5)
            return llm
        
        except Exception as Error:
            return None 