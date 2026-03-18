"""Feedback router for Haleon AI Assistant."""

import logging

from fastapi import APIRouter

from ..models.schemas import FeedbackRequest, FeedbackResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/feedback", tags=["feedback"])


@router.post("/", response_model=FeedbackResponse)
async def submit_feedback(body: FeedbackRequest) -> FeedbackResponse:
    """Accept and log user feedback for a chat message."""
    logger.info(
        "Feedback received session_id=%s message_id=%s rating=%d comment=%r",
        body.session_id,
        body.message_id,
        body.rating,
        body.comment,
    )
    return FeedbackResponse(status="accepted", message_id=body.message_id)
