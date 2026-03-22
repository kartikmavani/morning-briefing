import pytest
from core.ApplicationContainer import ApplicationContainer
from config.AppSettings import AppSettings
from service.AudioService import AudioService

def test_container_dependency_resolution(mocker):
    # Standard practice is to mock the heavy subsystems to prevent IoC initialization from hitting the physical OS
    mocker.patch("service.DatabaseService.ConnectionPool")
    mocker.patch("service.DatabaseService.PostgresSaver")
    mocker.patch("service.LlmService.init_chat_model")
    mocker.patch("service.LlmService.create_agent")
    
    container = ApplicationContainer()
    
    # Override settings explicitly for the test suite
    container.settings.override(
        AppSettings(
            database_url="postgresql://usr:pass@127.0.0.1:5432/testdb",
            model_name="test_model:1",
            tavily_api_key="tvly-test-test"
        )
    )
    
    # Ensure independent services map to the correct singletons
    assert container.settings().database_url == "postgresql://usr:pass@127.0.0.1:5432/testdb"
    assert isinstance(container.audio_service(), AudioService)

    # Ensure injected dependencies are correctly propagated downward
    llm = container.llm_service()
    db = container.db_service()
    
    assert llm is not None
    assert db is not None
