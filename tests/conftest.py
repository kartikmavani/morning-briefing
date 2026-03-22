import pytest
from config.settings import AppSettings

@pytest.fixture
def mock_settings():
    """ Provides a fake settings environment isolated from .env """
    return AppSettings(
        database_url="postgresql://fake_user:fake_password@localhost:5432/fake_db",
        model_name="ollama:fake_model",
        tavily_api_key="tvly-mock-key-12345"
    )
