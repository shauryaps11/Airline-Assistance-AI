from pydantic import BaseModel
from typing import Optional


class ChatRequest(BaseModel):
    session_id: str
    message: str


class ChatResponse(BaseModel):
    reply: str
    intent: str
    confidence: float
    tools_used: list[str]
    escalated: bool
    escalation_summary: Optional[str] = None
    image_b64: Optional[str] = None
    audio_b64: Optional[str] = None
