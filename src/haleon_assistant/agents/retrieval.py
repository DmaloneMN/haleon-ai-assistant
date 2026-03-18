"""Retrieval agent: fetches relevant documents from Azure AI Search."""

import logging

from ..services.search import SearchService

logger = logging.getLogger(__name__)


class RetrievalAgent:
    """Retrieves documents relevant to a query."""

    def __init__(self, search_service: SearchService) -> None:
        self._search = search_service

    async def run(self, query: str, intent: str) -> dict:
        """Search for *query* and return documents with assembled context."""
        documents = await self._search.search(query)

        context_parts: list[str] = []
        for i, doc in enumerate(documents, 1):
            title = doc.get("title") or doc.get("source") or f"Document {i}"
            content = doc.get("content", "")
            context_parts.append(f"[{i}] {title}\n{content}")

        context = "\n\n".join(context_parts)

        logger.info(
            "Retrieval query=%r intent=%s documents_found=%d",
            query,
            intent,
            len(documents),
        )

        return {
            "query": query,
            "intent": intent,
            "documents": documents,
            "context": context,
        }
