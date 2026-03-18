"""Embedder – returns vector representations for text chunks.

TODO: replace random vectors with real Azure OpenAI embedding calls.
"""

import random
from typing import List


def embed(text: str, dimensions: int = 1536) -> List[float]:
    """Return a random unit-length vector for *text*.

    This stub returns a deterministic random vector seeded by the text hash
    so that the same text always produces the same (fake) embedding.

    Args:
        text:       The text to embed.
        dimensions: Number of dimensions in the output vector.

    Returns:
        List of floats representing the embedding.
    """
    # TODO: call Azure OpenAI Embeddings API with the real deployment name
    rng = random.Random(hash(text))
    raw = [rng.gauss(0, 1) for _ in range(dimensions)]
    magnitude = sum(x**2 for x in raw) ** 0.5 or 1.0
    return [x / magnitude for x in raw]
