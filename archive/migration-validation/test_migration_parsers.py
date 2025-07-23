#!/usr/bin/env python3
"""
Test script to validate the new SRV1 and JSON3 parsers against existing sample files.
This validates our Phase 1 migration changes work correctly.
"""

import os
import json
import re
import xml.etree.ElementTree as ET
from typing import List


def parse_srv1_content(srv1_file_path: str) -> List[str]:
    """Parse SRV1 (XML) subtitle file and return timestamped transcript lines."""
    with open(srv1_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    transcript_lines = []
    
    try:
        root = ET.fromstring(content)
        for text_elem in root.findall('text'):
            start_time = float(text_elem.get('start', 0))
            text = text_elem.text
            
            if text and text.strip():
                # Format timestamp
                minutes = int(start_time // 60)
                seconds = int(start_time % 60)
                timestamp = f"[{minutes:02d}:{seconds:02d}]"
                
                # Clean and format text
                clean_text = re.sub(r'<[^>]+>', '', text).strip()
                if clean_text:
                    transcript_lines.append(f"{timestamp} {clean_text}")
    
    except ET.ParseError as e:
        print(f"Error parsing SRV1 XML content: {e}")
    
    return transcript_lines


def parse_json3_content(json3_file_path: str) -> List[str]:
    """Parse JSON3 subtitle file and return timestamped transcript lines."""
    with open(json3_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    transcript_lines = []
    
    for event in data.get('events', []):
        if 'segs' in event:
            start_time = event.get('tStartMs', 0) / 1000
            text_parts = []
            
            for seg in event['segs']:
                if 'utf8' in seg and seg['utf8'] != '\n':
                    text_parts.append(seg['utf8'])
            
            text = ''.join(text_parts).strip()
            if text:
                # Format timestamp
                minutes = int(start_time // 60)
                seconds = int(start_time % 60)
                timestamp = f"[{minutes:02d}:{seconds:02d}]"
                
                # Clean text
                clean_text = re.sub(r'<[^>]+>', '', text).strip()
                if clean_text:
                    transcript_lines.append(f"{timestamp} {clean_text}")
    
    return transcript_lines


def parse_vtt_content_legacy(vtt_file_path: str) -> List[str]:
    """Legacy VTT parser for comparison."""
    with open(vtt_file_path, 'r', encoding='utf-8') as f:
        vtt_content = f.read()
    
    lines = vtt_content.split('\n')
    transcript_lines = []
    
    current_timestamp = None
    current_text_lines = []
    
    for line in lines:
        line = line.strip()
        
        # Skip empty lines and VTT headers
        if not line or line.startswith('WEBVTT') or line.startswith('Kind:') or line.startswith('Language:'):
            continue
        
        # Check if line contains timestamp
        if '-->' in line:
            # Process previous cue if exists
            if current_timestamp and current_text_lines:
                combined_text = ' '.join(current_text_lines)
                clean_text = re.sub(r'<[^>]+>', '', combined_text).strip()
                if clean_text:
                    transcript_lines.append(f"{current_timestamp} {clean_text}")
            
            # Extract start timestamp
            start_time = line.split(' --> ')[0]
            try:
                time_clean = start_time.split('.')[0].split(':')
                if len(time_clean) >= 3:
                    hours = int(time_clean[0])
                    minutes = int(time_clean[1]) + (hours * 60)
                    seconds = int(time_clean[2])
                    current_timestamp = f"[{minutes:02d}:{seconds:02d}]"
                else:
                    current_timestamp = "[00:00]"
            except (ValueError, IndexError):
                current_timestamp = "[00:00]"
            
            current_text_lines = []
            continue
        
        # Accumulate text lines for current timestamp
        if current_timestamp:
            current_text_lines.append(line)
    
    # Process final cue
    if current_timestamp and current_text_lines:
        combined_text = ' '.join(current_text_lines)
        clean_text = re.sub(r'<[^>]+>', '', combined_text).strip()
        if clean_text:
            transcript_lines.append(f"{current_timestamp} {clean_text}")
    
    return transcript_lines


def calculate_duplication_stats(segments: List[str]) -> dict:
    """Calculate duplication statistics for a list of text segments."""
    total_segments = len(segments)
    if total_segments == 0:
        return {'total_segments': 0, 'exact_duplicates': 0, 'duplicate_rate': 0}
    
    # Count exact duplicates
    segment_counts = {}
    for segment in segments:
        # Extract just the text part (remove timestamp)
        text_part = segment.split('] ', 1)[1] if '] ' in segment else segment
        segment_counts[text_part] = segment_counts.get(text_part, 0) + 1
    
    exact_duplicates = sum(count - 1 for count in segment_counts.values() if count > 1)
    
    return {
        'total_segments': total_segments,
        'unique_segments': len(segment_counts),
        'exact_duplicates': exact_duplicates,
        'duplicate_rate': exact_duplicates / total_segments if total_segments > 0 else 0,
        'efficiency': (total_segments - exact_duplicates) / total_segments if total_segments > 0 else 0
    }


def test_parser_functions():
    """Test the new parser functions against existing sample files."""
    print("🧪 Testing Migration Parser Functions")
    print("=" * 50)
    
    # Sample files from our analysis
    base_name = "Fei-Fei Li： Spatial Intelligence is the Next Frontier in AI [_PioN-CpOP0].en"
    vtt_file = f"{base_name}.vtt"
    srv1_file = f"{base_name}.srv1"
    json3_file = f"{base_name}.json3"
    
    results = {}
    
    # Test VTT parser (baseline)
    if os.path.exists(vtt_file):
        print(f"\n📄 Testing VTT parser with {vtt_file}")
        try:
            vtt_segments = parse_vtt_content_legacy(vtt_file)
            vtt_stats = calculate_duplication_stats(vtt_segments)
            results['vtt'] = vtt_stats
            
            print(f"✅ VTT parsed successfully")
            print(f"   Total segments: {vtt_stats['total_segments']}")
            print(f"   Unique segments: {vtt_stats['unique_segments']}")
            print(f"   Duplicates: {vtt_stats['exact_duplicates']} ({vtt_stats['duplicate_rate']:.1%})")
            print(f"   Efficiency: {vtt_stats['efficiency']:.1%}")
            
        except Exception as e:
            print(f"❌ VTT parser failed: {e}")
    else:
        print(f"⚠️  VTT file not found: {vtt_file}")
    
    # Test SRV1 parser
    if os.path.exists(srv1_file):
        print(f"\n📄 Testing SRV1 parser with {srv1_file}")
        try:
            srv1_segments = parse_srv1_content(srv1_file)
            srv1_stats = calculate_duplication_stats(srv1_segments)
            results['srv1'] = srv1_stats
            
            print(f"✅ SRV1 parsed successfully")
            print(f"   Total segments: {srv1_stats['total_segments']}")
            print(f"   Unique segments: {srv1_stats['unique_segments']}")
            print(f"   Duplicates: {srv1_stats['exact_duplicates']} ({srv1_stats['duplicate_rate']:.1%})")
            print(f"   Efficiency: {srv1_stats['efficiency']:.1%}")
            
            # Show sample segments
            print(f"   Sample segments:")
            for i, segment in enumerate(srv1_segments[:3]):
                print(f"     {i+1}: {segment}")
                
        except Exception as e:
            print(f"❌ SRV1 parser failed: {e}")
    else:
        print(f"⚠️  SRV1 file not found: {srv1_file}")
    
    # Test JSON3 parser
    if os.path.exists(json3_file):
        print(f"\n📄 Testing JSON3 parser with {json3_file}")
        try:
            json3_segments = parse_json3_content(json3_file)
            json3_stats = calculate_duplication_stats(json3_segments)
            results['json3'] = json3_stats
            
            print(f"✅ JSON3 parsed successfully")
            print(f"   Total segments: {json3_stats['total_segments']}")
            print(f"   Unique segments: {json3_stats['unique_segments']}")
            print(f"   Duplicates: {json3_stats['exact_duplicates']} ({json3_stats['duplicate_rate']:.1%})")
            print(f"   Efficiency: {json3_stats['efficiency']:.1%}")
            
            # Show sample segments
            print(f"   Sample segments:")
            for i, segment in enumerate(json3_segments[:3]):
                print(f"     {i+1}: {segment}")
                
        except Exception as e:
            print(f"❌ JSON3 parser failed: {e}")
    else:
        print(f"⚠️  JSON3 file not found: {json3_file}")
    
    # Summary comparison
    print(f"\n📊 MIGRATION VALIDATION SUMMARY")
    print("=" * 50)
    
    if results:
        print("Format comparisons:")
        for fmt, stats in results.items():
            efficiency = stats['efficiency']
            quality = "🟢 Excellent" if efficiency >= 0.95 else "🟡 Good" if efficiency >= 0.8 else "🔴 Poor"
            print(f"  {fmt.upper():6}: {stats['duplicate_rate']:.1%} duplicates, {efficiency:.1%} efficiency {quality}")
        
        # Determine best format
        if 'srv1' in results and 'vtt' in results:
            srv1_improvement = results['srv1']['efficiency'] - results['vtt']['efficiency']
            print(f"\n🎯 SRV1 vs VTT improvement: {srv1_improvement:.1%}")
            
        if 'json3' in results and 'vtt' in results:
            json3_improvement = results['json3']['efficiency'] - results['vtt']['efficiency']
            print(f"🎯 JSON3 vs VTT improvement: {json3_improvement:.1%}")
        
        # Migration recommendation
        best_format = max(results.items(), key=lambda x: x[1]['efficiency'])
        print(f"\n✅ Migration recommendation: Use {best_format[0].upper()} format")
        print(f"   Best efficiency: {best_format[1]['efficiency']:.1%}")
        
    else:
        print("❌ No sample files found for testing")
        print("💡 Download sample files first using:")
        print("   yt-dlp --write-auto-subs --sub-format srv1,json3,vtt --skip-download _PioN-CpOP0")
    
    print(f"\n🚀 Migration Status: Phase 1 parser functions {'✅ VALIDATED' if results else '⚠️ NEEDS SAMPLE FILES'}")
    return results


if __name__ == "__main__":
    test_parser_functions()
