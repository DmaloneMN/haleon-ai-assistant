"""Orchestrator – coordinates all sub-agents to answer a user query.

TODO: replace stub calls with real AutoGen / Azure OpenAI agent invocations.
"""

from haleon_assistant.agents.retrieval_agent import RetrievalAgent
from haleon_assistant.agents.safety_agent import SafetyAgent
from haleon_assistant.agents.synthesis_agent import SynthesisAgent
from haleon_assistant.agents.triage_agent import TriageAgent


class Orchestrator:
    """Top-level orchestrator that wires triage → retrieval → safety → synthesis."""

    def __init__(self) -> None:
        self._triage = TriageAgent()
        self._retrieval = RetrievalAgent()
        self._safety = SafetyAgent()
        self._synthesis = SynthesisAgent()

    def run(self, query: str) -> dict:
        """Run the full pipeline and return a result dict.

        Returns:
            dict with keys ``answer`` (str) and ``citations`` (list).
        """
        route = self._triage.classify(query)
        documents = self._retrieval.retrieve(query, route=route)
        safety_result = self._safety.check(query)
        if not safety_result["pass"]:
            return {"answer": "I cannot answer that query.", "citations": []}
        return self._synthesis.compose(query, documents)
