"""Chat router for Haleon AI Assistant."""

import logging

from fastapi import APIRouter, Request

from ..models.schemas import ChatRequest, ChatResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/", response_model=ChatResponse)
async def chat(request: Request, body: ChatRequest) -> ChatResponse:
    """Process a chat message through the multi-agent pipeline."""
    orchestrator = request.app.state.orchestrator
    return await orchestrator.process(body)
