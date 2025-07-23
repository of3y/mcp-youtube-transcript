#!/usr/bin/env python3
"""
Test script to compare different yt-dlp subtitle formats and their impact on transcript quality and deduplication.
"""

import os
import sys
import subprocess
import json
import re
from pathlib import Path
import tempfile
import xml.etree.ElementTree as ET
from collections import defaultdict


def download_subtitles(video_id, format_type, language='en'):
    """Download subtitles in a specific format."""
    temp_dir = tempfile.mkdtemp()
    cmd = [
        'yt-dlp',
        '--write-auto-subs',
        '--sub-langs', language,
        '--sub-format', format_type,
        '--skip-download',
        video_id
    ]
    
    try:
        result = subprocess.run(cmd, cwd=temp_dir, capture_output=True, text=True, check=True)
        
        # Find the downloaded subtitle file
        for file in os.listdir(temp_dir):
            if file.endswith(f'.{format_type}'):
                return os.path.join(temp_dir, file)
        
        return None
    except subprocess.CalledProcessError as e:
        print(f"Error downloading {format_type} format: {e}")
        return None


def parse_vtt(file_path):
    """Parse VTT subtitle file and return list of text segments."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    segments = []
    lines = content.split('\n')
    i = 0
    
    while i < len(lines):
        line = lines[i].strip()
        if '-->' in line:  # Timing line
            i += 1
            text_lines = []
            while i < len(lines) and lines[i].strip() != '':
                text_lines.append(lines[i].strip())
                i += 1
            text = ' '.join(text_lines)
            if text:
                segments.append(text)
        i += 1
    
    return segments


def parse_srv1(file_path):
    """Parse SRV1 (XML) subtitle file and return list of text segments."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    segments = []
    try:
        root = ET.fromstring(content)
        for text_elem in root.findall('text'):
            text = text_elem.text
            if text:
                segments.append(text.strip())
    except ET.ParseError:
        print(f"Error parsing XML file: {file_path}")
    
    return segments


def parse_json3(file_path):
    """Parse JSON3 subtitle file and return list of text segments."""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    segments = []
    for event in data.get('events', []):
        if 'segs' in event:
            text_parts = []
            for seg in event['segs']:
                if 'utf8' in seg:
                    utf8_text = seg['utf8']
                    if utf8_text != '\n':  # Skip newlines
                        text_parts.append(utf8_text)
            text = ''.join(text_parts).strip()
            if text:
                segments.append(text)
    
    return segments


def calculate_duplication_stats(segments):
    """Calculate duplication statistics for a list of text segments."""
    total_segments = len(segments)
    if total_segments == 0:
        return {}
    
    # Count exact duplicates
    segment_counts = defaultdict(int)
    for segment in segments:
        segment_counts[segment] += 1
    
    exact_duplicates = sum(count - 1 for count in segment_counts.values() if count > 1)
    exact_duplicate_rate = exact_duplicates / total_segments
    
    # Count near duplicates (using simple word overlap)
    near_duplicates = 0
    for i, seg1 in enumerate(segments):
        for j, seg2 in enumerate(segments[i+1:], i+1):
            if i != j:
                words1 = set(seg1.lower().split())
                words2 = set(seg2.lower().split())
                if len(words1) > 0 and len(words2) > 0:
                    overlap = len(words1.intersection(words2)) / len(words1.union(words2))
                    if overlap > 0.7:  # 70% word overlap threshold
                        near_duplicates += 1
                        break  # Only count each segment once
    
    near_duplicate_rate = near_duplicates / total_segments
    
    return {
        'total_segments': total_segments,
        'exact_duplicates': exact_duplicates,
        'exact_duplicate_rate': exact_duplicate_rate,
        'near_duplicates': near_duplicates,
        'near_duplicate_rate': near_duplicate_rate,
        'unique_segments': len(segment_counts),
        'most_common_duplicates': sorted(
            [(text, count) for text, count in segment_counts.items() if count > 1],
            key=lambda x: x[1],
            reverse=True
        )[:5]
    }


def test_format(video_id, format_type, language='en'):
    """Test a specific subtitle format."""
    print(f"\n=== Testing {format_type.upper()} format ===")
    
    file_path = download_subtitles(video_id, format_type, language)
    if not file_path:
        print(f"Failed to download {format_type} format")
        return None
    
    try:
        # Parse based on format
        if format_type == 'vtt':
            segments = parse_vtt(file_path)
        elif format_type == 'srv1':
            segments = parse_srv1(file_path)
        elif format_type == 'json3':
            segments = parse_json3(file_path)
        else:
            print(f"Unsupported format: {format_type}")
            return None
        
        stats = calculate_duplication_stats(segments)
        
        print(f"Total segments: {stats['total_segments']}")
        print(f"Unique segments: {stats['unique_segments']}")
        print(f"Exact duplicates: {stats['exact_duplicates']} ({stats['exact_duplicate_rate']:.1%})")
        print(f"Near duplicates: {stats['near_duplicates']} ({stats['near_duplicate_rate']:.1%})")
        
        if stats['most_common_duplicates']:
            print("Most common duplicates:")
            for text, count in stats['most_common_duplicates']:
                print(f"  '{text}' appears {count} times")
        
        # Show first few segments as sample
        print(f"\nFirst 5 segments:")
        for i, seg in enumerate(segments[:5]):
            print(f"  {i+1}: {seg}")
        
        return stats
        
    finally:
        # Clean up
        if os.path.exists(file_path):
            os.remove(file_path)
        temp_dir = os.path.dirname(file_path)
        if os.path.exists(temp_dir):
            os.rmdir(temp_dir)


def main():
    video_id = "_PioN-CpOP0"  # Fei-Fei Li video with duplication issues
    formats_to_test = ['vtt', 'srv1', 'json3']
    
    print(f"Testing subtitle formats for video: {video_id}")
    print("=" * 60)
    
    results = {}
    for format_type in formats_to_test:
        try:
            result = test_format(video_id, format_type)
            if result:
                results[format_type] = result
        except Exception as e:
            print(f"Error testing {format_type}: {e}")
    
    # Summary comparison
    print("\n" + "=" * 60)
    print("SUMMARY COMPARISON")
    print("=" * 60)
    
    for format_type, stats in results.items():
        print(f"{format_type.upper():6}: {stats['exact_duplicate_rate']:.1%} exact, {stats['near_duplicate_rate']:.1%} near, {stats['unique_segments']}/{stats['total_segments']} unique")
    
    # Recommend best format
    if results:
        best_format = min(results.items(), key=lambda x: x[1]['exact_duplicate_rate'])
        print(f"\nBest format for deduplication: {best_format[0].upper()} ({best_format[1]['exact_duplicate_rate']:.1%} exact duplicates)")


if __name__ == "__main__":
    main()
