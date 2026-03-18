# haleon-ai-assistant

AI-powered assistant built with [AutoGen](https://github.com/microsoft/autogen) and Azure services, exposed via a [FastAPI](https://fastapi.tiangolo.com/) HTTP interface.

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

## Project structure

```
haleon-ai-assistant/
├── src/
│   └── haleon_assistant/
│       ├── __init__.py
│       └── main.py          # FastAPI app entry point
├── .env.example             # Environment variable template
├── .gitignore
├── pyproject.toml           # Project metadata & build config
├── requirements.txt         # Pinned/unpinned runtime dependencies
└── README.md
```

## Dependencies

| Package | Purpose |
|---|---|
| `autogen-ext[azure,openai]` | AutoGen Azure/OpenAI model integrations |
| `autogen-agentchat` | Multi-agent chat orchestration |
| `fastapi[standard]` | Web framework |
| `azure-search-documents` | Azure AI Search client |
| `azure-ai-contentsafety` | Content safety moderation |
| `azure-identity` | Azure credential helpers |
| `azure-keyvault-secrets` | Azure Key Vault secret access |
| `azure-storage-blob` | Azure Blob Storage client |
| `redis` | Redis client for caching/sessions |
| `python-dotenv` | Load `.env` variables at runtime |
| `uvicorn` | ASGI server |