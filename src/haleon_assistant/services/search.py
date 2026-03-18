"""Azure AI Search service with graceful degradation."""

import logging

logger = logging.getLogger(__name__)

try:
    from azure.core.credentials import AzureKeyCredential
    from azure.search.documents import SearchClient

    _SDK_AVAILABLE = True
except ImportError:
    _SDK_AVAILABLE = False
    logger.warning("azure-search-documents not installed; search disabled")


class SearchService:
    """Wraps Azure AI Search for document retrieval."""

    def __init__(self, endpoint: str, api_key: str, index_name: str) -> None:
        self._endpoint = endpoint or ""
        self._api_key = api_key or ""
        self._index_name = index_name or ""
        self._client = None

        if _SDK_AVAILABLE and self._endpoint and self._api_key and self._index_name:
            try:
                self._client = SearchClient(
                    endpoint=self._endpoint,
                    index_name=self._index_name,
                    credential=AzureKeyCredential(self._api_key),
                )
            except Exception as exc:
                logger.warning("Could not create SearchClient: %s", exc)

    async def search(self, query: str, top: int = 5) -> list[dict]:
        """Search the index and return up to *top* results.

        Returns ``[]`` when credentials are absent or the call fails.
        """
        if self._client is None:
            return []

        try:
            results = self._client.search(
                search_text=query,
                top=top,
                include_total_count=False,
            )
            docs: list[dict] = []
            for r in results:
                docs.append(
                    {
                        "id": r.get("id", ""),
                        "content": r.get("content", ""),
                        "title": r.get("title", ""),
                        "source": r.get("source", ""),
                        "url": r.get("url", ""),
                        "score": r.get("@search.score", 0.0),
                    }
                )
            return docs
        except Exception as exc:
            logger.warning("Search failed: %s", exc)
            return []
