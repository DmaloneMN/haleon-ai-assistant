"""Retrieval agent – fetches relevant documents for a query.

TODO: replace stub with real Azure AI Search calls.
"""


class RetrievalAgent:
    """Returns a list of document citations relevant to the query."""

    def retrieve(self, query: str, route: str = "general") -> list:
        """Return a list of example citation dicts.

        Args:
            query: The user's question.
            route:  Routing label from the triage agent.

        Returns:
            Non-empty list of citation dicts (stub data).
        """
        # TODO: call Azure AI Search with the query and route-specific index
        return [
            {
                "id": "doc-001",
                "title": "Example Product Monograph",
                "excerpt": f"Stub result for query '{query}' (route={route}).",
                "url": "https://example.com/doc-001",
            }
        ]
