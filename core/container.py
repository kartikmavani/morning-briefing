# core/container.py
from dependency_injector import containers, providers

from service.LlmService import LlmService
from service.DatabaseService import DatabaseService
from service.TaviliyService import TavilyService
from service.AudioService import AudioService
from config.settings import AppSettings

class ApplicationContainer(containers.DeclarativeContainer):
    """ Central IoC Container holding all singletons """
    
    # 1. Register AppSettings
    settings = providers.Singleton(AppSettings)
    
    # 2. Register DatabaseService, injecting settings
    db_service = providers.Singleton(
        DatabaseService,
        settings=settings
    )
    
    # 3. New Tool Service injected with settings
    tavily_service = providers.Singleton(
        TavilyService,
        settings=settings
    )
    
    # 4. Inject settings, db_service, AND tavily_service as required by LlmService.__init__
    llm_service = providers.Singleton(
        LlmService,
        db_service=db_service,
        tavily_service=tavily_service,
        settings=settings
    )

    # 5. Global zero-dependency Audio Service
    audio_service = providers.Singleton(AudioService)

