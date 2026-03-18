"""Unit tests for individual agents."""

import asyncio

import pytest

from haleon_assistant.agents.retrieval import RetrievalAgent
from haleon_assistant.agents.synthesis import SynthesisAgent
from haleon_assistant.agents.triage import TriageAgent
from haleon_assistant.services.content_safety import ContentSafetyService
from haleon_assistant.services.search import SearchService


def test_triage_safe_message():
    safety = ContentSafetyService(endpoint="", api_key="")
    agent = TriageAgent(content_safety_service=safety)
    result = asyncio.get_event_loop().run_until_complete(
        agent.run("What is the dosage for Panadol?", "sess-001")
    )
    assert result["safe"] is True
    assert "intent" in result
    assert result["session_id"] == "sess-001"


def test_retrieval_empty_results():
    search = SearchService(endpoint="", api_key="", index_name="")
    agent = RetrievalAgent(search_service=search)
    result = asyncio.get_event_loop().run_until_complete(
        agent.run("What is ibuprofen?", "general")
    )
    assert result["documents"] == []
    assert "context" in result


def test_synthesis_stub():
    agent = SynthesisAgent(openai_endpoint="", openai_key="", deployment="gpt-4o")
    result = asyncio.get_event_loop().run_until_complete(
        agent.run("What is Panadol?", "", [], "product_info")
    )
    assert isinstance(result["answer"], str)
    assert len(result["answer"]) > 0
    assert "citations" in result
    assert "escalate" in result
