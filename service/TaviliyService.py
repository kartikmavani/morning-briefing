import logging
from tavily import TavilyClient
from langchain.tools import tool
from config.settings import AppSettings

logger = logging.getLogger(__name__)

class TavilyService:
    def __init__(self, settings: AppSettings):
        self.client = TavilyClient(settings.tavily_api_key)

    def search_news_from_web(self, query: str, start_date: str, end_date: str):
        """
        Search for news from the web using Tavily API.
        
        Args:
            query (str): The search query.
            start_date (str): The start date for the search (YYYY-MM-DD).
            end_date (str): The end date for the search (YYYY-MM-DD).
        
        Returns:
            dict: The search results.
        """
        logger.info(f"Searching for news about {query} from {start_date} to {end_date}")
        return self.client.search(
            query=query,
            topic="news",
            search_depth="advanced",
            start_date=start_date,
            end_date=end_date
        )
