#!/usr/bin/env python3
"""
Basic functionality tests for Video Intelligence Suite
"""

import asyncio
import sys
import os

# Add parent directory to path to import server
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import get_youtube_transcript, analyze_video_comprehensive

async def test_basic_functionality():
    """Test basic Video Intelligence Suite functionality"""
    print("🧪 Testing basic Video Intelligence Suite functionality")
    
    # Test with a very short video
    test_url = "https://www.youtube.com/watch?v=jNQXAC9IVRw"
    
    print(f"📹 Testing with: {test_url}")
    
    # Test transcript
    print("\n1️⃣ Testing transcript extraction...")
    try:
        transcript = await get_youtube_transcript(test_url)
        if "❌" in transcript:
            print(f"❌ Transcript failed: {transcript[:100]}...")
            return False
        else:
            print(f"✅ Transcript success: {len(transcript)} characters")
    except Exception as e:
        print(f"❌ Transcript exception: {e}")
        return False
    
    # Test AI analysis
    print("\n2️⃣ Testing AI analysis...")
    try:
        analysis = await analyze_video_comprehensive(test_url, "summary")
        if "❌" in analysis:
            print(f"❌ Analysis failed: {analysis[:100]}...")
            return False
        else:
            print(f"✅ Analysis success: {len(analysis)} characters")
    except Exception as e:
        print(f"❌ Analysis exception: {e}")
        return False
    
    print("\n🎉 All core functions working!")
    return True

if __name__ == "__main__":
    asyncio.run(test_basic_functionality())
