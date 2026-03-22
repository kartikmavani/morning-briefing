from pydantic_settings import BaseSettings, SettingsConfigDict

class AppSettings(BaseSettings):
    """ Automatically maps variables from .env to strongly typed properties """
    database_url: str = "postgresql://user:password@localhost:5432/morning_briefing"
    db_pool_min_size: int = 1
    db_pool_max_size: int = 20
    model_name: str = "ollama:qwen3:8b"
    tavily_api_key: str = "tvly-your-key-here" # Added for TaviliyService

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore"
    )
