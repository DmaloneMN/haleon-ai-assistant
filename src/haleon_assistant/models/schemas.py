"""Pydantic schemas for Haleon AI Assistant API."""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class Citation(BaseModel):
    source: str
    title: str
    url: Optional[str] = None
    excerpt: Optional[str] = None


class ChatRequest(BaseModel):
    session_id: Optional[str] = None
    message: str
    channel: str = "web"


class ChatResponse(BaseModel):
    session_id: str
    answer: str
    citations: list[Citation] = Field(default_factory=list)
    disclaimer: str
    escalate: bool = False


class FeedbackRequest(BaseModel):
    session_id: str
    message_id: str
    rating: int = Field(..., description="1 for positive, -1 for negative")
    comment: Optional[str] = None


class FeedbackResponse(BaseModel):
    status: str
    message_id: str


class HealthResponse(BaseModel):
    status: str
    version: str
