#!/usr/bin/env python3
"""
Test script to verify the truncation fix for Claude Desktop's 100k character limit.
"""

import asyncio
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from enhanced_server import get_youtube_transcript, get_youtube_transcript_ytdlp
from src.youtube_transcript_server.config import settings, smart_truncate_output

async def test_truncation_fix():
    """Test the truncation fix with a real YouTube video."""
    
    # Test video - choose a longer video that would potentially exceed limits
    test_video = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Rick Roll (short video for testing)
    
    print("🧪 Testing YouTube Transcript Truncation Fix")
    print("=" * 60)
    print(f"Test video: {test_video}")
    print(f"Max output chars setting: {settings.max_output_chars:,}")
    print(f"Smart truncation enabled: {settings.enable_smart_truncation}")
    print()
    
    # Test primary extraction method
    print("📥 Testing primary transcript extraction...")
    try:
        result1 = await get_youtube_transcript(test_video)
        print(f"✅ Primary method result length: {len(result1):,} characters")
        
        if len(result1) > 100000:
            print("❌ Result exceeds Claude Desktop's 100k limit!")
        elif "TRANSCRIPT TRUNCATED" in result1:
            print("✅ Smart truncation applied successfully!")
        else:
            print("✅ Result within limits, no truncation needed")
            
    except Exception as e:
        print(f"❌ Primary method failed: {e}")
    
    print()
    
    # Test alternative extraction method
    print("📥 Testing yt-dlp transcript extraction...")
    try:
        result2 = await get_youtube_transcript_ytdlp(test_video)
        print(f"✅ yt-dlp method result length: {len(result2):,} characters")
        
        if len(result2) > 100000:
            print("❌ Result exceeds Claude Desktop's 100k limit!")
        elif "TRANSCRIPT TRUNCATED" in result2:
            print("✅ Smart truncation applied successfully!")
        else:
            print("✅ Result within limits, no truncation needed")
            
    except Exception as e:
        print(f"❌ yt-dlp method failed: {e}")
    
    print()
    
    # Test smart truncation function directly
    print("🔧 Testing smart truncation function...")
    test_content = "Sample transcript line\n" * 5000  # Create content that exceeds limit
    truncated = smart_truncate_output(test_content, test_video)
    
    print(f"Original test content: {len(test_content):,} characters")
    print(f"Truncated content: {len(truncated):,} characters")
    
    if len(truncated) <= settings.max_output_chars:
        print("✅ Smart truncation working correctly!")
    else:
        print("❌ Smart truncation failed to limit output!")
    
    print()
    print("🎉 Truncation fix testing completed!")
    print("The solution should now handle Claude Desktop's 100k character limit.")


if __name__ == "__main__":
    asyncio.run(test_truncation_fix())
