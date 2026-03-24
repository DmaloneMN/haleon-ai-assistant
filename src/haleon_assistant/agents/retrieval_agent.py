from haleon_assistant.tools.search_tool import SearchTool


class RetrievalAgent:
    """Retrieval agent that delegates to the SearchTool and normalizes results."""

    def __init__(self) -> None:
        self._search = SearchTool()

    def retrieve(self, query: str) -> list:
        """Return a list of normalized document dicts with keys: title, url, snippet."""
        raw_results = self._search.search(query)
        docs = []
        for r in raw_results:
            docs.append(
                {
                    "title": r.get("title") or r.get("id") or "",
                    "url": r.get("source") or r.get("url") or "",
                    "snippet": r.get("text") or r.get("snippet") or "",
                }
            )
        return docs
