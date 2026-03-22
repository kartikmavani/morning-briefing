import logging
from langgraph.checkpoint.postgres import PostgresSaver
from psycopg_pool import ConnectionPool
from config.AppSettings import AppSettings

logger = logging.getLogger(__name__)

class DatabaseService:
    """
    Manages global database connections across the application.
    """
    def __init__(self, settings: AppSettings):
        logger.info(f"Initializing Postgres DB connection pool (Min: {settings.db_pool_min_size}, Max: {settings.db_pool_max_size})...")
        
        # We now use the injected Pydantic settings object!
        # No more manual os.getenv() fetching anywhere.
        self.pool = ConnectionPool(
            conninfo=settings.database_url, 
            min_size=settings.db_pool_min_size,
            max_size=settings.db_pool_max_size,
            kwargs={"autocommit": True}
        )
        
        # Initialize the LangGraph Postgres checkpointer globally
        self.checkpointer = PostgresSaver(self.pool)
        
        # Automatically creates the 'checkpoints' and 'writes' tables if they don't exist
        self.checkpointer.setup()
        logger.info("LangGraph Postgres Saver created successfully.")
        
    def get_checkpointer(self) -> PostgresSaver:
        return self.checkpointer

    def close(self):
        self.pool.close()
