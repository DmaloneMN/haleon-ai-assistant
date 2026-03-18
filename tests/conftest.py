"""Pytest fixtures for Haleon AI Assistant tests."""

import pytest
from fastapi.testclient import TestClient

from haleon_assistant.config import Settings
from haleon_assistant.main import app


@pytest.fixture()
def client():
    """Return a synchronous TestClient for the FastAPI app."""
    with TestClient(app) as c:
        yield c


class _EmptySettings(Settings):
    """Settings subclass that clears all Azure credentials for testing."""

    def __init__(self) -> None:
        super().__init__()
        self.azure_openai_endpoint = ""
        self.azure_openai_api_key = ""
        self.azure_search_endpoint = ""
        self.azure_search_key = ""
        self.azure_content_safety_endpoint = ""
        self.azure_content_safety_key = ""
        self.azure_key_vault_url = ""
        self.azure_storage_account_url = ""


@pytest.fixture()
def mock_settings() -> _EmptySettings:
    """Return a Settings instance with all Azure credentials set to empty strings."""
    return _EmptySettings()
