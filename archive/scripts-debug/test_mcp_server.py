#!/usr/bin/env python3
"""
Test MCP server functionality directly
"""

import asyncio
import json
import sys
import os

# Add the server module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from server import get_youtube_transcript, analyze_video_comprehensive

async def test_mcp_tools():
    """Test MCP tools directly without the MCP protocol"""
    
    print("🧪 Testing MCP tools directly")
    
    # Test basic transcript extraction
    print("\n1️⃣ Testing get_youtube_transcript...")
    test_url = "https://www.youtube.com/watch?v=jNQXAC9IVRw"
    
    try:
        result = await get_youtube_transcript(test_url)
        if "❌" in result:
            print(f"❌ Transcript failed: {result[:100]}...")
            return False
        else:
            print(f"✅ Transcript success: {len(result)} characters")
    except Exception as e:
        print(f"❌ Exception in transcript: {e}")
        return False
    
    # Test AI analysis
    print("\n2️⃣ Testing analyze_video_comprehensive...")
    try:
        result = await analyze_video_comprehensive(test_url, "summary")
        if "❌" in result:
            print(f"❌ Analysis failed: {result[:100]}...")
            return False
        else:
            print(f"✅ Analysis success: {len(result)} characters")
    except Exception as e:
        print(f"❌ Exception in analysis: {e}")
        return False
    
    print("\n🎉 All MCP tools working correctly!")
    return True

if __name__ == "__main__":
    success = asyncio.run(test_mcp_tools())
    if success:
        print("\n✅ MCP server tools are ready for Claude Desktop")
        print("🔄 Make sure to restart Claude Desktop to load the new server")
    else:
        print("\n❌ Some issues found with MCP tools")
        sys.exit(1)
