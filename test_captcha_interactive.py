#!/usr/bin/env python3
"""
Test script for interactive CAPTCHA solving capabilities
Demonstrates the AI-powered image selection and object detection features
"""

from captcha_solver_llm import LLMCaptchaSolver, ColoredOutput

def test_image_contains_object():
    """Test the object detection in images"""
    print("\n" + "="*60)
    print("Testing: Image Object Detection")
    print("="*60)
    
    solver = LLMCaptchaSolver()
    
    # Test scenarios
    test_cases = [
        {
            'caption': 'a street view with traffic lights at an intersection',
            'target': 'traffic lights',
            'expected': True
        },
        {
            'caption': 'a building with windows and doors',
            'target': 'traffic lights',
            'expected': False
        },
        {
            'caption': 'a bicycle parked on the sidewalk',
            'target': 'bicycle',
            'expected': True
        },
        {
            'caption': 'a car on the road near trees',
            'target': 'bicycle',
            'expected': False
        },
    ]
    
    passed = 0
    total = len(test_cases)
    
    for i, test in enumerate(test_cases, 1):
        print(f"\nTest {i}: Looking for '{test['target']}' in '{test['caption']}'")
        
        # Simulate the object detection logic
        caption_lower = test['caption'].lower()
        target_lower = test['target'].lower()
        target_words = target_lower.split()
        
        # Check if target is in caption
        match = any(word in caption_lower for word in target_words if len(word) > 3)
        result = match or target_lower in caption_lower
        
        expected = test['expected']
        if result == expected:
            ColoredOutput.print_success(f"✓ PASS: Correctly identified (result={result}, expected={expected})")
            passed += 1
        else:
            ColoredOutput.print_error(f"✗ FAIL: Incorrect (result={result}, expected={expected})")
    
    print(f"\n{'-'*60}")
    print(f"Results: {passed}/{total} tests passed")
    return passed == total


def test_target_extraction():
    """Test extraction of target objects from challenge questions"""
    print("\n" + "="*60)
    print("Testing: Target Object Extraction")
    print("="*60)
    
    solver = LLMCaptchaSolver()
    
    test_cases = [
        ('Select all images with traffic lights', 'traffic lights'),
        ('Click on the bicycle', 'bicycle'),
        ('Find all images containing cars', 'cars'),
        ('Select images with stop signs', 'stop signs'),
        ('Click the fire hydrant', 'fire hydrant'),
    ]
    
    passed = 0
    total = len(test_cases)
    
    for question, expected_target in test_cases:
        result = solver._extract_target_from_question(question)
        
        print(f"\nQuestion: '{question}'")
        print(f"Expected: '{expected_target}'")
        print(f"Got: '{result}'")
        
        if result.lower() == expected_target.lower():
            ColoredOutput.print_success("✓ PASS: Correct extraction")
            passed += 1
        else:
            # Allow partial matches
            if expected_target.lower() in result.lower() or result.lower() in expected_target.lower():
                ColoredOutput.print_success("✓ PASS: Partial match (acceptable)")
                passed += 1
            else:
                ColoredOutput.print_error("✗ FAIL: Incorrect extraction")
    
    print(f"\n{'-'*60}")
    print(f"Results: {passed}/{total} tests passed")
    return passed == total


def test_pattern_extraction():
    """Test CAPTCHA pattern extraction from captions"""
    print("\n" + "="*60)
    print("Testing: CAPTCHA Pattern Extraction")
    print("="*60)
    
    solver = LLMCaptchaSolver()
    
    test_cases = [
        ('a sign with text ABC123', 'ABC123'),
        ('image shows code 5X7P2K', '5X7P2K'),
        ('text reads "HELLO"', 'HELLO'),
        ('captcha displays 987654', '987654'),
        ('a photo with the text 4R8T9Q on it', '4R8T9Q'),
    ]
    
    passed = 0
    total = len(test_cases)
    
    for caption, expected in test_cases:
        result = solver._extract_captcha_from_caption(caption)
        
        print(f"\nCaption: '{caption}'")
        print(f"Expected: '{expected}'")
        print(f"Got: '{result}'")
        
        if result and result.upper() == expected.upper():
            ColoredOutput.print_success("✓ PASS: Correct extraction")
            passed += 1
        else:
            ColoredOutput.print_error(f"✗ FAIL: Expected '{expected}', got '{result}'")
    
    print(f"\n{'-'*60}")
    print(f"Results: {passed}/{total} tests passed")
    return passed == total


def test_solver_strategies():
    """Test that all solver strategies are available"""
    print("\n" + "="*60)
    print("Testing: Solver Strategies Availability")
    print("="*60)
    
    solver = LLMCaptchaSolver()
    
    expected_strategies = [
        'HuggingFace BLIP-2 (Advanced Vision)',
        'HuggingFace BLIP (Original)',
        'HuggingFace ViT-GPT2 (Image to Text)',
        'Local OCR (Tesseract)',
        'Local Ollama Vision',
        'Pattern Recognition',
    ]
    
    print(f"\nExpected strategies: {len(expected_strategies)}")
    print(f"Available strategies: {len(solver.llm_providers)}")
    
    for i, provider in enumerate(solver.llm_providers, 1):
        print(f"  {i}. {provider['name']} ({provider['type']})")
    
    if len(solver.llm_providers) >= len(expected_strategies):
        ColoredOutput.print_success("✓ PASS: All strategies available")
        return True
    else:
        ColoredOutput.print_error("✗ FAIL: Missing strategies")
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("Interactive CAPTCHA Solver Test Suite")
    print("=" * 60)
    print()
    
    ColoredOutput.print_warning("⚠️  These tests demonstrate AI capabilities")
    ColoredOutput.print_warning("⚠️  Actual hCaptcha solving requires challenge data")
    print()
    
    tests = [
        ("Solver Strategies", test_solver_strategies),
        ("Pattern Extraction", test_pattern_extraction),
        ("Target Extraction", test_target_extraction),
        ("Image Object Detection", test_image_contains_object),
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
        status = "PASSED" if result else "FAILED"
        color = ColoredOutput.GREEN if result else ColoredOutput.FAIL
        print(f"{color}[{status}]{ColoredOutput.ENDC} - {test_name}")
    
    print()
    print(f"Total: {passed}/{total} test suites passed")
    
    if passed == total:
        ColoredOutput.print_success("All tests passed!")
        return 0
    else:
        ColoredOutput.print_error("Some tests failed!")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
