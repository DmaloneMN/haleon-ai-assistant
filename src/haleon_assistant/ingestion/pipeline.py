"""Ingestion pipeline – orchestrates chunker → embedder → indexer."""

import logging
from typing import List

from haleon_assistant.ingestion.chunker import chunk_text
from haleon_assistant.ingestion.embedder import embed
from haleon_assistant.ingestion.indexer import Indexer

logger = logging.getLogger(__name__)


def run_pipeline(
    documents: List[dict],
    index_name: str = "haleon-docs",
    chunk_size: int = 500,
    overlap: int = 50,
) -> None:
    """Ingest *documents* by chunking, embedding, then indexing each one.

    Args:
        documents:  List of dicts with at least ``id`` and ``content`` keys.
        index_name: Target Azure AI Search index name.
        chunk_size: Characters per chunk.
        overlap:    Overlap characters between consecutive chunks.
    """
    indexer = Indexer(index_name=index_name)
    records: List[dict] = []
    for doc in documents:
        doc_id = doc["id"]
        chunks = chunk_text(doc.get("content", ""), chunk_size=chunk_size, overlap=overlap)
        logger.info("Document %s → %d chunk(s)", doc_id, len(chunks))
        for idx, chunk in enumerate(chunks):
            records.append(
                {
                    "id": f"{doc_id}-chunk-{idx}",
                    "content": chunk,
                    "embedding": embed(chunk),
                }
            )
    indexer.upsert(records)
    logger.info("Pipeline complete: %d record(s) indexed to '%s'.", len(records), index_name)
