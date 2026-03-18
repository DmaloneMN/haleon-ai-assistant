"""Chat route – POST /api/v1/chat."""

from fastapi import APIRouter
from pydantic import BaseModel

from haleon_assistant.agents.orchestrator import Orchestrator

router = APIRouter(tags=["chat"])

_orchestrator = Orchestrator()


class ChatRequest(BaseModel):
    query: str


class ChatResponse(BaseModel):
    answer: str
    citations: list


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """Accept a user query and return an AI-generated answer (stub)."""
    result = _orchestrator.run(request.query)
    return ChatResponse(answer=result["answer"], citations=result["citations"])
