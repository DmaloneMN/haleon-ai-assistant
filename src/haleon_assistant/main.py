"""Haleon AI Assistant - FastAPI application entry point."""

from fastapi import FastAPI

app = FastAPI(
    title="Haleon AI Assistant",
    description="AI-powered assistant built with AutoGen and Azure services.",
    version="0.1.0",
)


@app.get("/health")
async def health_check() -> dict:
    """Health check endpoint."""
    return {"status": "ok"}


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
