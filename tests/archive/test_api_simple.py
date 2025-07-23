#!/usr/bin/env python3
"""
Simple API test for YouTube transcript extraction
"""

import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound

def test_simple():
    video_id = "dQw4w9WgXcQ"  # Rick Roll
    print(f"Testing video ID: {video_id}")
    
    try:
        # List available transcripts
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        print("Available transcripts:")
        for transcript in transcript_list:
            print(f"  - {transcript.language_code}: {transcript.language}")
        
        # Try to get transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        print(f"Success! Got {len(transcript)} transcript entries")
        print(f"First entry: {transcript[0]}")
        
    except TranscriptsDisabled:
        print("❌ Transcripts are disabled for this video")
    except NoTranscriptFound:
        print("❌ No transcript found for this video")
    except Exception as e:
        print(f"❌ Other error: {e}")

if __name__ == "__main__":
    test_simple()
