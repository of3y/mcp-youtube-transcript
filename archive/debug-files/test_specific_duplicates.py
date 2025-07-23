#!/usr/bin/env python3
"""
Test deduplication with the exact pattern from VTT parsing.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts'))

from youtube_to_mcp import deduplicate_transcript_lines, analyze_duplicates

# Sample lines that would come from problematic VTT parsing
sample_lines = [
    "[00:01] Please welcome former director",
    "[00:02] Please welcome former director of AI", 
    "[00:04] Please welcome former director of AI Tesla",
    "[00:05] Please welcome former director of AI Tesla Andre Carpathy.",
    "[00:07] Tesla Andre Carpathy.",
    "[00:08] Tesla Andre Carpathy. Hello everyone.",
]

def test_specific_duplicates():
    print("🧪 Testing Specific Duplicate Pattern")
    print("=" * 50)
    
    print(f"📝 Original lines ({len(sample_lines)}):")
    for i, line in enumerate(sample_lines, 1):
        print(f"{i:2d}. {line}")
    
    # Analyze duplicates before deduplication
    duplicate_analysis = analyze_duplicates(sample_lines)
    print(f"\n📊 Duplicate Analysis:")
    print(f"  Total lines: {duplicate_analysis['total_lines']}")
    print(f"  Unique lines: {duplicate_analysis['unique_lines']}")  
    print(f"  Duplicate lines: {duplicate_analysis['duplicate_count']}")
    
    if duplicate_analysis['duplicates']:
        print(f"\n⚠️  Found {duplicate_analysis['duplicate_count']} exact duplicates:")
        for dup in duplicate_analysis['duplicates']:
            print(f"  - Line {dup['line_number']}: '{dup['line']}'")
    else:
        print(f"\n✅ No exact duplicates found (but may have partial overlaps)")
    
    # Test deduplication
    deduplicated = deduplicate_transcript_lines(sample_lines)
    
    print(f"\n🧹 After deduplication ({len(deduplicated)} lines):")
    for i, line in enumerate(deduplicated, 1):
        print(f"{i:2d}. {line}")
    
    reduction = len(sample_lines) - len(deduplicated)
    print(f"\n📉 Reduction: {reduction} lines removed ({reduction/len(sample_lines)*100:.1f}%)")
    
    # Show which lines were removed
    print(f"\n❌ Removed lines:")
    for line in sample_lines:
        if line not in deduplicated:
            print(f"  - {line}")

if __name__ == "__main__":
    test_specific_duplicates()
