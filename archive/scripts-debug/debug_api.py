#!/usr/bin/env python3
"""
Debug script to understand the new youtube-transcript-api structure
"""

from youtube_transcript_api import YouTubeTranscriptApi
import json

def debug_api():
    video_id = "dQw4w9WgXcQ"  # Rick Roll video
    
    print("=== Testing list_transcripts ===")
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        print(f"transcript_list type: {type(transcript_list)}")
        
        for transcript in transcript_list:
            print(f"transcript type: {type(transcript)}")
            print(f"transcript attributes: {dir(transcript)}")
            print(f"language_code: {transcript.language_code}")
            print(f"language: {transcript.language}")
            print(f"is_generated: {transcript.is_generated}")
            
            # Try to fetch the actual transcript data
            print("\n=== Fetching transcript data ===")
            try:
                transcript_data = transcript.fetch()
                print(f"transcript_data type: {type(transcript_data)}")
                
                if hasattr(transcript_data, '__iter__'):
                    print("transcript_data is iterable")
                    for i, item in enumerate(transcript_data):
                        print(f"Item {i} type: {type(item)}")
                        print(f"Item {i} content: {item}")
                        if i >= 2:  # Only show first 3 items
                            break
                else:
                    print(f"transcript_data content: {transcript_data}")
                    
            except Exception as e:
                print(f"Error fetching transcript: {e}")
                
            break  # Only test the first transcript
            
    except Exception as e:
        print(f"Error listing transcripts: {e}")
    
    print("\n=== Testing direct get_transcript ===")
    try:
        transcript_data = YouTubeTranscriptApi.get_transcript(video_id)
        print(f"Direct transcript_data type: {type(transcript_data)}")
        
        if hasattr(transcript_data, '__iter__'):
            print("Direct transcript_data is iterable")
            for i, item in enumerate(transcript_data):
                print(f"Item {i} type: {type(item)}")
                print(f"Item {i} content: {item}")
                if i >= 2:  # Only show first 3 items
                    break
        else:
            print(f"Direct transcript_data content: {transcript_data}")
            
    except Exception as e:
        print(f"Error getting direct transcript: {e}")

if __name__ == "__main__":
    debug_api()
