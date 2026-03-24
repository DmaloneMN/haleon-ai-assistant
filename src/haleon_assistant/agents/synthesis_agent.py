from typing import List


class SynthesisAgent:
    """Compose a short answer from retrieved document snippets."""

    def synthesize(self, query: str, docs: List[dict]) -> str:
        snippets = [d.get("snippet", "") for d in docs if isinstance(d, dict)]
        joined = " ".join(s for s in snippets if s)
        base = f"Placeholder answer for: {query}" if query else "Placeholder answer"
        if joined:
            return f"{base}. Sources: {joined}"
        return base
