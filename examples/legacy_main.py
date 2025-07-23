#!/usr/bin/env python3
"""
Example usage of the YouTube Video Intelligence Suite

This example demonstrates how to use the MCP server tools programmatically.
Note: This is for reference only - the main usage is through Claude Desktop MCP integration.
"""

import asyncio
import sys
import os

# Add parent directory to path to import server
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import (
    get_youtube_transcript,
    analyze_video_comprehensive,
    create_study_notes,
    generate_quiz
)

async def example_usage():
    """Example of using the YouTube Video Intelligence Suite tools"""
    
    print("🎥 YouTube Video Intelligence Suite - Example Usage")
    print("=" * 55)
    
    # Example video - "Me at the zoo" (first YouTube video)
    video_url = "https://www.youtube.com/watch?v=jNQXAC9IVRw"
    
    print(f"\n📹 Analyzing video: {video_url}")
    
    # 1. Extract transcript
    print("\n1️⃣ Extracting transcript...")
    transcript = await get_youtube_transcript(video_url)
    print(f"Transcript length: {len(transcript)} characters")
    
    # 2. Generate summary
    print("\n2️⃣ Generating AI summary...")
    summary = await analyze_video_comprehensive(video_url, "summary")
    print("Summary generated successfully!")
    
    # 3. Create study notes
    print("\n3️⃣ Creating study notes...")
    notes = await create_study_notes(video_url, "markdown")
    print("Study notes created!")
    
    # 4. Generate quiz
    print("\n4️⃣ Generating quiz...")
    quiz = await generate_quiz(video_url, "easy", 3)
    print("Quiz generated!")
    
    print("\n✅ Example completed successfully!")
    print("\n💡 For actual usage, use these tools through Claude Desktop")
    print("   after configuring the MCP server in claude_desktop_config.json")

def main():
    """Main entry point"""
    print("YouTube Video Intelligence Suite - Example")
    print("This example shows how the tools work programmatically.")
    print("\nFor production use, configure as MCP server in Claude Desktop.")
    print("\nRunning example...")
    
    try:
        asyncio.run(example_usage())
    except KeyboardInterrupt:
        print("\n⚠️  Example interrupted by user")
    except Exception as e:
        print(f"\n❌ Example failed: {e}")
        print("Make sure API keys are set: ANTHROPIC_API_KEY or OPENAI_API_KEY")

if __name__ == "__main__":
    main()
