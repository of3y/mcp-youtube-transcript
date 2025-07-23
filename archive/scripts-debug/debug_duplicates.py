#!/usr/bin/env python3
"""
Simple test to investigate ytdlp duplicate issue
"""

import os
import sys
import asyncio
import tempfile
import subprocess
import glob
import re
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from enhanced_server import get_youtube_transcript_ytdlp, get_youtube_transcript

def analyze_duplicates(text: str):
    """Analyze text for duplicate lines."""
    lines = text.split('\n')
    # Extract only transcript lines (skip header)
    transcript_lines = []
    in_transcript = False
    
    for line in lines:
        if in_transcript or '[' in line and ']' in line:
            in_transcript = True
            if line.strip():
                transcript_lines.append(line.strip())
    
    print(f"📊 Total transcript lines: {len(transcript_lines)}")
    
    # Check for duplicates
    seen = set()
    duplicates = []
    
    for i, line in enumerate(transcript_lines):
        if line in seen:
            duplicates.append((i, line))
        else:
            seen.add(line)
    
    print(f"🔍 Unique lines: {len(seen)}")
    print(f"⚠️  Duplicates found: {len(duplicates)}")
    
    if duplicates:
        print("\n🚨 DUPLICATE LINES:")
        for i, (line_num, line) in enumerate(duplicates[:10]):  # Show first 10
            print(f"  {i+1}. Line {line_num}: {line[:100]}...")
    
    return len(duplicates) == 0

async def test_real_video():
    """Test with a real YouTube video"""
    # Use a short video that's likely to have captions
    test_urls = [
        "https://www.youtube.com/watch?v=kJQP7kiw5Fk",  # Luis von Ahn TED Talk
        "https://www.youtube.com/watch?v=_uQrJ0TkZlc",  # Python tutorial
    ]
    
    for video_url in test_urls:
        print(f"\n{'='*60}")
        print(f"🎥 Testing video: {video_url}")
        print(f"{'='*60}")
        
        # Test API method
        print(f"\n📡 Testing youtube-transcript-api method...")
        try:
            api_result = await get_youtube_transcript(video_url)
            if "❌" not in api_result:
                print(f"✅ API method successful")
                print(f"📝 Result length: {len(api_result)} characters")
                api_clean = analyze_duplicates(api_result)
                print(f"🔍 API duplicates clean: {api_clean}")
            else:
                print(f"❌ API method failed: {api_result[:200]}...")
        except Exception as e:
            print(f"❌ API method error: {e}")
        
        # Test ytdlp method
        print(f"\n🛠️  Testing yt-dlp method...")
        try:
            ytdlp_result = await get_youtube_transcript_ytdlp(video_url)
            if "❌" not in ytdlp_result:
                print(f"✅ yt-dlp method successful")
                print(f"📝 Result length: {len(ytdlp_result)} characters")
                ytdlp_clean = analyze_duplicates(ytdlp_result)
                print(f"🔍 yt-dlp duplicates clean: {ytdlp_clean}")
                
                # Save raw result for inspection
                with open(f"debug_ytdlp_result.txt", "w") as f:
                    f.write(ytdlp_result)
                print(f"💾 Saved raw result to debug_ytdlp_result.txt")
                
            else:
                print(f"❌ yt-dlp method failed: {ytdlp_result[:200]}...")
        except Exception as e:
            print(f"❌ yt-dlp method error: {e}")
        
        # Try only one video for now
        break

if __name__ == "__main__":
    print("🚀 Real Video Transcript Duplicate Investigation")
    asyncio.run(test_real_video())
