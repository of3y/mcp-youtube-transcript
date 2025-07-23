#!/usr/bin/env python3
"""
Test the fixed MCP server functions
"""

import asyncio
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import get_youtube_transcript, analyze_video_comprehensive

async def test_fixed_functions():
    print("Testing fixed transcript extraction...")
    
    # Test with a simple video that should work
    test_url = "https://www.youtube.com/watch?v=jNQXAC9IVRw"  # "Me at the zoo"
    
    try:
        print(f"Testing get_youtube_transcript with: {test_url}")
        result = await get_youtube_transcript(test_url)
        
        if "❌" in result:
            print(f"Error: {result}")
        else:
            print("✅ Success! Transcript extracted:")
            print(result[:300] + "...")
            
            # Test AI analysis if transcript works
            print("\nTesting AI analysis...")
            ai_result = await analyze_video_comprehensive(test_url, "summary")
            print(f"AI Analysis result: {ai_result[:200]}...")
            
    except Exception as e:
        print(f"Exception: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_fixed_functions())
