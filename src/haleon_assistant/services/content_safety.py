"""Azure Content Safety service with graceful degradation."""

import logging

logger = logging.getLogger(__name__)

try:
    from azure.ai.contentsafety import ContentSafetyClient
    from azure.ai.contentsafety.models import AnalyzeTextOptions
    from azure.core.credentials import AzureKeyCredential

    _SDK_AVAILABLE = True
except ImportError:
    _SDK_AVAILABLE = False
    logger.warning("azure-ai-contentsafety not installed; content safety checks disabled")


class ContentSafetyService:
    """Checks text against Azure Content Safety."""

    def __init__(self, endpoint: str, api_key: str) -> None:
        self._endpoint = endpoint or ""
        self._api_key = api_key or ""
        self._client = None

        if _SDK_AVAILABLE and self._endpoint and self._api_key:
            try:
                self._client = ContentSafetyClient(
                    endpoint=self._endpoint,
                    credential=AzureKeyCredential(self._api_key),
                )
            except Exception as exc:
                logger.warning("Could not create ContentSafetyClient: %s", exc)

    async def check(self, text: str) -> dict:
        """Return safety analysis for *text*.

        Falls back to ``{"safe": True, "categories": [], "severity": 0}`` when
        credentials are absent or the SDK call fails.
        """
        if self._client is None:
            return {"safe": True, "categories": [], "severity": 0}

        try:
            request = AnalyzeTextOptions(text=text)
            response = self._client.analyze_text(request)

            categories: list[str] = []
            max_severity = 0
            for item in response.categories_analysis:
                if item.severity and item.severity > 0:
                    categories.append(item.category)
                    if item.severity > max_severity:
                        max_severity = item.severity

            safe = max_severity < 4
            return {"safe": safe, "categories": categories, "severity": max_severity}
        except Exception as exc:
            logger.warning("Content safety check failed: %s", exc)
            return {"safe": True, "categories": [], "severity": 0}
