#!/usr/bin/env python3
"""
Test suite runner for v0.3.0 YouTube Video Intelligence Suite

Runs all tests in the correct order and provides comprehensive reporting.
"""

import subprocess
import sys
import os
import time
from pathlib import Path

def run_test_suite():
    """Run the complete test suite for v0.3.0."""
    
    print("🧪 YouTube Video Intelligence Suite v0.3.0 - Test Suite")
    print("=" * 70)
    
    # Test files in order of importance
    test_files = [
        "test_v030_comprehensive.py",
        "test_tools_functionality.py", 
        "test_resources_system.py",
        "test_prompts_system.py",
        "test_mcp_integration.py"
    ]
    
    results = {}
    total_start_time = time.time()
    
    for test_file in test_files:
        print(f"\n🔬 Running {test_file}...")
        print("-" * 50)
        
        start_time = time.time()
        
        try:
            # Run pytest for the specific file
            result = subprocess.run([
                sys.executable, "-m", "pytest", 
                f"tests/{test_file}", 
                "-v",
                "--tb=short"
            ], capture_output=True, text=True, cwd=Path(__file__).parent.parent)
            
            execution_time = time.time() - start_time
            
            if result.returncode == 0:
                print(f"✅ {test_file} - PASSED ({execution_time:.2f}s)")
                results[test_file] = "PASSED"
            else:
                print(f"❌ {test_file} - FAILED ({execution_time:.2f}s)")
                print(f"Error output:\n{result.stderr}")
                print(f"Test output:\n{result.stdout}")
                results[test_file] = "FAILED"
                
        except Exception as e:
            execution_time = time.time() - start_time
            print(f"💥 {test_file} - ERROR ({execution_time:.2f}s)")
            print(f"Exception: {e}")
            results[test_file] = "ERROR"
    
    total_execution_time = time.time() - total_start_time
    
    # Summary report
    print("\n" + "=" * 70)
    print("📊 TEST SUITE SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for status in results.values() if status == "PASSED")
    failed = sum(1 for status in results.values() if status == "FAILED")
    errors = sum(1 for status in results.values() if status == "ERROR")
    
    print(f"Total Tests: {len(test_files)}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"💥 Errors: {errors}")
    print(f"⏱️  Total Time: {total_execution_time:.2f}s")
    
    print("\nDetailed Results:")
    for test_file, status in results.items():
        status_icon = {"PASSED": "✅", "FAILED": "❌", "ERROR": "💥"}[status]
        print(f"  {status_icon} {test_file}: {status}")
    
    # Overall result
    if failed == 0 and errors == 0:
        print("\n🎉 ALL TESTS PASSED! v0.3.0 is ready for production.")
        return True
    else:
        print(f"\n⚠️  {failed + errors} test(s) failed. Review issues before deploying.")
        return False


def run_quick_smoke_test():
    """Run a quick smoke test to verify basic functionality."""
    
    print("🚀 Quick Smoke Test - Basic Functionality Check")
    print("-" * 50)
    
    try:
        # Test imports
        print("📦 Testing imports...")
        import enhanced_server
        from src.youtube_transcript_server import config, resources, prompts
        print("  ✅ All modules import successfully")
        
        # Test configuration
        print("⚙️  Testing configuration...")
        assert config.settings.version == "0.3.0"
        assert config.settings.server_name == "YouTube Transcript Analysis MCP Server"
        print("  ✅ Configuration is correct")
        
        # Test resources module
        print("📊 Testing resources...")
        assert hasattr(resources, 'cached_transcripts')
        assert hasattr(resources, 'analysis_history')
        assert callable(resources.get_memory_usage)
        print("  ✅ Resources module is functional")
        
        # Test prompts module
        print("💡 Testing prompts...")
        assert hasattr(prompts, 'AVAILABLE_PROMPTS')
        assert len(prompts.AVAILABLE_PROMPTS) >= 6
        print("  ✅ Prompts module is functional")
        
        # Test server initialization
        print("🖥️  Testing server...")
        assert hasattr(enhanced_server, 'mcp')
        # Check that the server was initialized with the correct version
        assert config.settings.version == "0.3.0"
        print("  ✅ Server initializes correctly")
        
        print("\n✅ Smoke test PASSED - Basic functionality is working!")
        return True
        
    except Exception as e:
        print(f"\n❌ Smoke test FAILED: {e}")
        return False


def clean_test_environment():
    """Clean up test environment."""
    
    print("🧹 Cleaning test environment...")
    
    # Clear any cached data
    try:
        from src.youtube_transcript_server import resources
        resources.cached_transcripts.clear()
        resources.analysis_history.clear()
        print("  ✅ Cleared test data")
    except:
        pass
    
    # Remove pytest cache
    cache_dirs = [
        "__pycache__",
        ".pytest_cache",
        "tests/__pycache__"
    ]
    
    for cache_dir in cache_dirs:
        if os.path.exists(cache_dir):
            try:
                import shutil
                shutil.rmtree(cache_dir)
                print(f"  ✅ Removed {cache_dir}")
            except:
                print(f"  ⚠️  Could not remove {cache_dir}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Test suite for YouTube Video Intelligence Suite v0.3.0")
    parser.add_argument("--smoke", action="store_true", help="Run quick smoke test only")
    parser.add_argument("--clean", action="store_true", help="Clean test environment before running")
    
    args = parser.parse_args()
    
    if args.clean:
        clean_test_environment()
        print()
    
    if args.smoke:
        success = run_quick_smoke_test()
    else:
        success = run_test_suite()
    
    sys.exit(0 if success else 1)
