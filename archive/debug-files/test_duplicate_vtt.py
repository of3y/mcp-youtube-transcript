#!/usr/bin/env python3
"""
Test script to specifically test VTT parsing with duplicate-prone content.
"""

import sys
import os
import tempfile
import shutil
import re

print("🧪 Starting VTT Duplicate Test")
print("=" * 60)
https://www.youtube.com/watch?v=2mezj14pCFI
# Create a synthetic VTT file that would typically produce duplicates
problematic_vtt_content = """WEBVTT
Kind: captions
Language: en

00:00:01.000 --> 00:00:03.000
Please welcome former director

00:00:02.500 --> 00:00:04.500
Please welcome former director of AI

00:00:04.000 --> 00:00:06.000
Please welcome former director of AI Tesla

00:00:05.500 --> 00:00:07.500
Please welcome former director of AI Tesla Andre Carpathy.

00:00:07.000 --> 00:00:09.000
Tesla Andre Carpathy.

00:00:08.500 --> 00:00:10.500
Tesla Andre Carpathy. Hello everyone.
"""

def test_vtt_parsing_duplicates():
    """Test VTT parsing with a file that should produce duplicates."""
    print("🔍 Parsing VTT content:")
    
    lines = problematic_vtt_content.split('\n')
    transcript_lines = []
    
    current_timestamp = None
    current_text_lines = []
    
    for i, line in enumerate(lines):
        line = line.strip()
        print(f"{i+1:2d}. Processing: '{line}'")
        
        # Skip empty lines and VTT headers
        if not line or line.startswith('WEBVTT') or line.startswith('Kind:') or line.startswith('Language:'):
            # If we hit an empty line and have accumulated text, process the cue
            if not line and current_timestamp and current_text_lines:
                combined_text = ' '.join(current_text_lines)
                clean_text = re.sub(r'<[^>]+>', '', combined_text).strip()
                if clean_text:
                    transcript_lines.append(f"{current_timestamp} {clean_text}")
                    print(f"    ✅ Added: {current_timestamp} {clean_text}")
                current_timestamp = None
                current_text_lines = []
            continue
        
        # Check if line contains timestamp
        if '-->' in line:
            # Process any accumulated text from previous cue
            if current_timestamp and current_text_lines:
                combined_text = ' '.join(current_text_lines)
                clean_text = re.sub(r'<[^>]+>', '', combined_text).strip()
                if clean_text:
                    transcript_lines.append(f"{current_timestamp} {clean_text}")
                    print(f"    ✅ Added: {current_timestamp} {clean_text}")
            
            # Extract start time for our format
            time_parts = line.split(' --> ')[0]
            try:
                # Parse timestamp properly: HH:MM:SS.mmm format
                time_clean = time_parts.split('.')[0].split(':')
                if len(time_clean) >= 3:
                    hours = int(time_clean[0])
                    minutes = int(time_clean[1]) + (hours * 60)  # Convert hours to minutes
                    seconds = int(time_clean[2])
                    current_timestamp = f"[{minutes:02d}:{seconds:02d}]"
                else:
                    current_timestamp = "[00:00]"
            except (ValueError, IndexError):
                current_timestamp = "[00:00]"
            
            print(f"    📍 New timestamp: {current_timestamp}")
            current_text_lines = []
            continue
        
        # Accumulate text lines for current timestamp
        if current_timestamp:
            current_text_lines.append(line)
            print(f"    📝 Accumulated text: {line}")
    
    # Process any remaining cue at the end of file
    if current_timestamp and current_text_lines:
        combined_text = ' '.join(current_text_lines)
        clean_text = re.sub(r'<[^>]+>', '', combined_text).strip()
        if clean_text:
            transcript_lines.append(f"{current_timestamp} {clean_text}")
            print(f"    ✅ Final: {current_timestamp} {clean_text}")
    
    print(f"\n📊 Raw transcript lines extracted: {len(transcript_lines)}")
    print("\n🔍 Raw lines:")
    for i, line in enumerate(transcript_lines, 1):
        print(f"{i:2d}. {line}")
    
    return transcript_lines

if __name__ == "__main__":
    try:
        lines = test_vtt_parsing_duplicates()
        print(f"\n✅ Test completed successfully. Generated {len(lines)} lines.")
    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
    """Test VTT parsing with a file that should produce duplicates."""
    print("🧪 Testing VTT Parsing with Duplicate-Prone Content")
    print("=" * 60)
    
    # Create a temporary directory and file
    temp_dir = tempfile.mkdtemp(prefix="test_vtt_")
    vtt_file = os.path.join(temp_dir, "test_video.en.vtt")
    
    try:
        # Write the problematic VTT content
        with open(vtt_file, 'w', encoding='utf-8') as f:
            f.write(problematic_vtt_content)
        
        print(f"📝 Created test VTT file: {vtt_file}")
        print(f"📏 VTT content lines: {len(problematic_vtt_content.strip().split(chr(10)))}")
        
        # Now manually parse this VTT content using the same logic as the script
        from youtube_to_mcp import re
        
        lines = problematic_vtt_content.split('\n')
        transcript_lines = []
        
        current_timestamp = None
        current_text_lines = []
        
        print("\n🔍 Parsing VTT content line by line:")
        print("-" * 40)
        
        for i, line in enumerate(lines):
            line = line.strip()
            print(f"{i+1:2d}. Processing: '{line}'")
            
            # Skip empty lines and VTT headers
            if not line or line.startswith('WEBVTT') or line.startswith('Kind:') or line.startswith('Language:'):
                # If we hit an empty line and have accumulated text, process the cue
                if not line and current_timestamp and current_text_lines:
                    combined_text = ' '.join(current_text_lines)
                    clean_text = re.sub(r'<[^>]+>', '', combined_text).strip()
                    if clean_text:
                        transcript_lines.append(f"{current_timestamp} {clean_text}")
                        print(f"    ✅ Added: {current_timestamp} {clean_text}")
                    current_timestamp = None
                    current_text_lines = []
                continue
            
            # Check if line contains timestamp
            if '-->' in line:
                # Process any accumulated text from previous cue
                if current_timestamp and current_text_lines:
                    combined_text = ' '.join(current_text_lines)
                    clean_text = re.sub(r'<[^>]+>', '', combined_text).strip()
                    if clean_text:
                        transcript_lines.append(f"{current_timestamp} {clean_text}")
                        print(f"    ✅ Added: {current_timestamp} {clean_text}")
                
                # Extract start time for our format
                time_parts = line.split(' --> ')[0]
                try:
                    # Parse timestamp properly: HH:MM:SS.mmm format
                    time_clean = time_parts.split('.')[0].split(':')
                    if len(time_clean) >= 3:
                        hours = int(time_clean[0])
                        minutes = int(time_clean[1]) + (hours * 60)  # Convert hours to minutes
                        seconds = int(time_clean[2])
                        current_timestamp = f"[{minutes:02d}:{seconds:02d}]"
                    else:
                        current_timestamp = "[00:00]"
                except (ValueError, IndexError):
                    current_timestamp = "[00:00]"
                
                print(f"    📍 New timestamp: {current_timestamp}")
                current_text_lines = []
                continue
            
            # Accumulate text lines for current timestamp
            if current_timestamp:
                current_text_lines.append(line)
                print(f"    📝 Accumulated text: {line}")
        
        # Process any remaining cue at the end of file
        if current_timestamp and current_text_lines:
            combined_text = ' '.join(current_text_lines)
            clean_text = re.sub(r'<[^>]+>', '', combined_text).strip()
            if clean_text:
                transcript_lines.append(f"{current_timestamp} {clean_text}")
                print(f"    ✅ Final: {current_timestamp} {clean_text}")
        
        print(f"\n📊 Raw transcript lines extracted: {len(transcript_lines)}")
        print("\n🔍 Raw lines:")
        for i, line in enumerate(transcript_lines, 1):
            print(f"{i:2d}. {line}")
        
        # Analyze duplicates
        duplicate_analysis = analyze_duplicates(transcript_lines)
        
        print(f"\n📈 Duplicate Analysis:")
        print(f"  Total lines: {duplicate_analysis['total_lines']}")
        print(f"  Unique lines: {duplicate_analysis['unique_lines']}")
        print(f"  Duplicate lines: {duplicate_analysis['duplicate_count']}")
        
        if duplicate_analysis['duplicates']:
            print(f"\n⚠️  Found {duplicate_analysis['duplicate_count']} duplicates:")
            for dup in duplicate_analysis['duplicates'][:5]:
                print(f"  - Line {dup['line_number']}: '{dup['line']}'")
                print(f"    (First seen at line {dup['first_occurrence'] + 1})")
        else:
            print(f"\n✅ No exact duplicates found")
        
        # Test deduplication
        from youtube_to_mcp import deduplicate_transcript_lines
        deduplicated = deduplicate_transcript_lines(transcript_lines)
        
        print(f"\n🧹 After deduplication: {len(deduplicated)} lines")
        print("Deduplicated lines:")
        for i, line in enumerate(deduplicated, 1):
            print(f"{i:2d}. {line}")
            
        reduction = len(transcript_lines) - len(deduplicated)
        print(f"\n📉 Reduction: {reduction} lines removed ({reduction/len(transcript_lines)*100:.1f}%)")
        
    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        # Clean up
        try:
            shutil.rmtree(temp_dir)
        except:
            pass

if __name__ == "__main__":
    test_vtt_parsing_duplicates()
