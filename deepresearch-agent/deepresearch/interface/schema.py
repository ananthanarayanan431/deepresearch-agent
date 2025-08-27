from typing import Optional

from pydantic import BaseModel


class ChatRequest(BaseModel):
    thread_id: Optional[str] = None
    message: str


class ChatResponse(BaseModel):
    thread_id: str
    response: str
    is_followup: bool = False  # indicates if model is asking for clarification
    report: Optional[str] = None
