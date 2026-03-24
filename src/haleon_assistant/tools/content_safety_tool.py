"""Content-safety tool – wraps Azure AI Content Safety.

TODO: replace stub with real azure-ai-contentsafety SDK calls.
"""


def check_content(text: str) -> dict:
    """Basic scaffold safety check: flags empty or whitespace-only text as unsafe.

    Args:
        text: The text to check.

    Returns:
        dict with ``safe`` (bool) and ``issues`` (list of str flag names).
    """
    if not text or not text.strip():
        return {"safe": False, "issues": ["empty_text"]}
    # Always safe in scaffold for non-empty text
    return {"safe": True, "issues": []}


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
