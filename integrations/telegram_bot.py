"""
CIT Telegram Bot - Автономний канал сповіщень
Інтеграція з Telegram для надсилання сенсорних повідомлень
"""

import os
import logging
from typing import Dict, Any, Optional
from pathlib import Path
import httpx
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import (
    Message, 
    InlineKeyboardMarkup, 
    InlineKeyboardButton,
    CallbackQuery,
    FSInputFile
)
from aiogram.filters import Command
from aiogram.enums import ParseMode

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TelegramNotifier:
    """Telegram інтеграція для CIT Voice"""
    
    def __init__(self, bot_token: str, chat_id: str, media_repo_url: Optional[str] = None):
        self.bot = Bot(token=bot_token)
        self.dp = Dispatcher()
        self.router = Router()
        self.chat_id = chat_id
        self.media_repo_url = media_repo_url or "https://raw.githubusercontent.com/Ihorog/media/main"
        
        # Реєстрація обробників
        self._setup_handlers()
        self.dp.include_router(self.router)
    
    def _setup_handlers(self):
        """Налаштування обробників команд та callback"""
        
        @self.router.message(Command("start"))
        async def cmd_start(message: Message):
            await message.answer(
                "🤖 CIT Voice активовано.\n"
                "Сенсорні сповіщення про стан системи будуть надходити сюди.\n\n"
                "Щільність 111. Факти та можливості."
            )
        
        @self.router.message(Command("status"))
        async def cmd_status(message: Message):
            await message.answer(
                "✅ Система активна\n"
                "📊 Моніторинг: manifest.json, api/state-visual\n"
                "🔔 Рівні сповіщень: 1 (Фон), 11 (Дія), 111 (Критично)"
            )
        
        @self.router.callback_query(F.data.startswith("accept_"))
        async def callback_accept(callback: CallbackQuery):
            intent_id = callback.data.replace("accept_", "")
            await callback.answer()
            await callback.message.edit_text(
                f"{callback.message.text}\n\n✅ ПРИЙНЯТО. Активація...",
                reply_markup=None
            )
            logger.info(f"Intent {intent_id} accepted by user")
        
        @self.router.callback_query(F.data.startswith("reject_"))
        async def callback_reject(callback: CallbackQuery):
            intent_id = callback.data.replace("reject_", "")
            await callback.answer()
            await callback.message.edit_text(
                f"{callback.message.text}\n\n❌ ВІДХИЛЕНО.",
                reply_markup=None
            )
            logger.info(f"Intent {intent_id} rejected by user")
    
    async def handle_event(self, event: Dict[str, Any]):
        """
        Обробка події від VoiceEngine
        Форматування та відправка повідомлення в Telegram
        """
        level = event['level']
        emoji = event['emoji']
        event_type = event['event_type']
        template = event['template']
        data = event.get('data', {})
        
        # Форматування повідомлення
        message_text = self._format_message(level, emoji, template, data)
        
        # Визначення, чи потрібні медіа та інтерактивність
        requires_media = event.get('requires_media', False)
        interactive = event.get('interactive', False)
        
        try:
            # Рівень 1 (Фон) - просте повідомлення
            if level == '1':
                await self.bot.send_message(
                    chat_id=self.chat_id,
                    text=message_text,
                    parse_mode=ParseMode.HTML
                )
            
            # Рівень 11 (Дія) - з медіа та кнопками
            elif level == '11':
                keyboard = None
                if interactive:
                    keyboard = self._create_action_keyboard(event_type)
                
                if requires_media:
                    media_path = await self._get_media_for_event(event_type)
                    if media_path:
                        await self.bot.send_photo(
                            chat_id=self.chat_id,
                            photo=FSInputFile(media_path),
                            caption=message_text,
                            parse_mode=ParseMode.HTML,
                            reply_markup=keyboard
                        )
                    else:
                        await self.bot.send_message(
                            chat_id=self.chat_id,
                            text=message_text,
                            parse_mode=ParseMode.HTML,
                            reply_markup=keyboard
                        )
                else:
                    await self.bot.send_message(
                        chat_id=self.chat_id,
                        text=message_text,
                        parse_mode=ParseMode.HTML,
                        reply_markup=keyboard
                    )
            
            # Рівень 111 (Критично) - з медіа
            elif level == '111':
                if requires_media:
                    media_path = await self._get_media_for_event(event_type)
                    if media_path:
                        await self.bot.send_photo(
                            chat_id=self.chat_id,
                            photo=FSInputFile(media_path),
                            caption=message_text,
                            parse_mode=ParseMode.HTML
                        )
                    else:
                        await self.bot.send_message(
                            chat_id=self.chat_id,
                            text=message_text,
                            parse_mode=ParseMode.HTML
                        )
                else:
                    await self.bot.send_message(
                        chat_id=self.chat_id,
                        text=message_text,
                        parse_mode=ParseMode.HTML
                    )
            
            logger.info(f"Message sent successfully: level={level}, type={event_type}")
            
        except Exception as e:
            logger.error(f"Failed to send message: {e}")
    
    def _format_message(self, level: str, emoji: str, template: str, data: Dict[str, Any]) -> str:
        """
        Форматування повідомлення згідно з шаблоном
        Стиль: Максимальна щільність 111. Жодної ввічливості.
        """
        # Базовий заголовок
        header = f"{emoji} <b>[{level}]</b>"
        
        # Рівень деталізації
        if level == '1':
            level_name = "(Фон)"
        elif level == '11':
            level_name = "(Дія)"
        elif level == '111':
            level_name = "(Критично)"
        else:
            level_name = ""
        
        # Заповнення шаблону даними
        try:
            formatted_template = template.format(**data)
        except KeyError:
            formatted_template = template
        
        # Фінальне повідомлення
        message = f"{header} {level_name}: {formatted_template}"
        
        return message
    
    def _create_action_keyboard(self, event_type: str) -> InlineKeyboardMarkup:
        """
        Створення інтерактивної клавіатури для режиму "Чарівна пропозиція"
        """
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ ПРИЙНЯТИ ВОЛЮ",
                    callback_data=f"accept_{event_type}"
                ),
                InlineKeyboardButton(
                    text="❌ ВІДХИЛИТИ",
                    callback_data=f"reject_{event_type}"
                )
            ]
        ])
        return keyboard
    
    async def _get_media_for_event(self, event_type: str) -> Optional[str]:
        """
        Отримання медіа активу для події з репозиторію media
        Повертає шлях до локально збереженого файлу
        """
        # Мапінг типів подій на медіа файли
        media_map = {
            'module_proposal': 'icons/action.png',
            'structural_gap': 'icons/critical.png',
            'intent_detected': 'icons/intent.png'
        }
        
        media_file = media_map.get(event_type)
        if not media_file:
            return None
        
        # Шлях для кешування медіа локально
        cache_dir = Path('/tmp/cit_media_cache')
        cache_dir.mkdir(exist_ok=True)
        local_path = cache_dir / Path(media_file).name
        
        # Якщо файл вже кешований, повернути його
        if local_path.exists():
            return str(local_path)
        
        # Завантажити з репозиторію
        try:
            url = f"{self.media_repo_url}/{media_file}"
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=10.0)
                if response.status_code == 200:
                    with open(local_path, 'wb') as f:
                        f.write(response.content)
                    logger.info(f"Downloaded media: {media_file}")
                    return str(local_path)
        except Exception as e:
            logger.warning(f"Failed to download media {media_file}: {e}")
        
        return None
    
    async def start(self):
        """Запуск Telegram бота"""
        logger.info("Starting Telegram bot...")
        await self.dp.start_polling(self.bot)
    
    async def stop(self):
        """Зупинка Telegram бота"""
        await self.bot.session.close()
        logger.info("Telegram bot stopped")


# Точка входу для тестування
if __name__ == "__main__":
    import asyncio
    from dotenv import load_dotenv
    
    load_dotenv()
    
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    
    if not bot_token or not chat_id:
        logger.error("TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID must be set in .env")
        exit(1)
    
    notifier = TelegramNotifier(bot_token, chat_id)
    
    try:
        asyncio.run(notifier.start())
    except KeyboardInterrupt:
        logger.info("Shutdown complete")
