#!/usr/bin/env python3
"""
Test script to debug YouTube transcript extraction
"""

import asyncio
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import get_youtube_transcript, extract_video_id
from youtube_transcript_api import YouTubeTranscriptApi

async def test_various_videos():
    """Test transcript extraction with various YouTube videos"""
    
    test_videos = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",  # Rick Roll (very popular)
        "https://www.youtube.com/watch?v=jNQXAC9IVRw",  # Me at the zoo (first YouTube video)
        "https://www.youtube.com/watch?v=9bZkp7q19f0",  # Popular TED talk
        "https://youtu.be/dQw4w9WgXcQ",  # Short URL format
    ]
    
    for video_url in test_videos:
        print(f"\n{'='*60}")
        print(f"Testing: {video_url}")
        print(f"{'='*60}")
        
        try:
            # Test video ID extraction
            video_id = extract_video_id(video_url)
            print(f"✅ Video ID extracted: {video_id}")
            
            # Test direct API call
            print("🔍 Testing direct YouTubeTranscriptApi...")
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            
            print("Available transcripts:")
            for transcript in transcript_list:
                print(f"  - {transcript.language_code}: {transcript.language}")
                if transcript.is_generated:
                    print("    (Auto-generated)")
                else:
                    print("    (Manual)")
            
            # Try to get English transcript
            try:
                transcript = transcript_list.find_transcript(['en'])
                transcript_data = transcript.fetch()
                print(f"✅ Transcript found! First few entries:")
                for i, entry in enumerate(transcript_data[:3]):
                    print(f"  {entry['start']:.1f}s: {entry['text']}")
                
                # Test our function
                print("\n🧪 Testing our MCP function...")
                result = await get_youtube_transcript(video_url)
                print(f"✅ Function result: {result[:200]}...")
                
            except Exception as e:
                print(f"❌ Error getting transcript: {e}")
                
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_various_videos())
