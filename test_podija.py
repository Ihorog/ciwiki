"""
Test suite for ПоДія (Podija) Intent Extractor
Tests acceptance criteria from technical specification
"""

import asyncio
import json
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from core.podija import PodijaIntentExtractor
from core.voice_engine import VoiceEngine


def test_acceptance_criteria_1():
    """
    Acceptance Criteria 1:
    Input "Завтра о 10 нарада" should return clean JSON with correct date
    """
    print("\n" + "="*70)
    print("TEST 1: Acceptance Criteria - 'Завтра о 10 нарада'")
    print("="*70)
    
    extractor = PodijaIntentExtractor()
    
    # Get tomorrow's date
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    
    result = extractor.extract_intent("Завтра о 10 нарада")
    
    print(f"Input: 'Завтра о 10 нарада'")
    print(f"Output: {json.dumps(result, ensure_ascii=False, indent=2)}")
    
    # Validate result
    assert result["title"] == "нарада", f"Expected title 'нарада', got '{result['title']}'"
    assert result["date"] == tomorrow, f"Expected date {tomorrow}, got {result['date']}"
    assert result["time"] == "10:00", f"Expected time '10:00', got '{result['time']}'"
    assert result["desc"] == "", f"Expected empty desc, got '{result['desc']}'"
    
    # Verify no template text
    assert "YYYY" not in result["date"], "Found template text in date field"
    assert "MM" not in result["date"], "Found template text in date field"
    assert "DD" not in result["date"], "Found template text in date field"
    
    print("✅ Test PASSED: Clean JSON with correct date returned")
    return True


def test_no_hallucination():
    """
    Test Zero-Hallucination Rule:
    System should not add context or names not in user request
    """
    print("\n" + "="*70)
    print("TEST 2: Zero-Hallucination Rule")
    print("="*70)
    
    extractor = PodijaIntentExtractor()
    
    test_cases = [
        ("Завтра зустріч", ["зустріч"]),
        ("Сьогодні о 15 дзвінок", ["дзвінок"]),
        ("10.03 презентація", ["презентація"]),
    ]
    
    all_passed = True
    
    for user_input, expected_keywords in test_cases:
        result = extractor.extract_intent(user_input)
        print(f"\nInput: '{user_input}'")
        print(f"Output title: '{result['title']}'")
        
        # Check that title only contains expected keywords
        title_lower = result['title'].lower()
        contains_expected = any(kw in title_lower for kw in expected_keywords)
        
        if contains_expected:
            print(f"✅ Contains expected keyword: {expected_keywords}")
        else:
            print(f"❌ Does not contain expected keyword: {expected_keywords}")
            all_passed = False
        
        # Check that no hardcoded personal names are added
        # (This would need to be more sophisticated in real implementation)
        forbidden_words = ["сергій", "іван", "марія", "олена", "петро"]
        has_forbidden = any(word in title_lower for word in forbidden_words)
        
        if not has_forbidden:
            print(f"✅ No forbidden personal names added")
        else:
            print(f"❌ Found forbidden personal name in output")
            all_passed = False
    
    if all_passed:
        print("\n✅ Test PASSED: Zero-hallucination rule maintained")
    else:
        print("\n❌ Test FAILED: Hallucination detected")
    
    return all_passed


def test_date_calculations():
    """
    Test date calculation relative to current date
    """
    print("\n" + "="*70)
    print("TEST 3: Date Calculation - Relative Dates")
    print("="*70)
    
    extractor = PodijaIntentExtractor()
    today = datetime.now()
    
    test_cases = [
        ("Сьогодні зустріч", today),
        ("Завтра зустріч", today + timedelta(days=1)),
        ("Післязавтра зустріч", today + timedelta(days=2)),
    ]
    
    all_passed = True
    
    for user_input, expected_date in test_cases:
        result = extractor.extract_intent(user_input)
        expected_date_str = expected_date.strftime("%Y-%m-%d")
        
        print(f"\nInput: '{user_input}'")
        print(f"Expected date: {expected_date_str}")
        print(f"Output date: {result['date']}")
        
        if result['date'] == expected_date_str:
            print("✅ Date calculated correctly")
        else:
            print("❌ Date calculation error")
            all_passed = False
    
    if all_passed:
        print("\n✅ Test PASSED: All dates calculated correctly")
    else:
        print("\n❌ Test FAILED: Date calculation errors")
    
    return all_passed


def test_time_extraction():
    """
    Test time extraction in 24-hour format
    """
    print("\n" + "="*70)
    print("TEST 4: Time Extraction - 24-Hour Format")
    print("="*70)
    
    extractor = PodijaIntentExtractor()
    
    test_cases = [
        ("Завтра о 10 зустріч", "10:00"),
        ("Сьогодні в 14:30 нарада", "14:30"),
        ("15.02 о 16 презентація", "16:00"),
        ("Завтра 09:15 дзвінок", "09:15"),
    ]
    
    all_passed = True
    
    for user_input, expected_time in test_cases:
        result = extractor.extract_intent(user_input)
        
        print(f"\nInput: '{user_input}'")
        print(f"Expected time: {expected_time}")
        print(f"Output time: {result['time']}")
        
        if result['time'] == expected_time:
            print("✅ Time extracted correctly")
        else:
            print("❌ Time extraction error")
            all_passed = False
    
    if all_passed:
        print("\n✅ Test PASSED: All times extracted correctly")
    else:
        print("\n❌ Test FAILED: Time extraction errors")
    
    return all_passed


def test_storage_sync():
    """
    Test that events are saved to calendar.json with unique IDs
    """
    print("\n" + "="*70)
    print("TEST 5: Storage Sync - calendar.json")
    print("="*70)
    
    # Use temporary calendar for testing
    import tempfile
    import os
    
    with tempfile.TemporaryDirectory() as tmpdir:
        calendar_path = os.path.join(tmpdir, "calendar.json")
        extractor = PodijaIntentExtractor(calendar_path)
        
        # Extract and save event
        event_data = extractor.extract_intent("Завтра о 10 нарада")
        saved_event = extractor.save_event(event_data)
        
        print(f"\nEvent saved with ID: {saved_event['id']}")
        print(f"Event data: {json.dumps(saved_event, ensure_ascii=False, indent=2)}")
        
        # Verify file exists
        assert Path(calendar_path).exists(), "calendar.json not created"
        print("✅ calendar.json file created")
        
        # Verify event in storage
        events = extractor.get_events()
        assert len(events) == 1, f"Expected 1 event, got {len(events)}"
        assert events[0]['id'] == saved_event['id'], "Event ID mismatch"
        print(f"✅ Event stored with unique ID: {saved_event['id']}")
        
        # Add another event
        event_data2 = extractor.extract_intent("Післязавтра о 14 презентація")
        saved_event2 = extractor.save_event(event_data2)
        
        # Verify both events
        events = extractor.get_events()
        assert len(events) == 2, f"Expected 2 events, got {len(events)}"
        assert saved_event['id'] != saved_event2['id'], "Event IDs not unique"
        print(f"✅ Second event stored with unique ID: {saved_event2['id']}")
        
        print("\n✅ Test PASSED: Storage sync working correctly")
        return True


async def test_voice_engine_integration():
    """
    Test integration with Voice Engine
    """
    print("\n" + "="*70)
    print("TEST 6: Voice Engine Integration")
    print("="*70)
    
    # Setup paths
    base_path = Path(__file__).parent
    ontology_path = base_path / "core" / "ontology.json"
    manifest_path = base_path / "public" / "manifest.json"
    
    # Initialize Voice Engine
    engine = VoiceEngine(
        ontology_path=str(ontology_path),
        manifest_path=str(manifest_path)
    )
    
    print("\n✅ Voice Engine initialized with Podija support")
    
    # Process Podija intent
    user_input = "Завтра о 10 нарада"
    saved_event = await engine.process_podija_intent(user_input)
    
    print(f"\n✅ Podija intent processed: {saved_event['title']}")
    print(f"   Date: {saved_event['date']}")
    print(f"   Time: {saved_event['time']}")
    print(f"   ID: {saved_event['id']}")
    
    # Verify event was classified correctly
    event_data = {
        'type': 'podija_event_created',
        'title': saved_event['title'],
        'date': saved_event['date'],
        'time': saved_event['time']
    }
    classified = engine.classify_event(event_data)
    
    print(f"\n✅ Event classified: Level {classified['level']} {classified['emoji']}")
    assert classified['level'] == '111', f"Expected level 111, got {classified['level']}"
    
    print("\n✅ Test PASSED: Voice Engine integration working")
    return True


def run_all_tests():
    """Run all test cases"""
    print("\n" + "="*70)
    print("🧪 ПоДія (Podija) Test Suite")
    print("="*70)
    print(f"Reference Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = []
    
    # Run synchronous tests
    results.append(("Acceptance Criteria 1", test_acceptance_criteria_1()))
    results.append(("Zero-Hallucination", test_no_hallucination()))
    results.append(("Date Calculations", test_date_calculations()))
    results.append(("Time Extraction", test_time_extraction()))
    results.append(("Storage Sync", test_storage_sync()))
    
    # Run async tests
    results.append(("Voice Engine Integration", asyncio.run(test_voice_engine_integration())))
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! 🎉")
        return True
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
