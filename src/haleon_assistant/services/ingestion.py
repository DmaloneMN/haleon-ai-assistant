"""Document ingestion pipeline for Haleon AI Assistant."""

import logging
from typing import Any

logger = logging.getLogger(__name__)

try:
    from azure.storage.blob import BlobServiceClient

    _BLOB_SDK_AVAILABLE = True
except ImportError:
    _BLOB_SDK_AVAILABLE = False
    logger.warning("azure-storage-blob not installed; ingestion disabled")

try:
    from azure.core.credentials import AzureKeyCredential
    from azure.search.documents import SearchClient
    from azure.search.documents.models import IndexDocumentsBatch

    _SEARCH_SDK_AVAILABLE = True
except ImportError:
    _SEARCH_SDK_AVAILABLE = False


class IngestionService:
    """Downloads blobs, chunks text, and indexes into Azure AI Search."""

    def __init__(
        self,
        storage_account_url: str,
        container: str,
        search_endpoint: str,
        search_key: str,
        index_name: str,
    ) -> None:
        self._storage_url = storage_account_url or ""
        self._container = container or ""
        self._search_endpoint = search_endpoint or ""
        self._search_key = search_key or ""
        self._index_name = index_name or ""

        self._blob_client = None
        self._search_client = None

        if _BLOB_SDK_AVAILABLE and self._storage_url:
            try:
                self._blob_client = BlobServiceClient(account_url=self._storage_url)
            except Exception as exc:
                logger.warning("Could not create BlobServiceClient: %s", exc)

        if _SEARCH_SDK_AVAILABLE and self._search_endpoint and self._search_key:
            try:
                self._search_client = SearchClient(
                    endpoint=self._search_endpoint,
                    index_name=self._index_name,
                    credential=AzureKeyCredential(self._search_key),
                )
            except Exception as exc:
                logger.warning("Could not create SearchClient for ingestion: %s", exc)

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    async def ingest_blob(self, blob_name: str) -> dict:
        """Download *blob_name*, chunk it, and index chunks.

        Returns ``{"blob": blob_name, "chunks_indexed": 0}`` on failure.
        """
        if self._blob_client is None:
            logger.warning("No blob client available; skipping ingestion")
            return {"blob": blob_name, "chunks_indexed": 0}

        try:
            container_client = self._blob_client.get_container_client(self._container)
            blob_data = container_client.download_blob(blob_name).readall()
            text = blob_data.decode("utf-8", errors="replace")
        except Exception as exc:
            logger.error("Failed to download blob %s: %s", blob_name, exc)
            return {"blob": blob_name, "chunks_indexed": 0}

        chunks = self.chunk_text(text)
        if not chunks or self._search_client is None:
            return {"blob": blob_name, "chunks_indexed": 0}

        documents: list[dict[str, Any]] = [
            {
                "id": f"{blob_name}-{i}",
                "content": chunk,
                "title": blob_name,
                "source": blob_name,
                "url": "",
            }
            for i, chunk in enumerate(chunks)
        ]

        try:
            self._search_client.upload_documents(documents=documents)
            logger.info("Indexed %d chunks from %s", len(documents), blob_name)
        except Exception as exc:
            logger.error("Failed to index chunks from %s: %s", blob_name, exc)
            return {"blob": blob_name, "chunks_indexed": 0}

        return {"blob": blob_name, "chunks_indexed": len(documents)}

    async def list_blobs(self) -> list[str]:
        """Return a list of blob names in the configured container."""
        if self._blob_client is None:
            return []
        try:
            container_client = self._blob_client.get_container_client(self._container)
            return [b.name for b in container_client.list_blobs()]
        except Exception as exc:
            logger.warning("Failed to list blobs: %s", exc)
            return []

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> list[str]:
        """Split *text* into overlapping chunks of *chunk_size* characters.

        Very small trailing chunks (< overlap size) are merged into the
        previous chunk to avoid near-empty index documents.
        """
        if not text:
            return []
        chunks: list[str] = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunks.append(text[start:end])
            start += chunk_size - overlap

        # Merge a tiny trailing chunk into the previous one
        if len(chunks) > 1 and len(chunks[-1]) < overlap:
            chunks[-2] += chunks[-1]
            chunks.pop()

        return chunks
