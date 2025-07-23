#!/usr/bin/env python3
"""
Simple usage example for the Streamlined YouTube Intelligence Suite

This example demonstrates the server's capabilities and shows how to test functionality.
Note: The main usage is through Claude Desktop MCP integration.
"""

import asyncio
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import core functions for testing (not the MCP tools themselves)
from streamlined_server import (
    extract_transcript_ytdlp,
    extract_enhanced_metadata,
    create_plain_text_transcript,
    calculate_quality_score,
    list_available_resources,
    settings
)

async def simple_example():
    """Simple example showing the core functionality"""
    
    print("🎥 YouTube Intelligence Suite v0.5.0 - Core Functions Test")
    print("=" * 65)
    
    # Example video - "Me at the zoo" (first YouTube video)
    video_url = "https://www.youtube.com/watch?v=jNQXAC9IVRw"
    
    print(f"\n📹 Testing with video: {video_url}")
    
    # 1. Test transcript extraction
    print("\n1️⃣ Testing transcript extraction...")
    try:
        result = extract_transcript_ytdlp(video_url, "en")
        if result['success']:
            print(f"✅ Transcript extracted: {result['line_count']} lines")
            print(f"   Quality score: {result['quality_metrics']['quality_score']}%")
            print(f"   Deduplication: {result['quality_metrics']['deduplication_effectiveness']}%")
        else:
            print(f"❌ Extraction failed: {result['error']}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 2. Test metadata extraction
    print("\n2️⃣ Testing metadata extraction...")
    try:
        metadata_result = extract_enhanced_metadata(video_url)
        if metadata_result['success']:
            metadata = metadata_result['metadata']
            print(f"✅ Metadata extracted:")
            print(f"   Title: {metadata.get('title', 'Unknown')}")
            print(f"   Channel: {metadata.get('channel', 'Unknown')}")
            print(f"   Views: {metadata.get('view_count', 0):,}")
        else:
            print(f"❌ Metadata extraction failed: {metadata_result['error']}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 3. Test plain text creation
    print("\n3️⃣ Testing plain text creation...")
    try:
        if 'result' in locals() and result['success']:
            plain_text = create_plain_text_transcript(result['lines'], aggressive_dedup=True)
            print(f"✅ Plain text created: {len(plain_text)} characters")
            print(f"   Sample: {plain_text[:100]}...")
        else:
            print("⚠️ Skipped - no transcript available")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 4. Check available resources
    print("\n4️⃣ Checking available resources...")
    try:
        resources = list_available_resources()
        print(f"✅ Found {len(resources)} existing resources")
        if resources:
            for r in resources[:3]:  # Show first 3
                print(f"   - {r['title']} (ID: {r['video_id']})")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 5. Show server configuration
    print("\n5️⃣ Server configuration:")
    print(f"✅ Server: {settings.server_name} v{settings.version}")
    print(f"   Resource directory: {settings.resource_dir}")
    print(f"   Max output chars: {settings.max_output_chars:,}")
    print(f"   Aggressive dedup: {settings.aggressive_dedup}")
    
    print("\n🎯 Core functionality test completed!")
    print("\n💡 Next Steps:")
    print("  • Start the MCP server: python main.py")
    print("  • Configure in Claude Desktop for production use")
    print("  • Use MCP tools for full AI integration")

def main():
    """Main entry point"""
    print("🚀 YouTube Intelligence Suite - Core Functions Test")
    print("This example tests the core extraction and analysis capabilities.")
    print("\nRunning tests...")
    
    try:
        asyncio.run(simple_example())
    except KeyboardInterrupt:
        print("\n⚠️  Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        print("Make sure yt-dlp is installed: pip install yt-dlp")

if __name__ == "__main__":
    main()
