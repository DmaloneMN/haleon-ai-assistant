"""Triage agent: content safety + intent classification."""

import logging

from ..services.content_safety import ContentSafetyService

logger = logging.getLogger(__name__)

_ADVERSE_KEYWORDS = frozenset(
    {
        "side effects",
        "adverse event",
        "adverse reaction",
        "allergic reaction",
        "anaphylaxis",
        "overdose",
        "poisoning",
        "hospitalized",
        "hospitalised",
        "death",
        "died",
        "serious reaction",
        "unexpected reaction",
    }
)

_INTENT_KEYWORDS: dict[str, tuple[str, ...]] = {
    "pharmacovigilance": tuple(_ADVERSE_KEYWORDS),
    "dosage": ("dose", "dosage", "how much", "how many", "mg", "milligram", "tablet"),
    "warnings": ("caution", "warning", "contraindication"),
    "product_info": ("ingredient", "active", "composition", "contain", "formula", "what is"),
}


class TriageAgent:
    """Classifies user messages and checks content safety."""

    def __init__(self, content_safety_service: ContentSafetyService) -> None:
        self._safety = content_safety_service

    async def run(self, message: str, session_id: str) -> dict:
        """Triage *message* and return classification metadata."""
        safety_result = await self._safety.check(message)
        safe: bool = safety_result.get("safe", True)

        intent = self._classify_intent(message)
        flag_pv = intent == "pharmacovigilance" or self._contains_adverse_keywords(message)

        logger.info(
            "Triage session=%s intent=%s safe=%s flag_pv=%s",
            session_id,
            intent,
            safe,
            flag_pv,
        )

        return {
            "safe": safe,
            "intent": intent,
            "message": message,
            "session_id": session_id,
            "flag_pv": flag_pv,
        }

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _classify_intent(message: str) -> str:
        lower = message.lower()
        for intent, keywords in _INTENT_KEYWORDS.items():
            if any(kw in lower for kw in keywords):
                return intent
        return "general"

    @staticmethod
    def _contains_adverse_keywords(message: str) -> bool:
        lower = message.lower()
        return any(kw in lower for kw in _ADVERSE_KEYWORDS)
