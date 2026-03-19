"""Orchestrator – coordinates all sub-agents to answer a user query."""

from haleon_assistant.agents.retrieval_agent import RetrievalAgent
from haleon_assistant.agents.safety_agent import SafetyAgent
from haleon_assistant.agents.synthesis_agent import SynthesisAgent
from haleon_assistant.agents.triage_agent import TriageAgent


class Orchestrator:
    """Top-level orchestrator that wires triage → retrieval → safety → synthesis."""

    def __init__(self) -> None:
        self.triage = TriageAgent()
        self.retrieval = RetrievalAgent()
        self.safety = SafetyAgent()
        self.synthesis = SynthesisAgent()

    def run(self, query: str) -> dict:
        """Run the full pipeline and return a result dict.

        Returns:
            dict with keys ``answer`` (str) and ``citations`` (list).
        """
        _route = self.triage.classify(query)
        docs = self.retrieval.retrieve(query)
        safe = self.safety.check(query, docs)
        if not safe.get("ok", True):
            return {"answer": "Content flagged by safety filters", "citations": []}
        answer = self.synthesis.synthesize(query, docs)
        return {"answer": answer, "citations": docs}
