#!/usr/bin/env python3
"""
Test runner for all Video Intelligence Suite tests
"""

import asyncio
import sys
import os
import importlib.util

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def run_test_file(test_file, test_function=None):
    """Run a specific test file"""
    print(f"\n{'='*60}")
    print(f"RUNNING: {test_file}")
    print('='*60)
    
    try:
        # Import the test module
        spec = importlib.util.spec_from_file_location("test_module", test_file)
        test_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(test_module)
        
        # Run the test function if specified
        if test_function and hasattr(test_module, test_function):
            if asyncio.iscoroutinefunction(getattr(test_module, test_function)):
                asyncio.run(getattr(test_module, test_function)())
            else:
                getattr(test_module, test_function)()
        else:
            # Try to find and run main test function
            for attr_name in dir(test_module):
                attr = getattr(test_module, attr_name)
                if callable(attr) and attr_name.startswith('test_') and not attr_name.startswith('test_module'):
                    if asyncio.iscoroutinefunction(attr):
                        asyncio.run(attr())
                    else:
                        attr()
                    break
        
        print(f"✅ {test_file} completed successfully")
        return True
        
    except Exception as e:
        print(f"❌ {test_file} failed: {e}")
        return False

async def run_all_tests():
    """Run all tests in the test suite"""
    
    print("🧪 Video Intelligence Suite - Test Runner")
    print("="*60)
    
    # Check environment
    has_anthropic = bool(os.getenv("ANTHROPIC_API_KEY"))
    has_openai = bool(os.getenv("OPENAI_API_KEY"))
    
    print(f"🔑 API Keys Status:")
    print(f"   Anthropic: {'✅' if has_anthropic else '❌'}")
    print(f"   OpenAI: {'✅' if has_openai else '❌'}")
    
    if not (has_anthropic or has_openai):
        print("\n⚠️  Warning: No AI API keys found.")
        print("   Set ANTHROPIC_API_KEY or OPENAI_API_KEY to test AI features.")
    
    # Test files to run in order
    test_files = [
        ("test_api_simple.py", "test_simple"),
        ("test_api_debug.py", "simple_test"), 
        ("test_basic.py", "test_basic_functionality"),
        ("test_fixed.py", "test_fixed_functions"),
        ("test_transcript.py", "test_various_videos"),
    ]
    
    # Only run comprehensive suite if we have API keys
    if has_anthropic or has_openai:
        test_files.append(("test_complete_suite.py", "test_all_tools"))
    
    # Get the test directory
    test_dir = os.path.dirname(os.path.abspath(__file__))
    
    results = []
    
    for test_file, test_function in test_files:
        test_path = os.path.join(test_dir, test_file)
        if os.path.exists(test_path):
            success = run_test_file(test_path, test_function)
            results.append((test_file, success))
        else:
            print(f"⚠️  Test file not found: {test_file}")
            results.append((test_file, False))
    
    # Summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print('='*60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_file, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status:8} {test_file}")
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Video Intelligence Suite is ready.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
    
    return passed == total

if __name__ == "__main__":
    asyncio.run(run_all_tests())
