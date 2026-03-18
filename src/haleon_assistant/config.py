"""Configuration management using os.getenv for Haleon AI Assistant."""

import os


class Settings:
    """Application settings loaded from environment variables."""

    # Azure OpenAI
    azure_openai_endpoint: str
    azure_openai_api_key: str
    azure_openai_deployment: str
    azure_openai_api_version: str

    # Azure AI Search
    azure_search_endpoint: str
    azure_search_key: str
    azure_search_index: str

    # Azure Content Safety
    azure_content_safety_endpoint: str
    azure_content_safety_key: str

    # Azure Key Vault
    azure_key_vault_url: str

    # Azure Storage
    azure_storage_account_url: str
    azure_storage_container: str

    # Redis
    redis_url: str

    # Server
    host: str
    port: int
    reload: bool

    def __init__(self) -> None:
        self.azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "")
        self.azure_openai_api_key = os.getenv("AZURE_OPENAI_API_KEY", "")
        self.azure_openai_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o")
        self.azure_openai_api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01")

        self.azure_search_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT", "")
        self.azure_search_key = os.getenv("AZURE_SEARCH_KEY", "")
        self.azure_search_index = os.getenv("AZURE_SEARCH_INDEX", "haleon-docs")

        self.azure_content_safety_endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT", "")
        self.azure_content_safety_key = os.getenv("AZURE_CONTENT_SAFETY_KEY", "")

        self.azure_key_vault_url = os.getenv("AZURE_KEY_VAULT_URL", "")

        self.azure_storage_account_url = os.getenv("AZURE_STORAGE_ACCOUNT_URL", "")
        self.azure_storage_container = os.getenv("AZURE_STORAGE_CONTAINER", "documents")

        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")

        self.host = os.getenv("HOST", "127.0.0.1")
        self.port = int(os.getenv("PORT", "8000"))
        self.reload = os.getenv("RELOAD", "false").lower() == "true"


_settings: Settings | None = None


def get_settings() -> Settings:
    """Return a cached Settings instance."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
