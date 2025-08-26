
from pydantic import BaseModel, Field
from typing import Optional


class ChatRequest(BaseModel):
    thread_id: Optional[str] = None
    message: str

class ChatResponse(BaseModel):
    thread_id: str
    is_followup: bool = False  # indicates if model is asking for clarification
    report: Optional[str] = None