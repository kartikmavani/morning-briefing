import logging
import argparse
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

from core.ApplicationContainer import ApplicationContainer

def init_container():
    """ Bootstraps the DI container exactly once for the script lifecycle. """
    app_container = ApplicationContainer()

    return app_container

# Bootstrap the IoC container natively
container = init_container()


def main():
    logger.info("🌅 Morning Briefing AI Initializing...")

    today_str = datetime.now().strftime("%Y-%m-%d")
    yesterday_str = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    
    parser = argparse.ArgumentParser(description="Fetch personalized news.")
    parser.add_argument(
        "--interests", 
        type=str, 
        default="Artificial Intelligence, Gold and Silver, War, Australia, Victoria",
        help="Comma separated list of topics"
    )
    args = parser.parse_args()
    interest_list = args.interests.split(",")
    llm_service = container.llm_service()
    for interest in interest_list:
        clean_interest = interest.strip()
        logger.info(f"Fetching news for topic: {clean_interest}")
        try:            
            result = llm_service.get_news(clean_interest, yesterday_str, today_str)
            logger.info(f"Final Agent Output for {clean_interest}: {result}")
            
            # Now, pipe the LLM text directly to MacOS TTS!
            audio_service = container.audio_service()
            audio_path = f"output/{clean_interest.replace(' ', '_').lower()}_briefing.aiff"
            audio_service.generate_podcast(result, output_path=audio_path)
            
        except Exception as e:
            logger.error(f"Failed to fetch news for topic {clean_interest}: {e}")
    

if __name__ == "__main__":
    main()