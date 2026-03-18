"""Rate-limit middleware – simple in-memory placeholder.

Uses a per-IP sliding-window counter backed by a plain Python dict.
In production replace with a Redis-backed solution.

TODO: configure limits via environment variables and wire into Redis.
"""

import time
from collections import defaultdict

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

# Simple config – adjust as needed
_MAX_REQUESTS = 100  # per window
_WINDOW_SECONDS = 60


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Placeholder in-memory rate limiter."""

    def __init__(self, app, max_requests: int = _MAX_REQUESTS, window: int = _WINDOW_SECONDS):
        super().__init__(app)
        self._max = max_requests
        self._window = window
        self._counts: dict = defaultdict(list)

    async def dispatch(self, request: Request, call_next):  # type: ignore[override]
        ip = request.client.host if request.client else "unknown"
        now = time.time()
        window_start = now - self._window
        self._counts[ip] = [t for t in self._counts[ip] if t > window_start]
        if len(self._counts[ip]) >= self._max:
            return JSONResponse({"detail": "Rate limit exceeded"}, status_code=429)
        self._counts[ip].append(now)
        return await call_next(request)
