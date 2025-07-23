#!/usr/bin/env python3
"""
Focused test for yt-dlp duplicate line investigation
"""

import os
import sys
import tempfile
import subprocess
import glob
import re
from pathlib import Path

def test_ytdlp_vtt_parsing():
    """Test VTT parsing logic with problematic content"""
    
    # Create test VTT content that might cause duplicates
    test_vtt_content = """WEBVTT
Kind: captions
Language: en

00:00:01.000 --> 00:00:05.000
Hello everyone, welcome to this video
about artificial intelligence

00:00:06.000 --> 00:00:10.000
Today we're going to explore
how AI is changing the world

00:00:11.000 --> 00:00:15.000
First, let's talk about machine learning
and its applications in various fields

00:00:16.000 --> 00:00:20.000
Machine learning algorithms can process
large amounts of data very quickly

00:00:21.000 --> 00:00:25.000
This capability allows them to identify
patterns that humans might miss

00:00:26.000 --> 00:00:30.000
For example, in medical diagnosis
AI can help doctors detect diseases

00:00:31.000 --> 00:00:35.000
The technology is also being used
in autonomous vehicles and robotics

NOTE Paragraph

00:00:36.000 --> 00:00:40.000
However, there are also challenges
and ethical considerations to address
"""

    print("🧪 Testing VTT parsing logic...")
    print(f"📄 VTT content length: {len(test_vtt_content)} characters")
    
    # Parse using the same logic as in enhanced_server.py
    lines = test_vtt_content.split('\n')
    transcript_lines = []
    
    current_timestamp = None
    current_text_lines = []
    
    print(f"🔍 Processing {len(lines)} VTT lines...")
    
    for i, line in enumerate(lines):
        original_line = line
        line = line.strip()
        
        print(f"Line {i:2d}: '{original_line}' -> '{line}'")
        
        # Skip empty lines and VTT headers
        if not line or line.startswith('WEBVTT') or line.startswith('Kind:') or line.startswith('Language:') or line.startswith('NOTE'):
            # If we hit an empty line and have accumulated text, process the cue
            if not line and current_timestamp and current_text_lines:
                # Join all text lines for this timestamp
                combined_text = ' '.join(current_text_lines)
                clean_text = re.sub(r'<[^>]+>', '', combined_text).strip()
                if clean_text:
                    transcript_lines.append(f"{current_timestamp} {clean_text}")
                    print(f"  ✅ Added: {current_timestamp} {clean_text}")
                current_timestamp = None
                current_text_lines = []
            continue
        
        # Check if line contains timestamp
        if '-->' in line:
            print(f"  🕐 Found timestamp line: {line}")
            
            # Process any accumulated text from previous cue
            if current_timestamp and current_text_lines:
                combined_text = ' '.join(current_text_lines)
                clean_text = re.sub(r'<[^>]+>', '', combined_text).strip()
                if clean_text:
                    transcript_lines.append(f"{current_timestamp} {clean_text}")
                    print(f"  ✅ Added: {current_timestamp} {clean_text}")
            
            # Extract start time for our format
            time_parts = line.split(' --> ')[0]
            print(f"    Time part: {time_parts}")
            
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
            except (ValueError, IndexError) as e:
                print(f"    ❌ Timestamp parse error: {e}")
                current_timestamp = "[00:00]"
            
            print(f"    Current timestamp: {current_timestamp}")
            current_text_lines = []
            continue
        
        # Accumulate text lines for current timestamp
        if current_timestamp:
            current_text_lines.append(line)
            print(f"    📝 Text line: {line}")
    
    # Process any remaining cue at the end of file
    if current_timestamp and current_text_lines:
        combined_text = ' '.join(current_text_lines)
        clean_text = re.sub(r'<[^>]+>', '', combined_text).strip()
        if clean_text:
            transcript_lines.append(f"{current_timestamp} {clean_text}")
            print(f"  ✅ Final: {current_timestamp} {clean_text}")
    
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
    
    print(f"\n📋 Final transcript:")
    for i, line in enumerate(transcript_lines, 1):
        print(f"  {i:2d}. {line}")
    
    if duplicates:
        print(f"\n⚠️  DUPLICATES FOUND:")
        for i, (line_num, line) in enumerate(duplicates):
            print(f"    {i+1}. Line {line_num}: {line}")
        return False
    else:
        print(f"\n✅ No duplicates found!")
        return True

def test_real_ytdlp():
    """Test with real yt-dlp download"""
    print(f"\n🛠️  Testing real yt-dlp download...")
    
    # Use a short video with known captions
    test_url = "https://www.youtube.com/watch?v=kJQP7kiw5Fk"
    
    temp_dir = tempfile.mkdtemp(prefix="ytdlp_test_")
    print(f"📁 Temp directory: {temp_dir}")
    
    try:
        # Download subtitles
        cmd = [
            'yt-dlp',
            '--write-auto-subs',
            '--write-subs', 
            '--sub-lang', 'en',
            '--sub-format', 'vtt',
            '--skip-download',
            '--output', f'{temp_dir}/%(title)s.%(ext)s',
            test_url
        ]
        
        print(f"🚀 Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        print(f"Return code: {result.returncode}")
        print(f"Stdout: {result.stdout[:500]}...")
        print(f"Stderr: {result.stderr[:500]}...")
        
        # Look for VTT files
        vtt_files = glob.glob(f'{temp_dir}/*.vtt')
        print(f"VTT files found: {vtt_files}")
        
        if vtt_files:
            vtt_file = vtt_files[0]
            print(f"📄 Reading VTT file: {vtt_file}")
            
            with open(vtt_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            print(f"VTT content length: {len(content)} characters")
            print(f"First 500 characters:")
            print(content[:500])
            
            # Save for manual inspection
            with open('debug_real_vtt.txt', 'w') as f:
                f.write(content)
            print(f"💾 Saved VTT content to debug_real_vtt.txt")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        # Clean up
        import shutil
        try:
            shutil.rmtree(temp_dir)
        except:
            pass

if __name__ == "__main__":
    print("🔍 VTT Parsing Duplicate Investigation")
    print("=" * 50)
    
    # Test 1: VTT parsing logic
    parsing_clean = test_ytdlp_vtt_parsing()
    
    # Test 2: Real yt-dlp download (if available)
    try:
        subprocess.run(['yt-dlp', '--version'], check=True, capture_output=True)
        test_real_ytdlp()
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("\n⚠️  yt-dlp not available, skipping real download test")
    
    print(f"\n{'='*50}")
    print(f"🎯 Summary:")
    print(f"  VTT parsing clean: {parsing_clean}")
    print(f"{'='*50}")
