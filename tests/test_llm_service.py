import pytest
from unittest.mock import MagicMock
from langchain_core.messages import AIMessage
from service.LlmService import LlmService

def test_llm_service_initialization(mock_settings, mocker):
    mock_init_chat = mocker.patch("service.LlmService.init_chat_model")
    mock_create_agent = mocker.patch("service.LlmService.create_agent")
    mock_structured_tool = mocker.patch("service.LlmService.StructuredTool.from_function")
    
    mock_db = MagicMock()
    mock_tavily = MagicMock()
    
    service = LlmService(mock_db, mock_tavily, mock_settings)
    
    # Validate core model initialization
    mock_init_chat.assert_called_once_with(model="ollama:fake_model", temperature=0)
    
    # Validate tool mapping
    mock_structured_tool.assert_called_once_with(
        func=mock_tavily.search_news_from_web,
        name="search_news_from_web",
        description="Search for news from the web using Tavily API. Requires query, start_date, and end_date strings."
    )
    
    # Validate agent injection
    mock_create_agent.assert_called_once_with(
        model=mock_init_chat.return_value,
        tools=[mock_structured_tool.return_value],
        checkpointer=mock_db.get_checkpointer.return_value,
        system_prompt="You are a news summarizer. Summarize the news for the user in podcast format. This podcast is hosted by Kartik"
    )

def test_get_news_execution_flow(mock_settings, mocker):
    mocker.patch("service.LlmService.init_chat_model")
    mock_create_agent = mocker.patch("service.LlmService.create_agent")
    mocker.patch("service.LlmService.StructuredTool.from_function")
    
    # Date patch to prevent dynamic variations
    mocker.patch("service.LlmService.datetime").now.return_value.strftime.return_value = "2026-03-22 12:00:00"
    
    service = LlmService(MagicMock(), MagicMock(), mock_settings)
    
    # Mocking the agent response
    mock_response = {"messages": [AIMessage(content="Here is your news from Kartik.")]}
    mock_create_agent.return_value.invoke.return_value = mock_response
    
    result = service.get_news("AI", "2026-03-21", "2026-03-22")
    
    # Verify exact string output extraction
    assert result == "Here is your news from Kartik."
    
    # Verify input invocation schema
    mock_create_agent.return_value.invoke.assert_called_once()
    args, kwargs = mock_create_agent.return_value.invoke.call_args
    
    assert "messages" in args[0]
    expected_prompt = "Search news from web about \"AI\" from start date : \"2026-03-21\" to end date : \"2026-03-22\""
    assert args[0]["messages"][0].content == expected_prompt
    assert kwargs["config"]["configurable"]["thread_id"] == "2026-03-22 12:00:00"
