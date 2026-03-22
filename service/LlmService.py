import logging
from dependency_injector import containers, providers
from service.DatabaseService import DatabaseService
from service.TaviliyService import TavilyService
from config.AppSettings import AppSettings
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from datetime import datetime

from langchain_core.tools import StructuredTool

logger = logging.getLogger(__name__)


class LlmService:
    """
    A service class designated to initialize and hold our AI models and agents.
    """
    def __init__(self, db_service: DatabaseService, tavily_service: TavilyService, settings: AppSettings):    
        logger.info(f"Booting up LlmService and allocating ChatModel: {settings.model_name}")
        self.default_llm = init_chat_model(
            model=settings.model_name,
            temperature=0
        )
        
        tavily_tool = StructuredTool.from_function(
            func=tavily_service.search_news_from_web,
            name="search_news_from_web",
            description="Search for news from the web using Tavily API. Requires query, start_date, and end_date strings."
        )
        
        self.news_agent = create_agent(
            model=self.default_llm, 
            tools=[tavily_tool],
            checkpointer=db_service.get_checkpointer(),
            system_prompt="You are a news summarizer. Summarize the news for the user in podcast format. This podcast is hosted by Kartik",
        )
        logger.info("ChatModel and Agent instantiated globally.")
    
    def get_news(self, query: str, start_date: str, end_date: str):
        config = {"configurable": {"thread_id": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}}
        query = {"messages": [HumanMessage(content=f"Search news from web about \"{query}\" from start date : \"{start_date}\" to end date : \"{end_date}\"")]}        
        result = self.news_agent.invoke(query, config=config)
        logger.info(f"Final Agent Output for {query}: {result}")
        return result.get("messages")[-1].content
        
