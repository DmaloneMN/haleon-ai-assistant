# Haleon AI Assistant

AI-powered healthcare assistant built with FastAPI and Azure services.
All agent and tool implementations are currently **deterministic stubs** – see
TODO comments throughout the codebase for where real logic must be wired in.

## What is implemented

### Agents (`src/haleon_assistant/agents/`)

| Agent | File | Description |
|-------|------|-------------|
| Orchestrator | `orchestrator.py` | Top-level request router; delegates to agents |
| Triage | `triage_agent.py` | Classifies incoming queries by intent/category |
| Retrieval | `retrieval_agent.py` | Fetches relevant docs via `SearchTool` |
| Safety | `safety_agent.py` | Runs content checks via `content_safety_tool` |
| Synthesis | `synthesis_agent.py` | Combines retrieved docs into a response |
| Pharmacovigilance | `pharmacovigilance_agent.py` | Adverse-event / PV signal detection |

### Tools (`src/haleon_assistant/tools/`)

| Tool | File | Description |
|------|------|-------------|
| SearchTool | `search_tool.py` | Keyword search stub (pluggable backend) |
| CacheTool | `cache_tool.py` | In-memory / Redis cache wrapper |
| DosageTool | `dosage_tool.py` | Deterministic dosage look-up |
| ContentSafetyTool | `content_safety_tool.py` | Deterministic `check_content()` stub |

### Ingestion (`src/haleon_assistant/ingestion/`)

`chunker.py` → `embedder.py` → `indexer.py` wired together by `pipeline.py`.

### Prompts (`src/haleon_assistant/prompts/`)

Plain-text system prompt templates:
`triage_system.txt`, `retrieval_system.txt`, `synthesis_system.txt`,
`safety_rules.txt`, `pharmacovigilance_rules.txt`.

### API (`src/haleon_assistant/api/`)

FastAPI routers for `/api/v1/health`, `/api/v1/chat`, `/api/v1/feedback`,
plus `auth` and `rate_limit` middleware stubs.

### Tests

| Directory | Contents |
|-----------|----------|
| `tests/unit/` | Unit tests for `TriageAgent`, `RetrievalAgent`, `SafetyAgent` |
| `tests/integration/` | End-to-end FastAPI test (`test_e2e_flow.py`) |
| `tests/red_team/` | `@pytest.mark.xfail` placeholder tests for hallucination, jailbreak, and medical-claim detection |

## Project layout

```
haleon-ai-assistant/
├── src/haleon_assistant/
│   ├── main.py                  # FastAPI app entry point
│   ├── api/
│   │   ├── routes/              # health, chat, feedback routers
│   │   └── middleware/          # auth, rate_limit stubs
│   ├── agents/                  # orchestrator + five specialist agents
│   ├── tools/                   # cache, search, dosage, content_safety
│   ├── ingestion/               # chunker, embedder, indexer, pipeline
│   └── prompts/                 # *.txt system prompt templates
├── tests/
│   ├── unit/                    # agent unit tests
│   ├── integration/             # end-to-end FastAPI tests
│   └── red_team/                # xfail adversarial-test placeholders
├── infra/                       # Bicep IaC – see Azure deployment below
│   ├── main.bicep
│   ├── modules/                 # openai, search, storage, redis, keyvault, …
│   └── parameters/              # dev / staging / prod parameter files
├── docs/                        # architecture.md, deployment-guide.md, runbook.md
├── .env.example                 # environment variable template
├── Dockerfile
├── docker-compose.yml
└── pyproject.toml
```

## Key dependencies

| Package | Purpose |
|---------|---------|
| `fastapi` | Web framework |
| `uvicorn[standard]` | ASGI server |
| `pytest` / `httpx` | Testing |
| `pytest-asyncio` | Async test support |
| `ruff` | Linter and formatter |
| `autoflake` | Unused-import removal |

## Prerequisites

- Python 3.10+
- (Optional) Redis – required only if `REDIS_URL` is configured
- (Optional) Azure subscription – all Azure calls are stubbed for local dev

## Running locally

```bash
# 1. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 2. Install the package (editable) plus test + dev dependencies
pip install -e .[test]
pip install -r requirements-dev.txt

# 3. Configure environment variables (all Azure values are optional locally)
cp .env.example .env
# Edit .env if you want to enable real Azure services

# 4. Start the development server
uvicorn haleon_assistant.main:app --reload
```

API base URL: <http://localhost:8000>  
Interactive docs: <http://localhost:8000/docs>

## Running tests

```bash
# Unit tests only
pytest -q tests/unit

# All tests (unit + integration + red-team xfail placeholders)
pytest -v
```

## Linting and formatting

```bash
# Auto-format
ruff format src tests

# Remove unused imports
autoflake --in-place --remove-all-unused-imports -r src tests

# Check for lint issues
ruff check src tests
```

## Docker

```bash
docker-compose up --build
```

This starts the FastAPI app (port 8000) and a Redis 7 container.

## Azure deployment checklist

1. **Environment variables** – copy `.env.example` to `.env` (never commit
   `.env`) and fill in the Azure credentials listed below:

   | Variable | Azure service |
   |----------|---------------|
   | `AZURE_OPENAI_ENDPOINT` / `AZURE_OPENAI_API_KEY` / `AZURE_OPENAI_DEPLOYMENT` | Azure OpenAI |
   | `AZURE_SEARCH_ENDPOINT` / `AZURE_SEARCH_KEY` / `AZURE_SEARCH_INDEX` | Azure AI Search |
   | `AZURE_CONTENT_SAFETY_ENDPOINT` / `AZURE_CONTENT_SAFETY_KEY` | Azure Content Safety |
   | `AZURE_KEYVAULT_URL` | Azure Key Vault |
   | `AZURE_STORAGE_ACCOUNT_URL` / `AZURE_STORAGE_CONTAINER` | Azure Blob Storage |
   | `REDIS_URL` | Azure Cache for Redis (or local) |

2. **Infrastructure as Code** – Bicep templates are in `infra/`.
   Deployment parameters live in `infra/parameters/` (dev / staging / prod).
   Deploy with:
   ```bash
   az deployment sub create \
     --location <region> \
     --template-file infra/main.bicep \
     --parameters infra/parameters/dev.bicepparam
   ```

3. **Container image** – build and push to Azure Container Registry:
   ```bash
   docker build -t <acr-name>.azurecr.io/haleon-assistant:latest .
   docker push <acr-name>.azurecr.io/haleon-assistant:latest
   ```

4. **Managed Identity** – use Azure Managed Identity in production instead
   of API keys.  Remove raw key variables and reference Key Vault secrets.

## Creating a pull request

```bash
git checkout -b feat/<your-feature>
# ... make changes ...
git add -p
git commit -m "feat: <short description>"
git push -u origin feat/<your-feature>
gh pr create --base main --title "feat: <short description>" --body "<details>"
```

## Recommended next steps

1. Replace `content_safety_tool.check_content()` stub with a real call to
   the Azure Content Safety SDK.
2. Wire `SearchTool` to Azure AI Search using the credentials in `.env`.
3. Connect `embedder.py` to an Azure OpenAI embeddings deployment.
4. Implement red-team tests in `tests/red_team/` (currently `xfail`
   placeholders for hallucination, jailbreak, and medical-claim detection).
5. Restrict CORS origins in `main.py` before deploying to production.

## Housekeeping

- Delete merged feature branches locally and remotely once PRs are merged:
  ```bash
  git branch -d feat/<branch>
  git push origin --delete feat/<branch>
  ```
- Remove any stray patch files (`*.patch`) from the repository root if
  they were accidentally committed.
