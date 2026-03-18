"""Search tool – wraps Azure AI Search client.

TODO: replace stub with real azure-search-documents SDK calls.
"""


class SearchTool:
    """Placeholder wrapper around Azure AI Search."""

    def search(self, query: str, top: int = 5) -> list:
        """Return example search result documents.

        Args:
            query: The search query string.
            top:   Maximum number of results to return.

        Returns:
            List of document dicts (stub data).
        """
        # TODO: initialise SearchClient with AZURE_SEARCH_ENDPOINT + key/identity
        return [
            {
                "id": f"doc-{i:03d}",
                "content": f"Sample document {i} matching '{query}'.",
                "score": round(1.0 - i * 0.1, 2),
            }
            for i in range(min(top, 3))
        ]
