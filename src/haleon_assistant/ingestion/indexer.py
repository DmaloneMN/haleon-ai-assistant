"""Indexer – creates or updates Azure AI Search indexes.

TODO: implement using azure-search-documents SDK.
"""

from typing import List


class Indexer:
    """Stub indexer that demonstrates the expected interface.

    Usage::

        indexer = Indexer(index_name="haleon-docs")
        indexer.upsert(documents)
    """

    def __init__(self, index_name: str = "haleon-docs") -> None:
        self.index_name = index_name
        # TODO: initialise SearchIndexClient and SearchClient with Azure creds

    def upsert(self, documents: List[dict]) -> None:
        """Merge-or-upload *documents* into the search index.

        Each document dict should contain at least ``id``, ``content``, and
        ``embedding`` keys.

        TODO: call SearchClient.merge_or_upload_documents(documents)
        """
        # Stub: no-op until real Azure SDK integration is added
