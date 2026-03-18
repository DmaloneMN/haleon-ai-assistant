"""Synthesis agent – composes the final answer with citations.

TODO: replace stub with a real LLM-based answer composition call.
"""


class SynthesisAgent:
    """Assembles a human-readable answer from retrieved documents."""

    def compose(self, query: str, documents: list) -> dict:
        """Return an answer dict with keys ``answer`` and ``citations``.

        Args:
            query:     The user's original question.
            documents: List of citation dicts from the retrieval agent.

        Returns:
            dict with ``answer`` (str) and ``citations`` (list).
        """
        # TODO: call Azure OpenAI with system prompt + documents + query
        answer = (
            f"This is a placeholder answer for '{query}'. "
            "Implementers should replace this with a real LLM-generated response."
        )
        return {"answer": answer, "citations": documents}
