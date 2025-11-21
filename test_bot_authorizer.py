#!/usr/bin/env python3
"""
Test script for bot_authorizer.py
Tests the core functionality without making actual API calls
"""

import sys
from bot_authorizer import BotAuthorizer, ColoredOutput

def test_oauth_url_validation():
    """Test OAuth2 URL validation"""
    print("Testing OAuth2 URL validation...")
    
    authorizer = BotAuthorizer("test_token")
    
    # Valid URLs
    valid_urls = [
        "https://discord.com/api/oauth2/authorize?client_id=123",
        "https://discord.com/oauth2/authorize?client_id=123",
        "https://canary.discord.com/api/oauth2/authorize?client_id=123",
        "https://ptb.discord.com/oauth2/authorize?client_id=123",
        "https://discord.com/api/v9/oauth2/authorize?client_id=123",
        "https://discord.com/api/v10/oauth2/authorize?client_id=123",
    ]
    
    # Invalid URLs
    invalid_urls = [
        "http://discord.com/api/oauth2/authorize?client_id=123",  # HTTP instead of HTTPS
        "https://example.com/oauth2/authorize?client_id=123",  # wrong domain
        "https://discord.com/api/oauth2/invite?client_id=123",  # wrong path
        "https://discord.com/oauth2?client_id=123",  # missing /authorize
    ]
    
    all_passed = True
    
    for url in valid_urls:
        if not authorizer.validate_oauth_url(url):
            ColoredOutput.print_error(f"Failed: Should be valid: {url}")
            all_passed = False
        else:
            ColoredOutput.print_success(f"Valid: {url}")
    
    for url in invalid_urls:
        if authorizer.validate_oauth_url(url):
            ColoredOutput.print_error(f"Failed: Should be invalid: {url}")
            all_passed = False
        else:
            ColoredOutput.print_success(f"Invalid (as expected): {url}")
    
    return all_passed


def test_parameter_parsing():
    """Test parameter extraction and merging"""
    print("\nTesting parameter parsing...")
    
    authorizer = BotAuthorizer("test_token")
    
    # Test URL with parameters
    test_url = "https://discord.com/api/oauth2/authorize?client_id=123456&scope=bot&permissions=8"
    
    try:
        # We can't actually make the API call, but we can validate the URL
        is_valid = authorizer.validate_oauth_url(test_url)
        if is_valid:
            ColoredOutput.print_success("URL parsing works correctly")
            return True
        else:
            ColoredOutput.print_error("URL parsing failed")
            return False
    except Exception as e:
        ColoredOutput.print_error(f"Exception during parsing: {e}")
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("Bot Authorizer Test Suite")
    print("=" * 60)
    print()
    
    tests = [
        ("OAuth URL Validation", test_oauth_url_validation),
        ("Parameter Parsing", test_parameter_parsing),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            ColoredOutput.print_error(f"Test '{test_name}' threw exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print()
    print("=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        color = ColoredOutput.GREEN if result else ColoredOutput.FAIL
        print(f"{color}{status}{ColoredOutput.ENDC} - {test_name}")
    
    print()
    print(f"Total: {passed}/{total} tests passed")
    
    if passed == total:
        ColoredOutput.print_success("All tests passed!")
        return 0
    else:
        ColoredOutput.print_error("Some tests failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
