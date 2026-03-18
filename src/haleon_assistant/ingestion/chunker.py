"""Chunker – splits documents into fixed-size text chunks with overlap."""

from typing import List


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """Split *text* into overlapping chunks of at most *chunk_size* characters.

    Args:
        text:       Input text to split.
        chunk_size: Maximum characters per chunk.
        overlap:    Number of characters repeated at the start of each
                    successive chunk to preserve context.

    Returns:
        List of text chunks (may be empty if *text* is empty).
    """
    if not text:
        return []
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks
