"""Auth middleware – placeholder JWT validation.

Reads JWKS_URL from environment.  If JWKS_URL is set, the middleware
requires an Authorization: Bearer <token> header and returns HTTP 401 when
it is absent.  When JWKS_URL is not set (local dev / CI) all requests are
passed through unchanged.

TODO: add real JWT signature + claims validation once JWKS_URL is configured.
"""

import os

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse


class AuthMiddleware(BaseHTTPMiddleware):
    """Placeholder JWT bearer-token middleware."""

    async def dispatch(self, request: Request, call_next):  # type: ignore[override]
        jwks_url = os.getenv("JWKS_URL", "")
        if jwks_url:
            auth_header = request.headers.get("Authorization", "")
            if not auth_header.startswith("Bearer "):
                return JSONResponse(
                    {"detail": "Missing or invalid Authorization header"},
                    status_code=401,
                )
            # TODO: validate JWT signature against JWKS_URL
        return await call_next(request)
