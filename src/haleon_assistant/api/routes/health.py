"""Health-check route."""

import time

from fastapi import APIRouter

router = APIRouter(tags=["health"])

_start = time.time()


@router.get("/health")
async def health() -> dict:
    """Return service health and uptime."""
    return {"status": "ok", "uptime_seconds": round(time.time() - _start, 2)}
