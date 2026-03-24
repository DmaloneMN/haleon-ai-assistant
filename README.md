# Haleon AI Assistant

AI-powered healthcare assistant built with FastAPI and Azure services.
All agent and tool implementations are **stubs** – see TODO comments throughout
the codebase for where real logic must be added.

## Prerequisites

- Python 3.10+
- (Optional) Redis for cache support
- (Optional) Azure subscription for real AI services

## Quick start

```bash
# Clone the repo
git clone https://github.com/DmaloneMN/haleon-ai-assistant.git
cd haleon-ai-assistant

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install the package (editable) plus test dependencies
pip install -e .[test]

# Configure environment variables
cp .env.example .env
# Edit .env and fill in your Azure credentials (optional for local dev)

# Run the development server
uvicorn haleon_assistant.main:app --reload
```

The API will be available at <http://localhost:8000>.  
Interactive docs: <http://localhost:8000/docs>

## Running tests

```bash
pytest -v
```

## Docker

```bash
docker-compose up --build
```

## Project structure

```
haleon-ai-assistant/
├── src/haleon_assistant/
│   ├── __init__.py
│   ├── main.py                  # FastAPI app entry point
│   ├── api/
│   │   ├── routes/              # health, chat, feedback routers
│   │   └── middleware/          # auth, rate_limit middleware
│   ├── agents/                  # triage, retrieval, safety, synthesis, PV
│   ├── tools/                   # search, dosage, content_safety, cache
│   ├── ingestion/               # chunker, embedder, indexer, pipeline
│   └── prompts/                 # system prompt text files
├── tests/
│   ├── unit/                    # agent unit tests
│   ├── integration/             # end-to-end FastAPI tests
│   └── red_team/                # hallucination / jailbreak placeholders
├── infra/                       # Bicep IaC templates
├── docs/                        # Architecture and runbook
├── Dockerfile
├── docker-compose.yml
└── pyproject.toml
```

## Key dependencies

| Package | Purpose |
|---------|---------|
| `fastapi` | Web framework |
| `uvicorn` | ASGI server |
| `pytest` / `httpx` | Testing |

<--body chore/update-readme: confirmed -->
