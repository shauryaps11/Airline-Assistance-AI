from fastapi import APIRouter, HTTPException
from backend.models import ChatRequest, ChatResponse
from backend.agent import engine
from backend import database as db

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def chat(req: ChatRequest):
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    return engine.process(req.session_id, req.message.strip())


@router.get("/session/{session_id}")
async def get_session(session_id: str):
    messages = db.get_session_messages(session_id)
    return {"session_id": session_id, "messages": messages}
