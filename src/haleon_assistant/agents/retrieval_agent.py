class RetrievalAgent:
    """Placeholder retrieval agent that returns deterministic example documents."""

    def retrieve(self, query: str) -> list:
        # Return a reproducible sample "document" for testing
        return [
            {
                "title": "Sample Doc",
                "url": "https://example.org/doc",
                "snippet": "Example snippet relevant to query: " + (query or ""),
            }
        ]
