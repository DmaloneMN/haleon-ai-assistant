"""Synthesis agent: generates answers using Azure OpenAI."""

import logging

logger = logging.getLogger(__name__)

_STUB_DISCLAIMER = (
    "This information is for general purposes only and does not constitute medical advice. "
    "Always consult a qualified healthcare professional."
)

_SYSTEM_PROMPT = """You are a helpful AI assistant for Haleon, a global consumer healthcare company.
Your role is to provide accurate, evidence-based information about Haleon products.

Rules:
1. Answer ONLY based on the provided context. Do not invent or assume information.
2. Cite the source documents using [1], [2], etc. notation.
3. Always include a medical disclaimer at the end of your response.
4. If the context does not contain enough information, say so clearly and suggest the user consults a healthcare professional.
5. If you are uncertain, set escalate=true in your response metadata.
6. Never provide specific medical diagnoses or personalised treatment plans.
"""


class SynthesisAgent:
    """Generates grounded answers using Azure OpenAI chat completions."""

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
                logger.warning("Could not create AzureOpenAI client: %s", exc)

    async def run(
        self,
        message: str,
        context: str,
        documents: list[dict],
        intent: str,
    ) -> dict:
        """Generate an answer grounded in *context*.

        Returns a stub response when credentials are absent.
        """
        if self._client is None:
            return self._stub_response(documents)

        user_content = (
            f"Context:\n{context}\n\n"
            f"User question ({intent}): {message}\n\n"
            "Provide an answer citing sources and include a disclaimer."
        )

        try:
            completion = self._client.chat.completions.create(
                model=self._deployment,
                messages=[
                    {"role": "system", "content": _SYSTEM_PROMPT},
                    {"role": "user", "content": user_content},
                ],
                temperature=0.2,
                max_tokens=1024,
            )
            answer = completion.choices[0].message.content or ""
            escalate = "uncertain" in answer.lower() or "consult" in answer.lower()
            citations = self._extract_citations(documents)

            logger.info("Synthesis completed intent=%s escalate=%s", intent, escalate)
            return {
                "answer": answer,
                "citations": citations,
                "escalate": escalate,
            }
        except Exception as exc:
            logger.error("Synthesis failed: %s", exc)
            return self._stub_response(documents)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _extract_citations(documents: list[dict]) -> list[dict]:
        citations: list[dict] = []
        for doc in documents:
            citations.append(
                {
                    "source": doc.get("source", ""),
                    "title": doc.get("title", ""),
                    "url": doc.get("url"),
                    "excerpt": (doc.get("content") or "")[:200],
                }
            )
        return citations

    @staticmethod
    def _stub_response(documents: list[dict]) -> dict:
        return {
            "answer": (
                "I currently don't have enough information to answer your question. "
                "Please consult a healthcare professional or visit the Haleon website for accurate information. "
                + _STUB_DISCLAIMER
            ),
            "citations": SynthesisAgent._extract_citations(documents),
            "escalate": False,
        }
