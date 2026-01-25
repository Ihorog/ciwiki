"""
CIT Voice - Головний запускач системи сенсорних сповіщень
Інтегрує VoiceEngine та TelegramNotifier
"""

import os
import sys
import asyncio
import logging
from pathlib import Path
from dotenv import load_dotenv

# Додати поточну директорію до шляху
sys.path.insert(0, str(Path(__file__).parent))

from core.voice_engine import VoiceEngine
from integrations.telegram_bot import TelegramNotifier

# Завантаження конфігурації
load_dotenv()

# Налаштування логування
log_level = os.getenv('LOG_LEVEL', 'INFO')
logging.basicConfig(
    level=getattr(logging, log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def main():
    """Головна функція запуску CIT Voice"""
    
    # Перевірка обов'язкових параметрів
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    
    if not bot_token or not chat_id:
        logger.error("TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID must be set in .env file")
        logger.error("Copy .env.example to .env and fill in the values")
        sys.exit(1)
    
    # Шляхи до файлів
    base_path = Path(__file__).parent
    ontology_path = base_path / "core" / "ontology.json"
    manifest_path = base_path / "public" / "manifest.json"
    
    # Перевірка існування файлів
    if not ontology_path.exists():
        logger.error(f"Ontology file not found: {ontology_path}")
        sys.exit(1)
    
    if not manifest_path.exists():
        logger.warning(f"Manifest file not found: {manifest_path}")
        logger.warning("Continuing without manifest monitoring...")
    
    # Ініціалізація компонентів
    logger.info("Initializing CIT Voice components...")
    
    # Voice Engine
    api_endpoint = os.getenv('API_STATE_ENDPOINT', 'http://localhost:3000/api/state-visual')
    engine = VoiceEngine(
        ontology_path=str(ontology_path),
        manifest_path=str(manifest_path),
        api_endpoint=api_endpoint
    )
    
    # Telegram Notifier
    media_repo_url = os.getenv('MEDIA_REPO_URL', 'https://raw.githubusercontent.com/Ihorog/media/main')
    notifier = TelegramNotifier(
        bot_token=bot_token,
        chat_id=chat_id,
        media_repo_url=media_repo_url
    )
    
    # Реєстрація Telegram як обробника подій
    engine.register_handler(notifier)
    
    # Запуск обох систем паралельно
    logger.info("Starting CIT Voice system...")
    
    try:
        await asyncio.gather(
            engine.start(),
            notifier.start()
        )
    except KeyboardInterrupt:
        logger.info("Shutdown requested...")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
    finally:
        engine.stop()
        await notifier.stop()
        logger.info("CIT Voice shutdown complete")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nShutdown complete")
