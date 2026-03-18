"""Haleon AI Assistant - FastAPI application entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from .agents.orchestrator import AgentOrchestrator
from .config import get_settings
from .models.schemas import HealthResponse
from .routers.chat import router as chat_router
from .routers.feedback import router as feedback_router


@asynccontextmanager
async def lifespan(application: FastAPI):
    """Initialise shared resources on startup."""
    settings = get_settings()
    application.state.orchestrator = AgentOrchestrator(settings)
    yield


app = FastAPI(
    title="Haleon AI Assistant",
    description="AI-powered assistant built with AutoGen and Azure services.",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(chat_router)
app.include_router(feedback_router)


@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint."""
    return HealthResponse(status="ok", version="0.1.0")


def main() -> None:
    """Run the application using uvicorn."""
    import uvicorn

    settings = get_settings()
    uvicorn.run(
        "haleon_assistant.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
    )


if __name__ == "__main__":
    main()
