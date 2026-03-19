"""Synthesis agent – composes the final answer with citations."""


class SynthesisAgent:
    """Assembles a human-readable answer from retrieved documents."""

    def synthesize(self, query: str, docs: list) -> str:
        """Return a placeholder answer string concatenating doc snippets.

        Args:
            query: The user's original question.
            docs:  List of citation dicts from the retrieval agent.

        Returns:
            Placeholder answer string.
        """
        snippets = " ".join(d.get("snippet", "") for d in docs)
        return f"Answer (placeholder): based on sources. {snippets}"
