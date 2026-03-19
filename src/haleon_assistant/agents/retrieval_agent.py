"""Retrieval agent – fetches relevant documents for a query."""


class RetrievalAgent:
    """Returns a list of document citations relevant to the query."""

    def retrieve(self, query: str) -> list:
        """Return a sample list of citation dicts.

        Args:
            query: The user's question.

        Returns:
            Non-empty list of citation dicts (stub data).
        """
        return [
            {
                "title": "Sample Doc",
                "url": "https://example.org/doc",
                "snippet": "Example snippet",
            }
        ]
