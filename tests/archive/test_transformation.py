#!/usr/bin/env python3
"""
Test script to verify the new Claude Desktop analysis approach
"""

import asyncio
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from server import analyze_video_comprehensive, extract_key_quotes, create_study_notes

async def test_new_analysis_approach():
    """Test that analysis tools return properly formatted prompts for Claude Desktop"""
    
    # Test video URL (a short, common video)
    test_url = "https://www.youtube.com/watch?v=jNQXAC9IVRw"
    
    print("🧪 Testing New Claude Desktop Analysis Approach")
    print("=" * 60)
    
    # Test 1: Comprehensive Analysis
    print("\n1️⃣ Testing comprehensive analysis...")
    try:
        result = await analyze_video_comprehensive(test_url, "summary")
        
        # Check that result contains expected components
        assert "Analysis Request" in result
        assert "Analysis Prompt:" in result
        assert "Transcript:" in result
        assert "Claude Desktop: Please analyze" in result
        print("   ✅ Comprehensive analysis format is correct")
        
        # Show sample of output
        print("   📝 Sample output:")
        print("   " + result[:200] + "..." if len(result) > 200 else result)
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Test 2: Key Quotes Extraction
    print("\n2️⃣ Testing key quotes extraction...")
    try:
        result = await extract_key_quotes(test_url, "education")
        
        # Check format
        assert "Quote Extraction Request" in result
        assert "Analysis Prompt:" in result
        assert "Transcript:" in result
        print("   ✅ Quote extraction format is correct")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Test 3: Study Notes Generation
    print("\n3️⃣ Testing study notes generation...")
    try:
        result = await create_study_notes(test_url, "markdown")
        
        # Check format
        assert "Study Notes Request" in result
        assert "Analysis Prompt:" in result
        assert "Transcript:" in result
        print("   ✅ Study notes format is correct")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("🎉 All tests passed!")
    print("✨ The new approach correctly provides structured prompts for Claude Desktop")
    print("💡 Claude Desktop will now handle all AI analysis without requiring API keys")
    return True

if __name__ == "__main__":
    success = asyncio.run(test_new_analysis_approach())
    sys.exit(0 if success else 1)
