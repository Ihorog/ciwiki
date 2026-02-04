# ПоДія (Podija) Module Documentation

## Overview

**ПоДія** is a calendar event management module that converts natural language input into structured calendar events. The module implements zero-hallucination intent extraction with strict JSON output.

## Technical Identifiers

- **UI Layer**: ПоДія (Cyrillic display name)
- **System Layer**: `podija` (technical identifier in code/API)
- **Data Layer**: `calendar.json` (storage file in `storage/shared/`)

## Architecture

### Priority Level

**Level 111 (Core Lobe #3)** - Critical system module

### Core Components

1. **Intent Extractor** (`core/podija.py`)
   - Natural language parsing
   - Date/time extraction
   - Zero-hallucination enforcement
   - Calendar storage management

2. **Voice Engine Integration** (`core/voice_engine.py`)
   - Event processing
   - Handler notification
   - Ontology-based classification

3. **Storage** (`storage/shared/calendar.json`)
   - Structured event storage
   - Unique ID generation (timestamp-based)
   - Metadata tracking

## Intent Extraction Algorithm

### System Prompt

```
Role: Podija Intent Extractor
Reference Date: [Dynamic: Current Date]
Output: Strict JSON ONLY

Fields:
- title: Event name (user's language)
- date: YYYY-MM-DD (calculated relative to current date)
- time: HH:MM (24-hour format)
- desc: Additional details or empty string

Constraints:
- FORBIDDEN: Return template text (e.g., YYYY-MM-DD)
- If date cannot be determined: use current date
- No personal names unless explicitly in user request
```

### Supported Date Patterns

- **Relative dates (Ukrainian)**:
  - `сьогодні` → today
  - `завтра` → tomorrow
  - `післязавтра` → day after tomorrow
  - `через тиждень` → in one week
  - `наступного тижня` → next week

- **Specific dates**:
  - `DD.MM` → day and month (current or next year)
  - `DD/MM` → day and month
  - `DD-MM` → day and month

### Time Patterns

- `о HH` → HH:00 (e.g., "о 10" → "10:00")
- `в HH:MM` → HH:MM (e.g., "в 14:30" → "14:30")
- `HH:MM` → HH:MM (direct format)
- Default: `09:00` if no time specified

## Usage Examples

### Basic Usage

```python
from core.podija import PodijaIntentExtractor

extractor = PodijaIntentExtractor()

# Extract intent
result = extractor.extract_intent("Завтра о 10 нарада")
# Output: {"title": "нарада", "date": "2026-02-05", "time": "10:00", "desc": ""}

# Save to calendar
event = extractor.save_event(result)
# Returns event with unique ID
```

### Voice Engine Integration

```python
from core.voice_engine import VoiceEngine

engine = VoiceEngine(ontology_path, manifest_path)

# Process natural language input
event = await engine.process_podija_intent("Завтра о 10 нарада")
# Automatically extracts, saves, and notifies handlers
```

## Zero-Hallucination Rules

The module enforces strict zero-hallucination constraints:

1. **No Invented Context**: Only extract information explicitly stated in user input
2. **No Personal Names**: Never add personal names unless in direct user input
3. **No Template Text**: Always return actual dates, never placeholder text
4. **Deterministic Parsing**: No fuzzy logic or AI-based guessing

## Storage Format

### calendar.json Structure

```json
{
  "events": [
    {
      "id": 1770228873246,
      "title": "нарада",
      "date": "2026-02-05",
      "time": "10:00",
      "desc": "",
      "created_at": "2026-02-04T18:14:33.246367",
      "status": "active"
    }
  ],
  "metadata": {
    "version": "1.0",
    "last_updated": "2026-02-04T18:14:33.246367"
  }
}
```

## Ontology Integration

Event type: `podija_event_created`
- Level: 111 (Critical)
- Emoji: 🔴
- Template: `📅 ПоДія: {title} ({date} о {time})`

## Testing

Run the comprehensive test suite:

```bash
python3 test_podija.py
```

Test coverage includes:
- Acceptance criteria validation
- Zero-hallucination enforcement
- Date calculation accuracy
- Time extraction in 24-hour format
- Storage sync and unique ID generation
- Voice Engine integration

## Security Considerations

1. **No Hardcoded Secrets**: No API keys or credentials in code
2. **Input Validation**: All user inputs validated before processing
3. **Path Safety**: File paths validated and contained
4. **No Code Execution**: Pure data processing, no eval() or exec()

## API Reference

### PodijaIntentExtractor

#### `__init__(calendar_path: Optional[str] = None)`
Initialize the intent extractor with optional custom calendar path.

#### `extract_intent(user_input: str) -> Dict[str, Any]`
Extract structured event data from natural language input.

**Returns**: `{"title": str, "date": str, "time": str, "desc": str}`

#### `save_event(event: Dict[str, Any]) -> Dict[str, Any]`
Save event to calendar.json with unique ID and metadata.

**Returns**: Complete event object with ID and timestamps

#### `get_events(date_filter: Optional[str] = None) -> list`
Retrieve events from calendar, optionally filtered by date.

## Acceptance Criteria Status

✅ **AC1**: Input "Завтра о 10 нарада" returns clean JSON with correct date  
✅ **AC2**: UI displays "ПоДія" in title  
✅ **AC3**: No hardcoded personal names in system prompts

## Future Enhancements

Potential improvements (not in current scope):
- Description extraction from extended input
- Recurring events support
- Event modification/deletion API
- PWA interface for event management
- Telegram bot integration for event notifications
