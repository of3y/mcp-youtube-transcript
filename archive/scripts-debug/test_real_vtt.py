#!/usr/bin/env python3
"""
Test parsing logic on real VTT file
"""

import re
from pathlib import Path

def parse_vtt_file(file_path):
    """Parse VTT file using the same logic as enhanced_server.py"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        vtt_content = f.read()
    
    print(f"📄 VTT file: {file_path}")
    print(f"📊 Content length: {len(vtt_content)} characters")
    
    # Parse VTT content using the same logic as enhanced_server.py
    lines = vtt_content.split('\n')
    transcript_lines = []
    
    current_timestamp = None
    current_text_lines = []
    
    print(f"🔍 Processing {len(lines)} VTT lines...")
    
    for i, line in enumerate(lines):
        original_line = line
        line = line.strip()
        
        # Show first 20 lines in detail
        if i < 20:
            print(f"Line {i:2d}: '{original_line}' -> '{line}'")
        
        # Skip empty lines and VTT headers
        if not line or line.startswith('WEBVTT') or line.startswith('Kind:') or line.startswith('Language:'):
            # If we hit an empty line and have accumulated text, process the cue
            if not line and current_timestamp and current_text_lines:
                # Join all text lines for this timestamp
                combined_text = ' '.join(current_text_lines)
                clean_text = re.sub(r'<[^>]+>', '', combined_text).strip()
                if clean_text:
                    transcript_lines.append(f"{current_timestamp} {clean_text}")
                    if len(transcript_lines) <= 10:
                        print(f"  ✅ Added line {len(transcript_lines)}: {current_timestamp} {clean_text[:50]}...")
                current_timestamp = None
                current_text_lines = []
            continue
        
        # Check if line contains timestamp
        if '-->' in line:
            if i < 20:
                print(f"  🕐 Found timestamp line: {line}")
            
            # Process any accumulated text from previous cue
            if current_timestamp and current_text_lines:
                combined_text = ' '.join(current_text_lines)
                clean_text = re.sub(r'<[^>]+>', '', combined_text).strip()
                if clean_text:
                    transcript_lines.append(f"{current_timestamp} {clean_text}")
                    if len(transcript_lines) <= 10:
                        print(f"  ✅ Added line {len(transcript_lines)}: {current_timestamp} {clean_text[:50]}...")
            
            # Extract start time for our format
            time_parts = line.split(' --> ')[0]
            if i < 20:
                print(f"    Time part: {time_parts}")
            
            try:
                # Parse timestamp properly: HH:MM:SS.mmm format
                time_clean = time_parts.split('.')[0].split(':')
                if len(time_clean) >= 3:
                    hours = int(time_clean[0])
                    minutes = int(time_clean[1]) + (hours * 60)
                    seconds = int(time_clean[2])
                    current_timestamp = f"[{minutes:02d}:{seconds:02d}]"
                else:
                    current_timestamp = "[00:00]"
            except (ValueError, IndexError) as e:
                if i < 20:
                    print(f"    ❌ Timestamp parse error: {e}")
                current_timestamp = "[00:00]"
            
            if i < 20:
                print(f"    Current timestamp: {current_timestamp}")
            current_text_lines = []
            continue
        
        # Accumulate text lines for current timestamp
        if current_timestamp:
            current_text_lines.append(line)
            if i < 20:
                print(f"    📝 Text line: {line}")
    
    # Process any remaining cue at the end of file
    if current_timestamp and current_text_lines:
        combined_text = ' '.join(current_text_lines)
        clean_text = re.sub(r'<[^>]+>', '', combined_text).strip()
        if clean_text:
            transcript_lines.append(f"{current_timestamp} {clean_text}")
            print(f"  ✅ Final line {len(transcript_lines)}: {current_timestamp} {clean_text[:50]}...")
    
    print(f"\n📊 Results:")
    print(f"  Total lines parsed: {len(transcript_lines)}")
    
    # Check for duplicates
    seen = set()
    duplicates = []
    
    for i, line in enumerate(transcript_lines):
        if line in seen:
            duplicates.append((i, line))
        else:
            seen.add(line)
    
    print(f"  Unique lines: {len(seen)}")
    print(f"  Duplicates: {len(duplicates)}")
    
    # Show first 10 lines
    print(f"\n📋 First 10 transcript lines:")
    for i, line in enumerate(transcript_lines[:10], 1):
        print(f"  {i:2d}. {line}")
    
    if len(transcript_lines) > 10:
        print(f"  ... and {len(transcript_lines) - 10} more lines")
    
    if duplicates:
        print(f"\n⚠️  DUPLICATES FOUND:")
        for i, (line_num, line) in enumerate(duplicates[:10]):
            print(f"    {i+1}. Line {line_num}: {line[:80]}...")
    else:
        print(f"\n✅ No duplicates found!")
    
    return transcript_lines, duplicates

if __name__ == "__main__":
    vtt_file = "Luis Fonsi - Despacito ft. Daddy Yankee [kJQP7kiw5Fk].en.vtt"
    
    if Path(vtt_file).exists():
        lines, duplicates = parse_vtt_file(vtt_file)
        
        print(f"\n{'='*60}")
        print(f"🎯 Summary:")
        print(f"  Total lines: {len(lines)}")
        print(f"  Duplicates: {len(duplicates)}")
        print(f"  Clean: {len(duplicates) == 0}")
        print(f"{'='*60}")
    else:
        print(f"❌ VTT file not found: {vtt_file}")
