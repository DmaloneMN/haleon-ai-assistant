from typing import Dict

from haleon_assistant.agents.retrieval_agent import RetrievalAgent
from haleon_assistant.agents.safety_agent import SafetyAgent
from haleon_assistant.agents.synthesis_agent import SynthesisAgent
from haleon_assistant.agents.triage_agent import TriageAgent


class Orchestrator:
    """Simple orchestrator that wires together triage, retrieval, safety, and synthesis."""

    def __init__(self) -> None:
        self.triage = TriageAgent()
        self.retrieval = RetrievalAgent()
        self.safety = SafetyAgent()
        self.synthesis = SynthesisAgent()

    def run(self, query: str) -> Dict:
        """Run the basic pipeline and return a result dict with answer and citations."""
        _ = query or ""
        route = self.triage.classify(query)
        docs = self.retrieval.retrieve(query)
        safety = self.safety.check(query, docs)
        if not safety.get("ok", True):
            return {"answer": "Content blocked by safety policy", "citations": []}
        answer = self.synthesis.synthesize(query, docs)
        return {"answer": answer, "citations": docs, "route": route}
