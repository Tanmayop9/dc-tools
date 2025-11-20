#!/usr/bin/env python3
"""
Test script to validate email retrieval functionality
Tests retry logic, fallback mechanisms, and error handling
"""

import sys
import time
from unittest.mock import Mock, patch
import requests.exceptions

# Test the free version
print("="*70)
print("Testing discord_creator_free.py email retrieval...")
print("="*70)

from discord_creator_free import DiscordCreatorFree

def test_email_retry_logic():
    """Test that email retrieval retries on failure"""
    creator = DiscordCreatorFree()
    
    # Mock the session.get to simulate network failures
    original_get = creator.session.get
    call_count = [0]
    
    def mock_get_fail_twice(*args, **kwargs):
        call_count[0] += 1
        if call_count[0] <= 2:
            raise requests.exceptions.ConnectionError("Simulated connection error")
        # Success on third try
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = ["test@1secmail.com"]
        return mock_response
    
    creator.session.get = mock_get_fail_twice
    
    print("\n[TEST] Testing retry logic with 2 failures then success...")
    email = creator.get_temp_email()
    
    if email == "test@1secmail.com":
        print("[✓] PASS: Email retrieved after retries")
        print(f"[✓] Retry logic worked correctly (attempted {call_count[0]} times)")
        return True
    else:
        print(f"[✗] FAIL: Expected 'test@1secmail.com', got '{email}'")
        return False

def test_email_fallback_to_offline():
    """Test that offline email generation works when all retries fail"""
    creator = DiscordCreatorFree()
    
    # Mock to always fail
    def mock_get_always_fail(*args, **kwargs):
        raise requests.exceptions.ConnectionError("Simulated persistent connection error")
    
    creator.session.get = mock_get_always_fail
    
    print("\n[TEST] Testing fallback to offline email generation...")
    email = creator.get_temp_email()
    
    if email and "@1secmail.com" in email:
        print(f"[✓] PASS: Offline email generated: {email}")
        return True
    else:
        print(f"[✗] FAIL: Expected offline email, got '{email}'")
        return False

def test_email_immediate_success():
    """Test that email retrieval works on first try when network is good"""
    creator = DiscordCreatorFree()
    
    # Mock successful response
    def mock_get_success(*args, **kwargs):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = ["success@1secmail.com"]
        return mock_response
    
    creator.session.get = mock_get_success
    
    print("\n[TEST] Testing immediate success scenario...")
    email = creator.get_temp_email()
    
    if email == "success@1secmail.com":
        print("[✓] PASS: Email retrieved on first attempt")
        return True
    else:
        print(f"[✗] FAIL: Expected 'success@1secmail.com', got '{email}'")
        return False

# Run tests
print("\nRunning email retrieval tests...\n")

tests = [
    test_email_immediate_success,
    test_email_retry_logic,
    test_email_fallback_to_offline,
]

passed = 0
failed = 0

for test in tests:
    try:
        if test():
            passed += 1
        else:
            failed += 1
    except Exception as e:
        print(f"[✗] FAIL: Test raised exception: {e}")
        failed += 1
    print()

# Summary
print("="*70)
print(f"Test Results: {passed} passed, {failed} failed out of {len(tests)} tests")
print("="*70)

if failed == 0:
    print("[✓] All tests passed!")
    sys.exit(0)
else:
    print(f"[✗] {failed} test(s) failed")
    sys.exit(1)
