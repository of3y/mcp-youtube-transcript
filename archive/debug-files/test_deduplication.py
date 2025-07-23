#!/usr/bin/env python3
"""
Test script to demonstrate the deduplication and script generation functionality.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts'))

from youtube_to_mcp import deduplicate_transcript_lines, create_plain_text_script

# Sample problematic lines from the Karpathy transcript
sample_lines = [
    "[00:01] Please welcome former director of AI",
    "[00:03] Please welcome former director of AI", 
    "[00:04] Please welcome former director of AI Tesla Andre Carpathy.",
    "[00:07] Tesla Andre Carpathy.",
    "[00:07] Tesla Andre Carpathy. [Music]",
    "[00:11] [Music]",
    "[00:11] [Music] Hello.",
    "[00:14] [Music]",
    "[00:19] Wow, a lot of people here. Hello.",
    "[00:22] Wow, a lot of people here. Hello.",
    "[00:22] Wow, a lot of people here. Hello. Um, okay. Yeah. So I'm excited to be",
    "[00:24] Um, okay. Yeah. So I'm excited to be",
    "[00:24] Um, okay. Yeah. So I'm excited to be here today to talk to you about software",
    "[00:27] here today to talk to you about software",
    "[00:27] here today to talk to you about software in the era of AI. And I'm told that many",
    "[00:30] in the era of AI. And I'm told that many",
    "[00:30] in the era of AI. And I'm told that many of you are students like bachelors,",
    "[00:32] of you are students like bachelors,",
]

def test_deduplication():
    print("🔍 Testing Deduplication")
    print("=" * 50)
    print(f"Original lines: {len(sample_lines)}")
    
    deduplicated = deduplicate_transcript_lines(sample_lines)
    print(f"After deduplication: {len(deduplicated)}")
    
    print("\n📋 Original vs Deduplicated:")
    print("-" * 50)
    
    for i, line in enumerate(sample_lines):
        status = "✅ KEPT" if line in deduplicated else "❌ REMOVED"
        print(f"{i+1:2d}. {status} {line}")
    
    print("\n📝 Final deduplicated lines:")
    print("-" * 50)
    for i, line in enumerate(deduplicated, 1):
        print(f"{i:2d}. {line}")

def test_script_generation():
    print("\n\n📖 Testing Script Generation")
    print("=" * 50)
    
    # Test with original lines
    script_with_dupes = create_plain_text_script(sample_lines, remove_duplicates=False)
    script_clean = create_plain_text_script(sample_lines, remove_duplicates=True)
    
    print("📄 Script WITH duplicates:")
    print("-" * 30)
    print(script_with_dupes[:300] + "..." if len(script_with_dupes) > 300 else script_with_dupes)
    
    print("\n📄 Script WITHOUT duplicates:")
    print("-" * 30)
    print(script_clean)

if __name__ == "__main__":
    test_deduplication()
    test_script_generation()
