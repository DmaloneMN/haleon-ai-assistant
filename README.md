# haleon-ai-assistant

AI-powered multi-agent assistant built for Haleon using [AutoGen](https://github.com/microsoft/autogen), Azure OpenAI, and Azure AI Search, exposed via a [FastAPI](https://fastapi.tiangolo.com/) HTTP interface.

## Architecture

```
User (web / mobile / call-centre / clinician portal)
        │
        ▼
┌─────────────────────────────────────────────────────────────┐
│                     FastAPI Application                     │
│  POST /chat    POST /feedback    GET /health                │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                  AgentOrchestrator                          │
│                                                             │
│  1. TriageAgent          ← Azure Content Safety + keywords  │
│  2. RetrievalAgent       ← Azure AI Search (hybrid+vector)  │
│  3. PharmacovigAgent     ← Azure OpenAI (parallel, if PV)   │
│  4. SynthesisAgent       ← Azure OpenAI GPT-4o              │
└─────────────────────────────────────────────────────────────┘
```

### Agent Pipeline

| Step | Agent | Responsibility |
|------|-------|----------------|
| 1 | **TriageAgent** | PII/safety screening via Azure Content Safety; keyword-based intent classification (`dosage`, `product_info`, `side_effects`, `pharmacovigilance`, `general`) |
| 2 | **RetrievalAgent** | Hybrid + vector search against the Haleon knowledge base in Azure AI Search (IFUs, SmPCs, FAQs, safety notices) |
| 3 | **PharmacovigAgent** | Detects adverse events; runs in parallel with retrieval when PV flag is set |
| 4 | **SynthesisAgent** | Grounded answer generation using Azure OpenAI GPT-4o; returns answer + citations + disclaimer |

## Prerequisites

- Python 3.10+
- (Optional) Redis for session/cache support

## Quick start

```bash
# Clone the repo (if you haven't already)
git clone https://github.com/DmaloneMN/haleon-ai-assistant.git
cd haleon-ai-assistant

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env and fill in your Azure credentials

# Run the development server
uvicorn src.haleon_assistant.main:app --reload
```

The API will be available at <http://localhost:8000>.  
Interactive docs: <http://localhost:8000/docs>

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Liveness check |
| `POST` | `/chat` | Submit a question; returns answer + citations + disclaimer |
| `POST` | `/feedback` | Submit thumbs-up/down feedback for a response |

### POST /chat

```json
// Request
{
  "session_id": "optional-uuid",
  "message": "What is the dosage for Panadol for adults?",
  "channel": "web"
}

// Response
{
  "session_id": "uuid",
  "answer": "The recommended adult dose of Panadol is ...",
  "citations": [
    {
      "source": "panadol-ifu-2024.pdf",
      "title": "Panadol IFU – Dosage",
      "url": "https://...",
      "excerpt": "..."
    }
  ],
  "disclaimer": "This information is for general purposes only ...",
  "escalate": false
}
```

## Project structure

```
haleon-ai-assistant/
├── src/
│   └── haleon_assistant/
│       ├── __init__.py
│       ├── main.py              # FastAPI app entry point
│       ├── config.py            # Settings from environment variables
│       ├── agents/
│       │   ├── orchestrator.py  # Multi-agent pipeline coordinator
│       │   ├── triage.py        # Content safety + intent classification
│       │   ├── retrieval.py     # Azure AI Search grounded retrieval
│       │   ├── synthesis.py     # Azure OpenAI answer generation
│       │   └── pharmacovigilance.py  # Adverse event detection
│       ├── routers/
│       │   ├── chat.py          # POST /chat
│       │   └── feedback.py      # POST /feedback
│       ├── services/
│       │   ├── content_safety.py # Azure Content Safety client
│       │   ├── search.py         # Azure AI Search client
│       │   └── ingestion.py      # Document ingestion pipeline
│       └── models/
│           └── schemas.py        # Pydantic request/response models
├── infra/
│   ├── main.bicep               # Root Bicep template
│   ├── deploy.sh                # Azure CLI deployment script
│   └── modules/
│       ├── openai.bicep
│       ├── search.bicep
│       ├── keyvault.bicep
│       └── monitoring.bicep
├── tests/
│   ├── conftest.py
│   ├── test_health.py
│   ├── test_chat.py
│   ├── test_feedback.py
│   ├── test_agents.py
│   └── red_team/
│       ├── test_hallucination.py
│       ├── test_jailbreak.py
│       └── test_compliance.py
├── .github/
│   └── workflows/
│       ├── ci.yml               # Lint + test on every push/PR
│       └── cd.yml               # Deploy infra + app on merge to main
├── Dockerfile
├── .env.example
├── .gitignore
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Infrastructure (IaC)

Bicep templates under `infra/` provision:

| Resource | Purpose |
|----------|---------|
| Azure OpenAI (GPT-4o) | Synthesise answers |
| Azure AI Search | Hybrid vector retrieval |
| Azure Storage Account | Document source (IFUs, PDFs) |
| Azure Key Vault | Secrets management |
| Log Analytics + App Insights | Observability & monitoring |

```bash
# Deploy to Azure
export AZURE_RESOURCE_GROUP=rg-haleon-ai
export AZURE_LOCATION=uksouth
export RESOURCE_PREFIX=haleon

# Set secrets as env vars before running
export AZURE_OPENAI_API_KEY=<key>
export AZURE_SEARCH_KEY=<key>

chmod +x infra/deploy.sh
./infra/deploy.sh "$AZURE_RESOURCE_GROUP" "$AZURE_LOCATION" "$RESOURCE_PREFIX"
```

## Document Ingestion

Use the `IngestionService` to index documents from Azure Blob Storage into Azure AI Search:

```python
from haleon_assistant.services.ingestion import IngestionService

svc = IngestionService(
    storage_account_url="https://<account>.blob.core.windows.net",
    container="documents",
    search_endpoint="https://<search>.search.windows.net",
    search_key="<key>",
    index_name="haleon-docs",
)

# Index a single blob
result = await svc.ingest_blob("panadol-ifu-2024.pdf")
print(result)  # {"blob": "panadol-ifu-2024.pdf", "chunks_indexed": 12}
```

## Dependencies

| Package | Purpose |
|---------|---------|
| `autogen-ext[azure,openai]` | AutoGen Azure/OpenAI model integrations |
| `autogen-agentchat` | Multi-agent chat orchestration |
| `fastapi[standard]` | Web framework |
| `openai>=1.0.0` | Azure OpenAI SDK |
| `azure-search-documents` | Azure AI Search client |
| `azure-ai-contentsafety` | Content safety moderation |
| `azure-identity` | Azure credential helpers |
| `azure-keyvault-secrets` | Azure Key Vault secret access |
| `azure-storage-blob` | Azure Blob Storage client |
| `redis` | Redis client for caching/sessions |
| `python-dotenv` | Load `.env` variables at runtime |
| `uvicorn` | ASGI server |
