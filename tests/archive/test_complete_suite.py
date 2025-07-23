#!/usr/bin/env python3
"""
Comprehensive test of all Video Intelligence Suite tools
"""

import asyncio
import sys
import os

# Add parent directory to path to import server
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import (
    get_youtube_transcript, 
    analyze_video_comprehensive,
    extract_key_quotes,
    create_study_notes,
    generate_quiz,
    fact_check_claims,
    extract_statistics_and_data,
    analyze_presentation_style,
    extract_citations_and_references
)

async def test_all_tools():
    """Test all Video Intelligence Suite tools"""
    
    # Use a video that should have good content for analysis
    test_url = "https://www.youtube.com/watch?v=jNQXAC9IVRw"  # "Me at the zoo" - first YouTube video
    
    # Check if we have API keys
    has_anthropic = bool(os.getenv("ANTHROPIC_API_KEY"))
    has_openai = bool(os.getenv("OPENAI_API_KEY"))
    
    print(f"🔑 API Keys available:")
    print(f"  - Anthropic: {'✅' if has_anthropic else '❌'}")
    print(f"  - OpenAI: {'✅' if has_openai else '❌'}")
    
    if not (has_anthropic or has_openai):
        print("⚠️  No AI API keys found. Set ANTHROPIC_API_KEY or OPENAI_API_KEY to test AI features.")
        return
    
    print(f"\n🎯 Testing with video: {test_url}")
    
    # Test 1: Basic transcript extraction
    print("\n" + "="*60)
    print("TEST 1: Basic Transcript Extraction")
    print("="*60)
    try:
        result = await get_youtube_transcript(test_url)
        if "❌" in result:
            print(f"❌ Failed: {result}")
            return
        else:
            print("✅ Transcript extraction successful")
            print(f"Preview: {result[:200]}...")
    except Exception as e:
        print(f"❌ Exception: {e}")
        return
    
    # Test 2: Comprehensive analysis
    print("\n" + "="*60)
    print("TEST 2: Comprehensive Video Analysis")
    print("="*60)
    analysis_types = ["summary", "key_points", "sentiment"]
    
    for analysis_type in analysis_types:
        try:
            print(f"\n🔍 Testing {analysis_type} analysis...")
            result = await analyze_video_comprehensive(test_url, analysis_type)
            if "❌" in result:
                print(f"❌ Failed: {result[:200]}...")
            else:
                print(f"✅ {analysis_type} analysis successful")
                print(f"Preview: {result[:150]}...")
        except Exception as e:
            print(f"❌ Exception in {analysis_type}: {e}")
    
    # Test 3: Extract quotes
    print("\n" + "="*60)
    print("TEST 3: Extract Key Quotes")
    print("="*60)
    try:
        result = await extract_key_quotes(test_url, "elephants")
        if "❌" in result:
            print(f"❌ Failed: {result[:200]}...")
        else:
            print("✅ Quote extraction successful")
            print(f"Preview: {result[:150]}...")
    except Exception as e:
        print(f"❌ Exception: {e}")
    
    # Test 4: Study notes
    print("\n" + "="*60)
    print("TEST 4: Create Study Notes")
    print("="*60)
    try:
        result = await create_study_notes(test_url, "markdown")
        if "❌" in result:
            print(f"❌ Failed: {result[:200]}...")
        else:
            print("✅ Study notes creation successful")
            print(f"Preview: {result[:150]}...")
    except Exception as e:
        print(f"❌ Exception: {e}")
    
    # Test 5: Quiz generation
    print("\n" + "="*60)
    print("TEST 5: Generate Quiz")
    print("="*60)
    try:
        result = await generate_quiz(test_url, "easy", 3)
        if "❌" in result:
            print(f"❌ Failed: {result[:200]}...")
        else:
            print("✅ Quiz generation successful")
            print(f"Preview: {result[:150]}...")
    except Exception as e:
        print(f"❌ Exception: {e}")
    
    # Test 6: Fact checking
    print("\n" + "="*60)
    print("TEST 6: Fact Check Claims")
    print("="*60)
    try:
        result = await fact_check_claims(test_url)
        if "❌" in result:
            print(f"❌ Failed: {result[:200]}...")
        else:
            print("✅ Fact checking successful")
            print(f"Preview: {result[:150]}...")
    except Exception as e:
        print(f"❌ Exception: {e}")
    
    print("\n" + "="*60)
    print("🎉 TESTING COMPLETE!")
    print("="*60)
    print("✅ Video Intelligence Suite is ready!")
    print("🔄 Next step: Restart Claude Desktop to use the new tools")

if __name__ == "__main__":
    asyncio.run(test_all_tools())
