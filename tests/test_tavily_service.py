import pytest
from service.TaviliyService import TavilyService

def test_tavily_service_initialization(mock_settings, mocker):
    mock_client = mocker.patch("service.TaviliyService.TavilyClient")
    
    service = TavilyService(mock_settings)
    mock_client.assert_called_once_with("tvly-mock-key-12345")

def test_tavily_search_news(mock_settings, mocker):
    mocker.patch("service.TaviliyService.TavilyClient")
    service = TavilyService(mock_settings)
    
    # Intercept API Response
    service.client.search.return_value = {"results": [{"title": "Test AI News"}]}
    
    result = service.search_news_from_web("AI", "2026-03-21", "2026-03-22")
    
    # Verification
    assert result == {"results": [{"title": "Test AI News"}]}
    service.client.search.assert_called_once_with(
        query="AI",
        topic="news",
        search_depth="advanced",
        start_date="2026-03-21",
        end_date="2026-03-22"
    )
