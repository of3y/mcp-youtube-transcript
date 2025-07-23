#!/usr/bin/env python3
"""
Debug test for YouTube API compatibility
"""

import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from youtube_transcript_api import YouTubeTranscriptApi

def simple_test():
    # Use a simple educational video that should have transcripts
    video_id = "jNQXAC9IVRw"  # "Me at the zoo" - first YouTube video
    
    try:
        print("Testing direct get_transcript...")
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        print(f"Success! Type: {type(transcript)}")
        print(f"Length: {len(transcript)}")
        print(f"First item: {transcript[0]}")
        print(f"First item type: {type(transcript[0])}")
        
        if len(transcript) > 0:
            first_item = transcript[0]
            print(f"First item keys: {first_item.keys() if hasattr(first_item, 'keys') else 'No keys method'}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    simple_test()
