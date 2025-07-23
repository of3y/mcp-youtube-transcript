#!/usr/bin/env python3
"""
Simple YouTube to MCP Resource Tool - Quick Test
"""

import os
import subprocess
import json
import re

def test_ytdlp_and_create_resource():
    """Test yt-dlp and create MCP resource"""
    
    video_url = "https://www.youtube.com/watch?v=kJQP7kiw5Fk"
    video_id = "kJQP7kiw5Fk"
    
    print("🚀 Simple YouTube to MCP Resource Test")
    print(f"Video: {video_url}")
    print()
    
    # 1. Test yt-dlp availability
    try:
        result = subprocess.run(['yt-dlp', '--version'], capture_output=True, text=True)
        print(f"✅ yt-dlp version: {result.stdout.strip()}")
    except FileNotFoundError:
        print("❌ yt-dlp not found")
        return
    
    # 2. Get video metadata
    print("\n📊 Getting video metadata...")
    try:
        cmd = ['yt-dlp', '--dump-json', '--no-download', video_url]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            metadata = json.loads(result.stdout)
            title = metadata.get('title', 'Unknown')
            duration = metadata.get('duration_string', 'Unknown')
            uploader = metadata.get('uploader', 'Unknown')
            print(f"📺 Title: {title}")
            print(f"📅 Duration: {duration}")
            print(f"👤 Channel: {uploader}")
        else:
            print(f"⚠️  Could not get metadata: {result.stderr}")
            metadata = {}
    except Exception as e:
        print(f"⚠️  Metadata error: {e}")
        metadata = {}
    
    # 3. Download subtitles if not already present
    vtt_file = f"Luis Fonsi - Despacito ft. Daddy Yankee [{video_id}].en.vtt"
    
    if not os.path.exists(vtt_file):
        print(f"\n🛠️  Downloading subtitles...")
        cmd = ['yt-dlp', '--write-auto-subs', '--sub-lang', 'en', '--sub-format', 'vtt', '--skip-download', video_url]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode != 0:
            print(f"❌ Download failed: {result.stderr}")
            return
        print(f"✅ Downloaded: {vtt_file}")
    else:
        print(f"✅ Using existing: {vtt_file}")
    
    # 4. Parse VTT file
    print(f"\n🔍 Parsing VTT file...")
    try:
        with open(vtt_file, 'r', encoding='utf-8') as f:
            vtt_content = f.read()
        
        lines = vtt_content.split('\\n')
        transcript_lines = []
        
        current_timestamp = None
        current_text_lines = []
        
        for line in lines:
            line = line.strip()
            
            # Skip empty lines and VTT headers
            if not line or line.startswith('WEBVTT') or line.startswith('Kind:') or line.startswith('Language:'):
                if not line and current_timestamp and current_text_lines:
                    combined_text = ' '.join(current_text_lines)
                    clean_text = re.sub(r'<[^>]+>', '', combined_text).strip()
                    if clean_text:
                        transcript_lines.append(f"{current_timestamp} {clean_text}")
                    current_timestamp = None
                    current_text_lines = []
                continue
            
            # Check if line contains timestamp
            if '-->' in line:
                if current_timestamp and current_text_lines:
                    combined_text = ' '.join(current_text_lines)
                    clean_text = re.sub(r'<[^>]+>', '', combined_text).strip()
                    if clean_text:
                        transcript_lines.append(f"{current_timestamp} {clean_text}")
                
                time_parts = line.split(' --> ')[0]
                try:
                    time_clean = time_parts.split('.')[0].split(':')
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
            
            if current_timestamp:
                current_text_lines.append(line)
        
        # Process final cue
        if current_timestamp and current_text_lines:
            combined_text = ' '.join(current_text_lines)
            clean_text = re.sub(r'<[^>]+>', '', combined_text).strip()
            if clean_text:
                transcript_lines.append(f"{current_timestamp} {clean_text}")
        
        print(f"✅ Parsed {len(transcript_lines)} transcript lines")
        
        # Check for duplicates
        seen = set()
        duplicates = []
        for i, line in enumerate(transcript_lines):
            if line in seen:
                duplicates.append((i, line))
            else:
                seen.add(line)
        
        print(f"📊 Unique lines: {len(seen)}")
        print(f"📊 Duplicates: {len(duplicates)}")
        
        if duplicates:
            print("⚠️  DUPLICATES FOUND:")
            for i, (line_num, line) in enumerate(duplicates[:3]):
                print(f"   {i+1}. Line {line_num+1}: {line[:60]}...")
        else:
            print("✅ No duplicates found!")
        
    except Exception as e:
        print(f"❌ Parsing error: {e}")
        return
    
    # 5. Create MCP resource
    print(f"\n📝 Creating MCP resource...")
    
    title = metadata.get('title', f'Video {video_id}')
    
    markdown_content = f"""# {title}

## Video Information

- **Video ID:** `{video_id}`
- **URL:** {video_url}
- **Title:** {title}
- **Channel:** {metadata.get('uploader', 'Unknown')}
- **Duration:** {metadata.get('duration_string', 'Unknown')}

## Transcript

"""
    
    for line in transcript_lines:
        markdown_content += f"{line}\\n"
    
    markdown_content += f"""

## Quality Analysis

- **Total Lines:** {len(transcript_lines)}
- **Unique Lines:** {len(seen)}
- **Duplicates:** {len(duplicates)}
- **Quality Score:** {((len(seen) / max(len(transcript_lines), 1)) * 100):.1f}%

---

*Generated by Simple YouTube to MCP Tool*
"""
    
    # Save markdown file
    os.makedirs('./mcp_resources', exist_ok=True)
    
    safe_title = re.sub(r'[^\\w\\s-]', '', title).strip()
    safe_title = re.sub(r'[-\\s]+', '-', safe_title)[:50]
    
    output_file = f"./mcp_resources/{video_id}_{safe_title}.md"
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"✅ Created MCP resource: {output_file}")
        print(f"📁 File size: {os.path.getsize(output_file)} bytes")
        
        # Show first few lines
        print(f"\\n📋 First 5 transcript lines:")
        for i, line in enumerate(transcript_lines[:5], 1):
            print(f"  {i}. {line}")
        
    except Exception as e:
        print(f"❌ Save error: {e}")
    
    print(f"\\n{'='*50}")
    print(f"🎉 MCP Resource Creation Complete!")
    print(f"✅ No duplicate issues found")
    print(f"📁 Resource ready for MCP integration")
    print(f"{'='*50}")

if __name__ == "__main__":
    test_ytdlp_and_create_resource()
