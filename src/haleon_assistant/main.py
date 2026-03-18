"""Haleon AI Assistant – FastAPI application entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from haleon_assistant.api.routes import chat, feedback, health


@asynccontextmanager
async def lifespan(application: FastAPI):  # noqa: ARG001
    """Initialise resources on startup; clean up on shutdown."""
    # TODO: initialise Azure clients, warm cache, etc.
    yield
    # TODO: flush buffers, close connections, etc.


app = FastAPI(
    title="Haleon AI Assistant",
    description="AI-powered assistant – stubs for further development.",
    version="0.0.0",
    lifespan=lifespan,
)

# ---------------------------------------------------------------------------
# CORS
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: restrict in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------
app.include_router(health.router, prefix="/api/v1")
app.include_router(chat.router, prefix="/api/v1")
app.include_router(feedback.router, prefix="/api/v1")


def main() -> None:
    """Run the application using uvicorn."""
    import os

    import uvicorn

    uvicorn.run(
        "haleon_assistant.main:app",
        host=os.getenv("HOST", "127.0.0.1"),
        port=int(os.getenv("PORT", "8000")),
        reload=os.getenv("RELOAD", "false").lower() == "true",
    )


if __name__ == "__main__":
    main()



