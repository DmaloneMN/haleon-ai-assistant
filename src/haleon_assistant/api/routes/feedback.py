"""Feedback route – POST /api/v1/feedback."""

from fastapi import APIRouter
from pydantic import BaseModel
from starlette.responses import Response

router = APIRouter(tags=["feedback"])


class FeedbackRequest(BaseModel):
    query: str
    answer: str
    rating: int  # 1-5
    comment: str = ""


@router.post("/feedback", status_code=202)
async def feedback(request: FeedbackRequest) -> Response:
    """Accept user feedback and return 202 Accepted (stub)."""
    # TODO: persist feedback to Azure Table Storage or Event Hub
    return Response(status_code=202)
