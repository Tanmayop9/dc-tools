#!/usr/bin/env python3
"""
Test script to verify the cache directory is created in a writable location
"""

import sys
import tempfile
from pathlib import Path
from captcha_solver_ultra import UltraAdvancedCaptchaSolver, ColoredOutput


def test_default_cache_directory():
    """Test that default cache directory is in home directory"""
    print("Testing default cache directory location...")
    
    solver = UltraAdvancedCaptchaSolver()
    
    # Verify cache directory is in home directory
    expected_location = Path.home() / 'captcha_cache'
    
    if solver.cache_dir == expected_location:
        ColoredOutput.print_success(f"Cache directory correctly set to: {solver.cache_dir}")
        
        # Verify it exists and is writable
        if solver.cache_dir.exists() and solver.cache_dir.is_dir():
            ColoredOutput.print_success("Cache directory exists and is a directory")
            
            # Test write access
            test_file = solver.cache_dir / "test_write.txt"
            try:
                test_file.write_text("test")
                test_file.unlink()
                ColoredOutput.print_success("Cache directory is writable")
                return True
            except Exception as e:
                ColoredOutput.print_error(f"Cache directory is not writable: {e}")
                return False
        else:
            ColoredOutput.print_error("Cache directory does not exist or is not a directory")
            return False
    else:
        ColoredOutput.print_error(f"Expected: {expected_location}")
        ColoredOutput.print_error(f"Got: {solver.cache_dir}")
        return False


def test_custom_cache_directory():
    """Test that custom cache directory can be specified"""
    print("\nTesting custom cache directory...")
    
    # Use a temporary directory for testing
    with tempfile.TemporaryDirectory() as tmpdir:
        custom_cache = Path(tmpdir) / "custom_captcha_cache"
        
        solver = UltraAdvancedCaptchaSolver(cache_dir=str(custom_cache))
        
        if solver.cache_dir == custom_cache:
            ColoredOutput.print_success(f"Custom cache directory correctly set to: {solver.cache_dir}")
            
            # Verify it was created
            if custom_cache.exists() and custom_cache.is_dir():
                ColoredOutput.print_success("Custom cache directory exists")
                return True
            else:
                ColoredOutput.print_error("Custom cache directory was not created")
                return False
        else:
            ColoredOutput.print_error(f"Expected: {custom_cache}")
            ColoredOutput.print_error(f"Got: {solver.cache_dir}")
            return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("Cache Directory Test Suite")
    print("=" * 60)
    print()
    
    tests = [
        ("Default Cache Directory", test_default_cache_directory),
        ("Custom Cache Directory", test_custom_cache_directory),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            ColoredOutput.print_error(f"Test '{test_name}' threw exception: {e}")
            import traceback
            traceback.print_exc()
            results.append((test_name, False))
    
    # Summary
    print()
    print("=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "PASSED" if result else "FAILED"
        color = ColoredOutput.GREEN if result else ColoredOutput.FAIL
        print(f"{color}[{status}]{ColoredOutput.ENDC} - {test_name}")
    
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
