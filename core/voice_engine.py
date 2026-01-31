"""
CIT Voice Engine - Central Event Processor
Слухає зміни станів у manifest.json та api/state-visual
Надає семантичне забарвлення подій згідно з ontology.json
"""

import json
import asyncio
import logging
import hashlib
import time
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import httpx

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class VoiceEngine:
    """Центральний обробник подій для CIT Voice"""
    
    def __init__(self, ontology_path: str, manifest_path: str, api_endpoint: Optional[str] = None):
        self.ontology_path = Path(ontology_path)
        self.manifest_path = Path(manifest_path)
        self.api_endpoint = api_endpoint or "http://localhost:3000/api/state-visual"
        self.ontology = self._load_ontology()
        self.event_handlers: List = []
        self.observer = None
        self.manifest_handler = None
        
    def _load_ontology(self) -> Dict[str, Any]:
        """Завантаження семантичної онтології"""
        try:
            with open(self.ontology_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load ontology: {e}")
            return {}
    
    def register_handler(self, handler):
        """Реєстрація обробника подій (наприклад, Telegram bot)"""
        self.event_handlers.append(handler)
        logger.info(f"Registered event handler: {handler.__class__.__name__}")
    
    def classify_event(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Класифікація події згідно з онтологією
        Повертає структуру з рівнем, шаблоном та додатковою інформацією
        """
        event_type = event_data.get('type', 'state_change')
        
        # Отримати тип події з онтології
        event_config = self.ontology.get('event_types', {}).get(event_type, {})
        level = event_config.get('level', '1')
        level_config = self.ontology.get('event_levels', {}).get(level, {})
        
        return {
            'level': level,
            'emoji': level_config.get('emoji', '⚪'),
            'priority': level_config.get('priority', 'background'),
            'template': event_config.get('template', ''),
            'requires_media': event_config.get('requires_media', False),
            'interactive': event_config.get('interactive', False),
            'event_type': event_type,
            'timestamp': datetime.now().isoformat(),
            'data': event_data
        }
    
    async def process_event(self, event_data: Dict[str, Any]):
        """Обробка події та розсилка по всіх обробниках"""
        classified_event = self.classify_event(event_data)
        
        logger.info(f"Processing event: level={classified_event['level']}, "
                   f"type={classified_event['event_type']}")
        
        # Паралельна відправка подій всім зареєстрованим обробникам
        tasks = []
        for handler in self.event_handlers:
            task = asyncio.create_task(self._safe_handle_event(handler, classified_event))
            tasks.append(task)
        
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
    
    async def _safe_handle_event(self, handler, event):
        """Безпечний виклик обробника з обробкою помилок"""
        try:
            await handler.handle_event(event)
        except Exception as e:
            logger.error(f"Handler {handler.__class__.__name__} failed: {e}")
    
    async def watch_manifest(self):
        """Моніторинг змін у manifest.json"""
        class ManifestHandler(FileSystemEventHandler):
            def __init__(self, voice_engine):
                self.voice_engine = voice_engine
                self.pending_tasks = set()
                self.last_modified = 0
                self.debounce_delay = 1.0  # секунди
                
            def on_modified(self, event):
                if event.src_path.endswith('manifest.json'):
                    # Debouncing: ignore repeated events within 1 second
                    current_time = time.time()
                    if current_time - self.last_modified < self.debounce_delay:
                        return
                    self.last_modified = current_time
                    
                    logger.info("Manifest.json changed")
                    event_data = {
                        'type': 'knowledge_synthesis',
                        'source': 'manifest',
                        'description': 'Організм проводить фоновий синтез знань...'
                    }
                    # Створити task та зберегти посилання
                    task = asyncio.create_task(self.voice_engine.process_event(event_data))
                    self.pending_tasks.add(task)
                    task.add_done_callback(self.pending_tasks.discard)
            
            async def cleanup(self):
                """Очистка незавершених задач"""
                if self.pending_tasks:
                    await asyncio.gather(*self.pending_tasks, return_exceptions=True)
                    self.pending_tasks.clear()
        
        self.observer = Observer()
        self.manifest_handler = ManifestHandler(self)
        self.observer.schedule(self.manifest_handler, str(self.manifest_path.parent), recursive=False)
        self.observer.start()
        logger.info(f"Started watching manifest: {self.manifest_path}")
    
    async def poll_api_state(self, interval: int = 30):
        """Періодичний опитування API для змін стану"""
        async with httpx.AsyncClient() as client:
            previous_state_hash = None
            
            while True:
                try:
                    response = await client.get(self.api_endpoint, timeout=10.0)
                    if response.status_code == 200:
                        current_state = response.json()
                        
                        # Використання хешування для ефективного порівняння
                        current_state_json = json.dumps(current_state, sort_keys=True)
                        current_state_hash = hashlib.md5(current_state_json.encode()).hexdigest()
                        
                        # Порівняння зі попереднім станом через хеш
                        if previous_state_hash and previous_state_hash != current_state_hash:
                            event_data = {
                                'type': 'visual_state_change',
                                'source': 'api',
                                'previous': None,  # Не зберігаємо попередній стан для економії пам'яті
                                'current': current_state,
                                'description': f'Візуальний стан змінено'
                            }
                            await self.process_event(event_data)
                        
                        previous_state_hash = current_state_hash
                        
                except httpx.RequestError as e:
                    logger.warning(f"API request failed: {e}")
                except Exception as e:
                    logger.error(f"Error polling API: {e}")
                
                await asyncio.sleep(interval)
    
    async def emit_intent_event(self, intent_data: Dict[str, Any]):
        """
        Ручна генерація події наміру від IntentObserver
        Використовується для режиму "Чарівна пропозиція"
        """
        event_data = {
            'type': 'intent_detected',
            'source': 'intent_observer',
            'intent_description': intent_data.get('description', ''),
            'action_suggestion': intent_data.get('action', ''),
            'module_name': intent_data.get('module', ''),
            'goal': intent_data.get('goal', '')
        }
        await self.process_event(event_data)
    
    async def start(self):
        """Запуск голосового движка"""
        logger.info("Starting CIT Voice Engine...")
        
        # Запустити моніторинг manifest.json
        await self.watch_manifest()
        
        # Запустити опитування API
        tasks = [
            self.poll_api_state()
        ]
        
        await asyncio.gather(*tasks)
    
    def stop(self):
        """Зупинка голосового движка"""
        if self.observer:
            self.observer.stop()
            self.observer.join()
        # Очистка незавершених задач в manifest handler
        if self.manifest_handler:
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    asyncio.create_task(self.manifest_handler.cleanup())
                else:
                    loop.run_until_complete(self.manifest_handler.cleanup())
            except Exception as e:
                logger.error(f"Error cleaning up manifest handler: {e}")
        logger.info("CIT Voice Engine stopped")


# Точка входу для тестування
if __name__ == "__main__":
    import sys
    
    # Шляхи за замовчуванням
    ontology_path = sys.argv[1] if len(sys.argv) > 1 else "core/ontology.json"
    manifest_path = sys.argv[2] if len(sys.argv) > 2 else "public/manifest.json"
    
    engine = VoiceEngine(ontology_path, manifest_path)
    
    try:
        asyncio.run(engine.start())
    except KeyboardInterrupt:
        engine.stop()
        logger.info("Shutdown complete")
