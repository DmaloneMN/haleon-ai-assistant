"""Cache tool – Redis wrapper with in-memory fallback.

When REDIS_URL is not set (local dev / CI) an in-memory dict is used instead.

TODO: configure TTL, key prefixes, and serialisation for production use.
"""

import os
from typing import Any, Optional

_store: dict = {}


class CacheTool:
    """Get/set cache backed by Redis or an in-memory dict."""

    def __init__(self) -> None:
        self._redis_url = os.getenv("REDIS_URL", "")
        self._client: Any = None
        if self._redis_url:
            try:
                import redis  # type: ignore[import-untyped]

                self._client = redis.from_url(self._redis_url)
            except Exception:
                # Fall back to in-memory if Redis is unavailable
                self._client = None

    def get(self, key: str) -> Optional[str]:
        """Return cached value for *key* or ``None`` if not found."""
        if self._client:
            return self._client.get(key)
        return _store.get(key)

    def set(self, key: str, value: str, ttl: int = 300) -> None:
        """Store *value* under *key* with optional TTL (seconds)."""
        if self._client:
            self._client.setex(key, ttl, value)
        else:
            _store[key] = value
