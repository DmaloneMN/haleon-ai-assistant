"""Pharmacovigilance agent: detects and logs adverse events."""

import logging

logger = logging.getLogger(__name__)

_PV_SYSTEM_PROMPT = """You are a pharmacovigilance specialist AI for Haleon.
Your task is to analyse user messages for potential adverse drug reactions or events.

Rules:
1. Identify any mention of unexpected symptoms, side effects, or health changes after taking a Haleon product.
2. Summarise the potential adverse event clearly and concisely.
3. Indicate whether the report should be escalated to the pharmacovigilance team.
4. Do NOT provide medical advice or diagnoses.
"""


class PharmacovigAgent:
    """Detects adverse events and flags them for regulatory compliance."""

    def __init__(
        self,
        openai_endpoint: str,
        openai_key: str,
        deployment: str,
        api_version: str = "2024-02-01",
    ) -> None:
        self._endpoint = openai_endpoint or ""
        self._key = openai_key or ""
        self._deployment = deployment or "gpt-4o"
        self._api_version = api_version
        self._client = None

        if self._endpoint and self._key:
            try:
                from openai import AzureOpenAI

                self._client = AzureOpenAI(
                    azure_endpoint=self._endpoint,
                    api_key=self._key,
                    api_version=self._api_version,
                )
            except Exception as exc:
                logger.warning("Could not create AzureOpenAI client for PV: %s", exc)

    async def run(self, message: str, session_id: str) -> dict:
        """Analyse *message* for adverse events.

        Returns a stub when credentials are absent.
        """
        if self._client is None:
            return self._stub_response(session_id)

        try:
            completion = self._client.chat.completions.create(
                model=self._deployment,
                messages=[
                    {"role": "system", "content": _PV_SYSTEM_PROMPT},
                    {"role": "user", "content": message},
                ],
                temperature=0.1,
                max_tokens=512,
            )
            answer = completion.choices[0].message.content or ""
            detected = any(
                kw in answer.lower()
                for kw in ["adverse", "reaction", "side effect", "symptom", "report"]
            )
            escalate = detected

            if detected:
                logger.warning(
                    "PHARMACOVIGILANCE EVENT DETECTED session=%s summary=%s",
                    session_id,
                    answer[:200],
                )

            return {
                "detected": detected,
                "summary": answer,
                "escalate": escalate,
                "session_id": session_id,
            }
        except Exception as exc:
            logger.error("Pharmacovigilance check failed: %s", exc)
            return self._stub_response(session_id)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _stub_response(session_id: str) -> dict:
        return {
            "detected": False,
            "summary": "",
            "escalate": False,
            "session_id": session_id,
        }
