"""
Тестовий скрипт для CIT Voice
Симулює різні типи подій без реального запуску системи
"""

import asyncio
import sys
import traceback
from pathlib import Path

# Додати поточну директорію до шляху
sys.path.insert(0, str(Path(__file__).parent))

from core.voice_engine import VoiceEngine


class MockTelegramHandler:
    """Mock обробник для тестування без реального Telegram"""
    
    async def handle_event(self, event):
        print("\n" + "="*60)
        print(f"📢 MOCK TELEGRAM MESSAGE")
        print("="*60)
        print(f"Level: {event['level']} {event['emoji']}")
        print(f"Priority: {event['priority']}")
        print(f"Event Type: {event['event_type']}")
        print(f"Template: {event['template']}")
        print(f"Requires Media: {event.get('requires_media', False)}")
        print(f"Interactive: {event.get('interactive', False)}")
        print(f"Timestamp: {event['timestamp']}")
        print(f"Data: {event['data']}")
        print("="*60 + "\n")


async def test_events():
    """Тестування різних типів подій"""
    
    # Ініціалізація Voice Engine
    base_path = Path(__file__).parent
    ontology_path = base_path / "core" / "ontology.json"
    manifest_path = base_path / "public" / "manifest.json"
    
    engine = VoiceEngine(
        ontology_path=str(ontology_path),
        manifest_path=str(manifest_path)
    )
    
    # Реєстрація mock обробника
    mock_handler = MockTelegramHandler()
    engine.register_handler(mock_handler)
    
    print("\n🚀 Starting CIT Voice Test Suite\n")
    
    # Тест 1: Рівень 1 (Фон) - Knowledge Synthesis
    print("Test 1: Background Knowledge Synthesis Event")
    await engine.process_event({
        'type': 'knowledge_synthesis',
        'source': 'test',
        'description': 'Організм проводить фоновий синтез знань...'
    })
    await asyncio.sleep(1)
    
    # Тест 2: Рівень 1 (Фон) - State Change
    print("Test 2: Background State Change Event")
    await engine.process_event({
        'type': 'state_change',
        'source': 'manifest',
        'state_description': 'Manifest updated with new modules'
    })
    await asyncio.sleep(1)
    
    # Тест 3: Рівень 11 (Дія) - Module Proposal
    print("Test 3: Action Level - Module Proposal")
    await engine.emit_intent_event({
        'description': 'Виявлено необхідність оптимізації процесу синтезу',
        'action': 'Активувати модуль автоматичної оптимізації',
        'module': 'AutoOptimizer',
        'goal': 'швидкість синтезу на 40%'
    })
    await asyncio.sleep(1)
    
    # Тест 4: Рівень 11 (Дія) - Intent Detected (з кнопками)
    print("Test 4: Action Level - Intent Detection with Buttons")
    test_event = {
        'type': 'module_proposal',
        'source': 'intent_observer',
        'module_name': 'SecurityAuditor',
        'goal': 'захист системи'
    }
    await engine.process_event(test_event)
    await asyncio.sleep(1)
    
    # Тест 5: Рівень 111 (Критично) - Structural Gap
    print("Test 5: Critical Level - Structural Gap")
    await engine.process_event({
        'type': 'structural_gap',
        'source': 'error_detector',
        'description': 'Виявлено структурну прогалину в модулі безпеки'
    })
    await asyncio.sleep(1)
    
    print("\n✅ All tests completed!\n")


async def test_classification():
    """Тестування класифікації подій"""
    
    base_path = Path(__file__).parent
    ontology_path = base_path / "core" / "ontology.json"
    manifest_path = base_path / "public" / "manifest.json"
    
    engine = VoiceEngine(
        ontology_path=str(ontology_path),
        manifest_path=str(manifest_path)
    )
    
    print("\n🔍 Testing Event Classification\n")
    
    test_cases = [
        {'type': 'knowledge_synthesis'},
        {'type': 'module_proposal', 'module_name': 'TestModule'},
        {'type': 'structural_gap'},
        {'type': 'intent_detected'},
        {'type': 'state_change'},
        {'type': 'unknown_type'}  # Should default to level 1
    ]
    
    for test_case in test_cases:
        result = engine.classify_event(test_case)
        print(f"Event: {test_case.get('type', 'unknown')}")
        print(f"  → Level: {result['level']} {result['emoji']}")
        print(f"  → Priority: {result['priority']}")
        print(f"  → Media: {result['requires_media']}")
        print(f"  → Interactive: {result['interactive']}")
        print()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='CIT Voice Test Suite')
    parser.add_argument(
        '--mode',
        choices=['events', 'classification', 'all'],
        default='all',
        help='Test mode to run'
    )
    
    args = parser.parse_args()
    
    try:
        if args.mode == 'events' or args.mode == 'all':
            asyncio.run(test_events())
        
        if args.mode == 'classification' or args.mode == 'all':
            asyncio.run(test_classification())
            
    except KeyboardInterrupt:
        print("\n\n⛔ Tests interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Test failed with error: {e}")
        traceback.print_exc()
