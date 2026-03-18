# Architecture

## Overview

The Haleon AI Assistant is a FastAPI-based web application that routes user
queries through a multi-agent pipeline backed by Azure AI services.

```
User → FastAPI App → Orchestrator
                         ├── TriageAgent        (intent classification)
                         ├── RetrievalAgent     (Azure AI Search)
                         ├── SafetyAgent        (Azure Content Safety)
                         └── SynthesisAgent     (Azure OpenAI GPT-4)
```

## Key Components

| Component | Technology | Status |
|-----------|-----------|--------|
| API layer | FastAPI + Uvicorn | Stub |
| Triage | Keyword / LLM classifier | Stub |
| Retrieval | Azure AI Search | Stub |
| Safety | Azure Content Safety | Stub |
| Synthesis | Azure OpenAI | Stub |
| Cache | Redis (in-memory fallback) | Stub |
| Ingestion | Chunker → Embedder → Indexer | Stub |

## Infrastructure

All Azure resources are provisioned via Bicep templates in the `infra/` folder.
See `deployment-guide.md` for deployment instructions.

## Next Steps

- Replace all stubs with real Azure SDK calls.
- Add authentication and authorisation (see `api/middleware/auth.py`).
- Configure rate limiting backed by Redis.
- Set up CI/CD deployment pipeline.
