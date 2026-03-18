# Agent Design

## Agent Pipeline

The assistant uses a sequential multi-agent pipeline:

1. **TriageAgent** – classifies the intent of the user's query into one of:
   `dosage`, `side_effects`, `pharmacovigilance`, `general`.

2. **RetrievalAgent** – fetches relevant documents from Azure AI Search using
   the query and the route returned by the triage agent.

3. **SafetyAgent** – checks the query for PII, toxicity, and self-harm signals
   before any answer is generated.

4. **SynthesisAgent** – composes a grounded answer using the retrieved
   documents and an Azure OpenAI GPT-4 deployment.

5. **PharmacovigilanceAgent** – runs in parallel to detect adverse event
   signals and trigger regulatory reporting workflows.

## Adding a New Agent

1. Create `src/haleon_assistant/agents/<name>_agent.py`.
2. Implement a class with at least one public method.
3. Register the agent in `orchestrator.py`.
4. Add a unit test in `tests/unit/test_<name>_agent.py`.

## Prompt Templates

Prompt templates live in `src/haleon_assistant/prompts/`.
Use `{{variable}}` placeholders for dynamic content.
