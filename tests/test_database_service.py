import pytest
from service.DatabaseService import DatabaseService

def test_database_service_boot(mock_settings, mocker):
    mock_pool = mocker.patch("service.DatabaseService.ConnectionPool")
    mock_saver = mocker.patch("service.DatabaseService.PostgresSaver")
    
    db_service = DatabaseService(mock_settings)
    
    # Verify pool mapping
    mock_pool.assert_called_once()
    pool_kwargs = mock_pool.call_args[1]
    assert pool_kwargs["min_size"] == mock_settings.db_pool_min_size
    assert pool_kwargs["max_size"] == mock_settings.db_pool_max_size
    
    # Verify LangGraph Saver integration
    mock_saver.assert_called_once_with(mock_pool.return_value)
    mock_saver.return_value.setup.assert_called_once()
    
    # Verify singleton getter
    assert db_service.get_checkpointer() == mock_saver.return_value
