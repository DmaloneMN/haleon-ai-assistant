"""Multi-agent orchestrator for Haleon AI Assistant."""

from __future__ import annotations

import asyncio
import logging
import uuid

from ..agents.pharmacovigilance import PharmacovigAgent
from ..agents.retrieval import RetrievalAgent
from ..agents.synthesis import SynthesisAgent
from ..agents.triage import TriageAgent
from ..models.schemas import ChatRequest, ChatResponse, Citation
from ..services.content_safety import ContentSafetyService
from ..services.search import SearchService

logger = logging.getLogger(__name__)

_BLOCKED_ANSWER = (
    "I'm sorry, but your message could not be processed as it may contain unsafe content. "
    "Please rephrase your question."
)
_BLOCKED_DISCLAIMER = (
    "Haleon AI Assistant enforces content safety policies. "
    "Please consult a healthcare professional for medical advice."
)
_DEFAULT_DISCLAIMER = (
    "This information is for general purposes only and does not constitute medical advice. "
    "Always consult a qualified healthcare professional before making health decisions."
)


class AgentOrchestrator:
    """Coordinates triage → retrieval → synthesis pipeline."""

    def __init__(self, settings) -> None:  # noqa: ANN001
        safety_svc = ContentSafetyService(
            endpoint=settings.azure_content_safety_endpoint,
            api_key=settings.azure_content_safety_key,
        )
        search_svc = SearchService(
            endpoint=settings.azure_search_endpoint,
            api_key=settings.azure_search_key,
            index_name=settings.azure_search_index,
        )

        self._triage = TriageAgent(content_safety_service=safety_svc)
        self._retrieval = RetrievalAgent(search_service=search_svc)
        self._synthesis = SynthesisAgent(
            openai_endpoint=settings.azure_openai_endpoint,
            openai_key=settings.azure_openai_api_key,
            deployment=settings.azure_openai_deployment,
            api_version=settings.azure_openai_api_version,
        )
        self._pv = PharmacovigAgent(
            openai_endpoint=settings.azure_openai_endpoint,
            openai_key=settings.azure_openai_api_key,
            deployment=settings.azure_openai_deployment,
            api_version=settings.azure_openai_api_version,
        )

    async def process(self, request: ChatRequest) -> ChatResponse:
        """Run the full multi-agent pipeline for *request*."""
        session_id = request.session_id or str(uuid.uuid4())
        message = request.message

        # Step 1 – Triage
        triage_result = await self._triage.run(message, session_id)

        # Step 2 – Block unsafe content
        if not triage_result.get("safe", True):
            logger.warning("Blocked unsafe message session=%s", session_id)
            return ChatResponse(
                session_id=session_id,
                answer=_BLOCKED_ANSWER,
                citations=[],
                disclaimer=_BLOCKED_DISCLAIMER,
                escalate=True,
            )

        intent: str = triage_result.get("intent", "general")
        flag_pv: bool = triage_result.get("flag_pv", False)

        # Step 3 – Parallel PV check + retrieval when PV flag is set
        if flag_pv:
            retrieval_result, pv_result = await asyncio.gather(
                self._retrieval.run(message, intent),
                self._pv.run(message, session_id),
            )
            if pv_result.get("detected"):
                logger.warning(
                    "PV event detected session=%s escalate=%s",
                    session_id,
                    pv_result.get("escalate"),
                )
        else:
            # Step 4 – Retrieval only
            retrieval_result = await self._retrieval.run(message, intent)
            pv_result = {"detected": False, "escalate": False}

        # Step 5 – Synthesis
        context: str = retrieval_result.get("context", "")
        documents: list[dict] = retrieval_result.get("documents", [])

        synthesis_result = await self._synthesis.run(message, context, documents, intent)

        # Step 6 – Build response
        raw_citations: list[dict] = synthesis_result.get("citations", [])
        citations = [
            Citation(
                source=c.get("source", ""),
                title=c.get("title", ""),
                url=c.get("url"),
                excerpt=c.get("excerpt"),
            )
            for c in raw_citations
        ]

        escalate = synthesis_result.get("escalate", False) or pv_result.get("escalate", False)

        return ChatResponse(
            session_id=session_id,
            answer=synthesis_result.get("answer", ""),
            citations=citations,
            disclaimer=_DEFAULT_DISCLAIMER,
            escalate=escalate,
        )
