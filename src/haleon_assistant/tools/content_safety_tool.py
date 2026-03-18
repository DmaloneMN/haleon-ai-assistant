"""Content-safety tool – wraps Azure AI Content Safety.

TODO: replace stub with real azure-ai-contentsafety SDK calls.
"""


class ContentSafetyTool:
    """Placeholder wrapper around Azure AI Content Safety."""

    def analyze(self, text: str) -> dict:
        """Simulate a content-safety analysis.

        Returns:
            dict with ``safe`` (bool) and ``categories`` (dict of category → score).
        """
        # TODO: initialise ContentSafetyClient with endpoint and credentials
        return {
            "safe": True,
            "categories": {
                "hate": 0,
                "self_harm": 0,
                "sexual": 0,
                "violence": 0,
            },
        }
