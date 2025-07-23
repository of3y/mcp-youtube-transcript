#!/usr/bin/env python3
"""
Performance and reliability tests for Video Intelligence Suite
"""

import asyncio
import sys
import os
import time

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import get_youtube_transcript, analyze_video_comprehensive

async def test_performance():
    """Test performance with various video lengths and types"""
    
    print("🚀 Performance Testing - Video Intelligence Suite")
    print("="*60)
    
    # Test videos of different lengths and complexity
    test_cases = [
        {
            "name": "Short Video (19 seconds)",
            "url": "https://www.youtube.com/watch?v=jNQXAC9IVRw",
            "expected_max_time": 10.0  # seconds
        },
        {
            "name": "Medium Video (Rick Roll)",
            "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ", 
            "expected_max_time": 15.0
        }
    ]
    
    results = []
    
    for test_case in test_cases:
        print(f"\n📊 Testing: {test_case['name']}")
        print(f"URL: {test_case['url']}")
        
        # Test transcript extraction speed
        start_time = time.time()
        try:
            transcript = await get_youtube_transcript(test_case['url'])
            transcript_time = time.time() - start_time
            
            if "❌" in transcript:
                print(f"❌ Transcript extraction failed: {transcript[:100]}...")
                results.append({
                    "test": test_case['name'],
                    "transcript_success": False,
                    "transcript_time": transcript_time,
                    "ai_success": False,
                    "ai_time": 0
                })
                continue
                
            print(f"✅ Transcript extracted in {transcript_time:.2f}s")
            print(f"   Length: {len(transcript)} characters")
            
            # Test AI analysis speed (if API keys available)
            ai_success = False
            ai_time = 0
            
            if os.getenv("ANTHROPIC_API_KEY") or os.getenv("OPENAI_API_KEY"):
                start_time = time.time()
                try:
                    analysis = await analyze_video_comprehensive(test_case['url'], "summary")
                    ai_time = time.time() - start_time
                    
                    if "❌" not in analysis:
                        ai_success = True
                        print(f"✅ AI analysis completed in {ai_time:.2f}s")
                    else:
                        print(f"❌ AI analysis failed: {analysis[:100]}...")
                        
                except Exception as e:
                    ai_time = time.time() - start_time
                    print(f"❌ AI analysis error: {e}")
            else:
                print("⚠️  Skipping AI analysis (no API keys)")
            
            results.append({
                "test": test_case['name'],
                "transcript_success": True,
                "transcript_time": transcript_time,
                "ai_success": ai_success,
                "ai_time": ai_time
            })
            
            # Performance check
            if transcript_time > test_case['expected_max_time']:
                print(f"⚠️  Transcript extraction slower than expected ({transcript_time:.2f}s > {test_case['expected_max_time']}s)")
            else:
                print(f"✅ Performance within expected range")
                
        except Exception as e:
            transcript_time = time.time() - start_time
            print(f"❌ Error: {e}")
            results.append({
                "test": test_case['name'],
                "transcript_success": False,
                "transcript_time": transcript_time,
                "ai_success": False,
                "ai_time": 0
            })
    
    # Summary
    print(f"\n{'='*60}")
    print("PERFORMANCE SUMMARY")
    print('='*60)
    
    total_tests = len(results)
    transcript_successes = sum(1 for r in results if r['transcript_success'])
    ai_successes = sum(1 for r in results if r['ai_success'])
    
    print(f"Transcript Extraction: {transcript_successes}/{total_tests} successful")
    print(f"AI Analysis: {ai_successes}/{total_tests} successful")
    
    if results:
        avg_transcript_time = sum(r['transcript_time'] for r in results if r['transcript_success']) / max(1, transcript_successes)
        avg_ai_time = sum(r['ai_time'] for r in results if r['ai_success']) / max(1, ai_successes)
        
        print(f"\nAverage Times:")
        print(f"  Transcript Extraction: {avg_transcript_time:.2f}s")
        if ai_successes > 0:
            print(f"  AI Analysis: {avg_ai_time:.2f}s")
    
    return transcript_successes == total_tests

async def test_error_handling():
    """Test error handling with invalid inputs"""
    
    print(f"\n{'='*60}")
    print("ERROR HANDLING TESTS")
    print('='*60)
    
    error_test_cases = [
        {
            "name": "Invalid URL",
            "url": "https://www.youtube.com/watch?v=invalid123",
            "should_fail": True
        },
        {
            "name": "Non-YouTube URL", 
            "url": "https://www.google.com",
            "should_fail": True
        },
        {
            "name": "Empty URL",
            "url": "",
            "should_fail": True
        }
    ]
    
    for test_case in error_test_cases:
        print(f"\n🧪 Testing: {test_case['name']}")
        try:
            result = await get_youtube_transcript(test_case['url'])
            
            if test_case['should_fail'] and "❌" in result:
                print(f"✅ Correctly handled error: {result[:100]}...")
            elif not test_case['should_fail'] and "❌" not in result:
                print(f"✅ Successfully processed: {len(result)} characters")
            else:
                print(f"⚠️  Unexpected result for {test_case['name']}")
                
        except Exception as e:
            if test_case['should_fail']:
                print(f"✅ Correctly caught exception: {e}")
            else:
                print(f"❌ Unexpected exception: {e}")

async def run_performance_tests():
    """Run all performance tests"""
    
    print("🎯 Starting Performance & Reliability Tests")
    
    success1 = await test_performance()
    await test_error_handling()
    
    print(f"\n{'='*60}")
    print("🏁 PERFORMANCE TESTING COMPLETE")
    print('='*60)
    
    if success1:
        print("✅ All performance tests passed!")
    else:
        print("⚠️  Some performance issues detected")

if __name__ == "__main__":
    asyncio.run(run_performance_tests())
