"""
ПоДія (Podija) - Intent Extractor for Calendar Events
Converts natural language to structured JSON for calendar events

Technical Specification:
- UI: ПоДія (Cyrillic)
- System: podija (technical identifier)
- Data: calendar.json (storage)

Core Rules:
- Zero-Hallucination: No invented context or personal names
- Strict JSON output only
- Date calculations relative to current date
- No template text in output (e.g., YYYY-MM-DD)
"""

import json
import logging
import os
import re
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class PodijaIntentExtractor:
    """
    Podija Intent Extractor - Converts natural language to calendar events
    
    System Prompt:
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
    """
    
    def __init__(self, calendar_path: Optional[str] = None):
        """
        Initialize Podija Intent Extractor
        
        Args:
            calendar_path: Path to calendar.json storage file
        """
        if calendar_path is None:
            base_path = Path(__file__).parent.parent
            calendar_path = base_path / "storage" / "shared" / "calendar.json"
        
        self.calendar_path = Path(calendar_path)
        self._ensure_storage()
    
    def _ensure_storage(self):
        """Ensure storage directory and file exist"""
        self.calendar_path.parent.mkdir(parents=True, exist_ok=True)
        
        if not self.calendar_path.exists():
            initial_data = {
                "events": [],
                "metadata": {
                    "version": "1.0",
                    "last_updated": None
                }
            }
            with open(self.calendar_path, 'w', encoding='utf-8') as f:
                json.dump(initial_data, f, ensure_ascii=False, indent=2)
            logger.info(f"Created calendar storage: {self.calendar_path}")
    
    def extract_intent(self, user_input: str) -> Dict[str, Any]:
        """
        Extract event intent from natural language
        
        Args:
            user_input: Natural language input from user
            
        Returns:
            Dict with fields: title, date, time, desc
            
        Examples:
            "Завтра о 10 нарада" -> {
                "title": "нарада",
                "date": "2026-02-05",
                "time": "10:00",
                "desc": ""
            }
        """
        current_date = datetime.now()
        
        # Parse the input for temporal markers and event details
        parsed = self._parse_natural_language(user_input, current_date)
        
        return {
            "title": parsed["title"],
            "date": parsed["date"],
            "time": parsed["time"],
            "desc": parsed["desc"]
        }
    
    def _parse_natural_language(self, text: str, reference_date: datetime) -> Dict[str, Any]:
        """
        Parse natural language to extract event components
        
        This is a deterministic parser - no fuzzy logic, no hallucination.
        """
        text_lower = text.lower()
        
        # Extract date
        event_date = self._extract_date(text_lower, reference_date)
        
        # Extract time
        event_time = self._extract_time(text_lower)
        
        # Extract title (remove date/time markers)
        title = self._extract_title(text, text_lower)
        
        # Extract description (optional additional context)
        desc = self._extract_description(text, text_lower)
        
        return {
            "title": title,
            "date": event_date.strftime("%Y-%m-%d"),
            "time": event_time,
            "desc": desc
        }
    
    def _extract_date(self, text: str, reference_date: datetime) -> datetime:
        """Extract and calculate date from text"""
        # Relative date markers (Ukrainian)
        # Check longer patterns first to avoid partial matches
        if "післязавтра" in text or "після завтра" in text:
            return reference_date + timedelta(days=2)
        elif "завтра" in text:
            return reference_date + timedelta(days=1)
        elif "сьогодні" in text or "сьогодн" in text:
            return reference_date
        elif "через тиждень" in text:
            return reference_date + timedelta(days=7)
        elif "наступного тижня" in text or "наст тижня" in text:
            # Find next Monday
            days_ahead = 7 - reference_date.weekday()
            if days_ahead <= 0:
                days_ahead += 7
            return reference_date + timedelta(days=days_ahead)
        
        # Try to find specific date patterns (DD.MM, DD/MM, DD-MM)
        date_pattern = r'(\d{1,2})[\.\-/](\d{1,2})'
        match = re.search(date_pattern, text)
        if match:
            day = int(match.group(1))
            month = int(match.group(2))
            year = reference_date.year
            
            # If the date has passed this year, assume next year
            try:
                parsed_date = datetime(year, month, day)
                if parsed_date < reference_date:
                    parsed_date = datetime(year + 1, month, day)
                return parsed_date
            except ValueError:
                # Invalid date, use current date
                logger.warning(f"Invalid date parsed: {day}.{month}")
                return reference_date
        
        # Default: use current date if no date marker found
        return reference_date
    
    def _extract_time(self, text: str) -> str:
        """Extract time from text"""
        
        # Pattern for time: "о 10", "в 14:30", "о 9:00", "14:30"
        time_patterns = [
            r'[ов]\s*(\d{1,2}):(\d{2})',  # "о 10:30", "в 14:30"
            r'[ов]\s*(\d{1,2})\s*(?:год|час)',  # "о 10 год", "в 14 час"
            r'[ов]\s*(\d{1,2})(?:\s|$)',  # "о 10 ", "в 14"
            r'(\d{1,2}):(\d{2})',  # "14:30"
        ]
        
        for pattern in time_patterns:
            match = re.search(pattern, text)
            if match:
                hour = int(match.group(1))
                minute = int(match.group(2)) if len(match.groups()) > 1 else 0
                
                # Validate time
                if 0 <= hour < 24 and 0 <= minute < 60:
                    return f"{hour:02d}:{minute:02d}"
        
        # Default: 09:00 if no time specified
        return "09:00"
    
    def _extract_title(self, original_text: str, text_lower: str) -> str:
        """Extract event title from text"""
        # Remove date/time markers to get clean title
        # Order matters: check longer patterns first to avoid partial matches
        markers_to_remove = [
            r'післязавтра\s*',
            r'після\s+завтра\s*',
            r'наступного\s+тижня\s*',
            r'через\s+тиждень\s*',
            r'завтра\s*',
            r'сьогодні\s*',
            r'[ов]\s*\d{1,2}(?::\d{2})?\s*(?:год|час)?\s*',
            r'\d{1,2}:\d{2}\s*',
            r'\d{1,2}[\.\-/]\d{1,2}[\.\-/]?\d*\s*',
        ]
        
        title = original_text.strip()
        
        for marker in markers_to_remove:
            title = re.sub(marker, '', title, flags=re.IGNORECASE)
        
        # Clean up extra whitespace
        title = ' '.join(title.split())
        
        return title if title else "Подія"
    
    def _extract_description(self, original_text: str, text_lower: str) -> str:
        """Extract additional description if present"""
        # Look for description markers
        # For now, return empty - can be extended based on patterns
        return ""
    
    def save_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """
        Save event to calendar.json with unique ID
        
        Args:
            event: Event data with title, date, time, desc
            
        Returns:
            Saved event with added id and metadata
        """
        # Generate unique ID using timestamp with microseconds
        event_id = int(time.time() * 1000000)  # Use microseconds for better uniqueness
        
        # Create full event object
        full_event = {
            "id": event_id,
            "title": event["title"],
            "date": event["date"],
            "time": event["time"],
            "desc": event["desc"],
            "created_at": datetime.now().isoformat(),
            "status": "active"
        }
        
        # Load current calendar
        with open(self.calendar_path, 'r', encoding='utf-8') as f:
            calendar_data = json.load(f)
        
        # Add event
        calendar_data["events"].append(full_event)
        calendar_data["metadata"]["last_updated"] = datetime.now().isoformat()
        
        # Save back to file
        with open(self.calendar_path, 'w', encoding='utf-8') as f:
            json.dump(calendar_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Saved event: {full_event['title']} on {full_event['date']} at {full_event['time']}")
        
        return full_event
    
    def get_events(self, date_filter: Optional[str] = None) -> list:
        """
        Get events from calendar
        
        Args:
            date_filter: Optional date filter in YYYY-MM-DD format
            
        Returns:
            List of events
        """
        with open(self.calendar_path, 'r', encoding='utf-8') as f:
            calendar_data = json.load(f)
        
        events = calendar_data.get("events", [])
        
        if date_filter:
            events = [e for e in events if e["date"] == date_filter]
        
        return events


# Convenience function for quick intent extraction
def extract_event_intent(user_input: str, calendar_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Quick function to extract intent from natural language
    
    Args:
        user_input: Natural language input
        calendar_path: Optional path to calendar.json
        
    Returns:
        Event data dict with title, date, time, desc
    """
    extractor = PodijaIntentExtractor(calendar_path)
    return extractor.extract_intent(user_input)


# Example usage
if __name__ == "__main__":
    # Test cases
    test_inputs = [
        "Завтра о 10 нарада",
        "Сьогодні в 14:30 зустріч з командою",
        "15.02 о 16 презентація проекту",
        "Через тиждень дзвінок",
    ]
    
    extractor = PodijaIntentExtractor()
    
    print("🗓️  ПоДія Intent Extractor - Test Cases\n")
    print(f"Reference Date: {datetime.now().strftime('%Y-%m-%d')}\n")
    
    for test_input in test_inputs:
        print(f"Input: {test_input}")
        result = extractor.extract_intent(test_input)
        print(f"Output: {json.dumps(result, ensure_ascii=False, indent=2)}")
        print()
