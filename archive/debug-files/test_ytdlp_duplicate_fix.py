#!/usr/bin/env python3
"""
Test script to verify the fix for duplicate lines in get_youtube_transcript_ytdlp function.

This test creates mock VTT content that would have caused the duplicate line issue
and verifies that the fixed parsing logic properly handles:
1. Multiple text lines per timestamp cue
2. Proper timestamp parsing
3. No duplicate entries in the output
"""

import os
import tempfile
import asyncio
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from enhanced_server import get_youtube_transcript_ytdlp

# Mock VTT content that would cause duplicates with the old logic
MOCK_VTT_CONTENT_PROBLEMATIC = """WEBVTT
Kind: captions
Language: en

00:00:00.000 --> 00:00:05.000
There was a 5-year waiting
list and we got a rotary telephone, but

00:00:06.000 --> 00:00:10.000
it was amazing technology at the time
even though it seems primitive now

00:00:11.000 --> 00:00:15.000
The world was changing rapidly
and we were all excited
about the future possibilities

00:00:16.000 --> 00:00:20.000
Single line entry here

00:00:21.000 --> 00:00:25.000
This has HTML <b>formatting</b> tags
that need to be <i>removed</i> properly
"""

# Expected output after proper parsing (what we want to see)
EXPECTED_OUTPUT_LINES = [
    "[00:00] There was a 5-year waiting list and we got a rotary telephone, but",
    "[00:06] it was amazing technology at the time even though it seems primitive now", 
    "[00:11] The world was changing rapidly and we were all excited about the future possibilities",
    "[00:16] Single line entry here",
    "[00:21] This has HTML formatting tags that need to be removed properly"
]

class MockSubprocessResult:
    """Mock subprocess result for testing"""
    def __init__(self, returncode=0, stderr=""):
        self.returncode = returncode
        self.stderr = stderr

async def test_ytdlp_duplicate_fix():
    """Test that the ytdlp function no longer produces duplicate lines"""
    
    print("🧪 Testing YouTube Transcript ytdlp Duplicate Line Fix")
    print("=" * 60)
    
    # Create a temporary VTT file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.en.vtt', delete=False) as temp_file:
        temp_file.write(MOCK_VTT_CONTENT_PROBLEMATIC)
        temp_vtt_path = temp_file.name
    
    try:
        # Mock the subprocess and glob behavior
        import subprocess
        import glob
        
        # Store original functions
        original_run = subprocess.run
        original_glob = glob.glob
        
        def mock_subprocess_run(*args, **kwargs):
            return MockSubprocessResult(returncode=0)
        
        def mock_glob(pattern):
            if '*.en.vtt' in pattern:
                return [temp_vtt_path]
            return []
        
        # Apply mocks
        subprocess.run = mock_subprocess_run
        glob.glob = mock_glob
        
        # Test with a sample YouTube URL
        test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        
        print(f"📺 Testing with URL: {test_url}")
        print(f"📄 Using mock VTT file: {temp_vtt_path}")
        print()
        
        # Run the function
        result = await get_youtube_transcript_ytdlp(test_url, "en")
        
        # Restore original functions
        subprocess.run = original_run
        glob.glob = original_glob
        
        print("📊 Analysis Results:")
        print("-" * 40)
        
        # Check if the function succeeded
        if "❌" in result:
            print(f"❌ Function failed: {result}")
            return False
        
        # Extract the transcript part (remove header)
        lines = result.split('\n')
        transcript_lines = []
        in_transcript = False
        
        for line in lines:
            if in_transcript:
                transcript_lines.append(line)
            elif line.strip() == "":
                in_transcript = True
        
        # Remove empty lines
        transcript_lines = [line for line in transcript_lines if line.strip()]
        
        print(f"✅ Function executed successfully")
        print(f"📝 Generated {len(transcript_lines)} transcript lines")
        print()
        
        # Test 1: Check for duplicates
        print("🔍 Test 1: Checking for duplicate lines...")
        duplicates_found = []
        seen_lines = set()
        
        for line in transcript_lines:
            if line in seen_lines:
                duplicates_found.append(line)
            seen_lines.add(line)
        
        if duplicates_found:
            print(f"❌ DUPLICATE LINES FOUND: {len(duplicates_found)}")
            for dup in duplicates_found:
                print(f"   - {dup}")
            return False
        else:
            print("✅ No duplicate lines found")
        
        # Test 2: Check expected content
        print("\n🔍 Test 2: Checking expected content...")
        all_expected_found = True
        
        for expected_line in EXPECTED_OUTPUT_LINES:
            found = any(expected_line in transcript_line for transcript_line in transcript_lines)
            if found:
                print(f"✅ Found: {expected_line}")
            else:
                print(f"❌ Missing: {expected_line}")
                all_expected_found = False
        
        # Test 3: Check timestamp format
        print("\n🔍 Test 3: Checking timestamp format...")
        timestamp_format_correct = True
        
        for line in transcript_lines:
            if not line.startswith('[') or ']' not in line:
                print(f"❌ Invalid timestamp format: {line}")
                timestamp_format_correct = False
        
        if timestamp_format_correct:
            print("✅ All timestamps properly formatted")
        
        # Test 4: Check HTML tag removal
        print("\n🔍 Test 4: Checking HTML tag removal...")
        html_tags_found = []
        
        for line in transcript_lines:
            if '<' in line and '>' in line:
                html_tags_found.append(line)
        
        if html_tags_found:
            print(f"❌ HTML tags still present in {len(html_tags_found)} lines:")
            for line in html_tags_found:
                print(f"   - {line}")
            return False
        else:
            print("✅ All HTML tags properly removed")
        
        # Test 5: Check line combining
        print("\n🔍 Test 5: Checking multi-line cue combining...")
        
        # Look for the specific multi-line cue we know should be combined
        combined_waiting_line = None
        for line in transcript_lines:
            if "There was a 5-year waiting list and we got a rotary telephone" in line:
                combined_waiting_line = line
                break
        
        if combined_waiting_line:
            print(f"✅ Multi-line cue properly combined: {combined_waiting_line}")
        else:
            print("❌ Multi-line cue not properly combined")
            return False
        
        print("\n" + "=" * 60)
        print("📋 FINAL TRANSCRIPT OUTPUT:")
        print("-" * 60)
        for i, line in enumerate(transcript_lines, 1):
            print(f"{i:2d}. {line}")
        
        print("\n" + "=" * 60)
        
        if all_expected_found and timestamp_format_correct and not duplicates_found:
            print("🎉 ALL TESTS PASSED! The duplicate line issue has been fixed.")
            return True
        else:
            print("❌ Some tests failed. Please review the output above.")
            return False
            
    finally:
        # Clean up temporary file
        try:
            os.unlink(temp_vtt_path)
        except:
            pass

async def test_edge_cases():
    """Test edge cases that might cause issues"""
    
    print("\n🧪 Testing Edge Cases")
    print("=" * 30)
    
    # Test case: Empty VTT file
    print("\n📝 Test: Empty VTT file")
    empty_vtt = "WEBVTT\n\n"
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.en.vtt', delete=False) as temp_file:
        temp_file.write(empty_vtt)
        temp_path = temp_file.name
    
    try:
        import subprocess
        import glob
        
        original_run = subprocess.run
        original_glob = glob.glob
        
        subprocess.run = lambda *args, **kwargs: MockSubprocessResult(returncode=0)
        glob.glob = lambda pattern: [temp_path] if '*.en.vtt' in pattern else []
        
        result = await get_youtube_transcript_ytdlp("https://www.youtube.com/watch?v=test", "en")
        
        subprocess.run = original_run
        glob.glob = original_glob
        
        if "Could not parse transcript content" in result:
            print("✅ Empty VTT file handled correctly")
        else:
            print(f"❌ Unexpected result for empty VTT: {result}")
        
    finally:
        try:
            os.unlink(temp_path)
        except:
            pass
    
    # Test case: Malformed timestamps
    print("\n📝 Test: Malformed timestamps")
    malformed_vtt = """WEBVTT

INVALID_TIMESTAMP --> 00:00:05.000
This should be handled gracefully

00:00:10.000 --> INVALID_END
This should also be handled
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.en.vtt', delete=False) as temp_file:
        temp_file.write(malformed_vtt)
        temp_path = temp_file.name
    
    try:
        import subprocess
        import glob
        
        original_run = subprocess.run
        original_glob = glob.glob
        
        subprocess.run = lambda *args, **kwargs: MockSubprocessResult(returncode=0)
        glob.glob = lambda pattern: [temp_path] if '*.en.vtt' in pattern else []
        
        result = await get_youtube_transcript_ytdlp("https://www.youtube.com/watch?v=test", "en")
        
        subprocess.run = original_run
        glob.glob = original_glob
        
        if "❌" not in result:
            print("✅ Malformed timestamps handled gracefully")
        else:
            print(f"❌ Function failed with malformed timestamps: {result}")
        
    finally:
        try:
            os.unlink(temp_path)
        except:
            pass

async def main():
    """Run all tests"""
    print("🚀 Starting YouTube Transcript ytdlp Fix Tests\n")
    
    # Run main test
    main_test_passed = await test_ytdlp_duplicate_fix()
    
    # Run edge case tests
    await test_edge_cases()
    
    print("\n" + "=" * 60)
    if main_test_passed:
        print("🎊 OVERALL RESULT: SUCCESS - The duplicate line fix is working correctly!")
    else:
        print("💥 OVERALL RESULT: FAILURE - Issues detected, please review the output.")
    print("=" * 60)
    
    return main_test_passed

if __name__ == "__main__":
    # Run the async main function
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
