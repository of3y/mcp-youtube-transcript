#!/usr/bin/env python3
"""
Advanced YouTube Transcript CLI Tool

This tool:
1. Downloads transcripts using both methods (API and yt-dlp)
2. Analyzes for duplicates and issues
3. Saves clean markdown versions for MCP resource usage
4. Provides detailed debugging information
"""

import os
import sys
import argparse
import asyncio
import re
import subprocess
import glob
import tempfile
import shutil
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
import json

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from youtube_transcript_api import YouTubeTranscriptApi
    from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
except ImportError:
    print("❌ youtube-transcript-api not installed. Install with: uv add youtube-transcript-api")
    sys.exit(1)


def extract_video_id(url: str) -> str:
    """Extract YouTube video ID from various URL formats."""
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
        r'(?:embed\/)([0-9A-Za-z_-]{11})',
        r'(?:youtu\.be\/)([0-9A-Za-z_-]{11})'
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    raise ValueError(f"Could not extract video ID from URL: {url}")


def get_video_info_ytdlp(video_url: str) -> Dict[str, Any]:
    """Get video information using yt-dlp."""
    try:
        cmd = ['yt-dlp', '--dump-json', '--no-download', video_url]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            return json.loads(result.stdout)
    except Exception as e:
        print(f"⚠️  Could not get video info: {e}")
    return {}


def extract_transcript_api(video_url: str, language: str = "en") -> Dict[str, Any]:
    """Extract transcript using youtube-transcript-api."""
    print(f"🔍 Extracting transcript using youtube-transcript-api...")
    
    try:
        video_id = extract_video_id(video_url)
        
        # Get available transcripts
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        available_languages = []
        for transcript in transcript_list:
            available_languages.append(f"{transcript.language_code} ({'auto' if transcript.is_generated else 'manual'})")
        
        print(f"📋 Available languages: {', '.join(available_languages)}")
        
        # Try to find the requested language
        try:
            transcript = transcript_list.find_transcript([language])
        except NoTranscriptFound:
            try:
                transcript = transcript_list.find_transcript(['en'])
                language = 'en'
                print(f"⚠️  Requested language not found, using English")
            except NoTranscriptFound:
                transcript = transcript_list.find_generated_transcript(['en'])
                language = 'en (auto-generated)'
                print(f"⚠️  Manual transcript not found, using auto-generated")
        
        # Get transcript data
        transcript_data = transcript.fetch()
        
        # Format transcript
        formatted_lines = []
        for entry in transcript_data:
            if isinstance(entry, dict):
                start_time = entry.get('start', 0)
                text = entry.get('text', '')
            elif hasattr(entry, 'start') and hasattr(entry, 'text'):
                start_time = entry.start
                text = entry.text
            else:
                start_time = 0
                text = str(entry)
            
            timestamp = f"[{int(start_time//60):02d}:{int(start_time%60):02d}]"
            formatted_lines.append(f"{timestamp} {text}")
        
        return {
            'method': 'youtube-transcript-api',
            'success': True,
            'language': language,
            'available_languages': available_languages,
            'lines': formatted_lines,
            'line_count': len(formatted_lines),
            'raw_data': transcript_data[:5]  # First 5 entries for debugging
        }
        
    except Exception as e:
        return {
            'method': 'youtube-transcript-api',
            'success': False,
            'error': str(e),
            'lines': [],
            'line_count': 0
        }


def extract_transcript_ytdlp(video_url: str, language: str = "en", debug: bool = False) -> Dict[str, Any]:
    """Extract transcript using yt-dlp with detailed debugging."""
    print(f"🔍 Extracting transcript using yt-dlp...")
    
    temp_dir = None
    try:
        video_id = extract_video_id(video_url)
        
        # Create temporary directory for downloads
        temp_dir = tempfile.mkdtemp(prefix="ytdlp_transcript_")
        if debug:
            print(f"📁 Temp directory: {temp_dir}")
        
        # Download subtitles using yt-dlp
        cmd = [
            'yt-dlp',
            '--write-auto-subs',
            '--write-subs', 
            '--sub-lang', language,
            '--sub-format', 'vtt',
            '--skip-download',
            '--output', f'{temp_dir}/%(title)s.%(ext)s',
            video_url
        ]
        
        if debug:
            print(f"🚀 Running: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode != 0:
            if debug:
                print(f"⚠️  First attempt failed, trying auto-generated subtitles only...")
                print(f"   Stderr: {result.stderr[:300]}...")
            
            cmd_auto = [
                'yt-dlp',
                '--write-auto-subs',
                '--sub-lang', 'en',
                '--sub-format', 'vtt',
                '--skip-download',
                '--output', f'{temp_dir}/%(title)s.%(ext)s',
                video_url
            ]
            result = subprocess.run(cmd_auto, capture_output=True, text=True, timeout=60)
            
            if result.returncode != 0:
                return {
                    'method': 'yt-dlp',
                    'success': False,
                    'error': f"yt-dlp failed: {result.stderr}",
                    'lines': [],
                    'line_count': 0
                }
        
        # Find VTT files
        vtt_files = glob.glob(f'{temp_dir}/*.{language}.vtt') or glob.glob(f'{temp_dir}/*.en.vtt')
        
        if not vtt_files:
            return {
                'method': 'yt-dlp',
                'success': False,
                'error': f"No VTT files found for language '{language}'",
                'lines': [],
                'line_count': 0
            }
        
        vtt_file = vtt_files[0]
        if debug:
            print(f"📄 Found VTT file: {os.path.basename(vtt_file)}")
        
        # Read and parse VTT content
        with open(vtt_file, 'r', encoding='utf-8') as f:
            vtt_content = f.read()
        
        if debug:
            print(f"📊 VTT file size: {len(vtt_content)} characters")
            # Save raw VTT for inspection
            debug_vtt_path = f"debug_raw_{video_id}.vtt"
            with open(debug_vtt_path, 'w', encoding='utf-8') as f:
                f.write(vtt_content)
            print(f"💾 Saved raw VTT to: {debug_vtt_path}")
        
        # Parse VTT content using the same logic as enhanced_server.py
        lines = vtt_content.split('\n')
        transcript_lines = []
        
        current_timestamp = None
        current_text_lines = []
        
        if debug:
            print(f"🔍 Processing {len(lines)} VTT lines...")
        
        for i, line in enumerate(lines):
            line = line.strip()
            
            # Skip empty lines and VTT headers
            if not line or line.startswith('WEBVTT') or line.startswith('Kind:') or line.startswith('Language:'):
                # If we hit an empty line and have accumulated text, process the cue
                if not line and current_timestamp and current_text_lines:
                    # Join all text lines for this timestamp
                    combined_text = ' '.join(current_text_lines)
                    clean_text = re.sub(r'<[^>]+>', '', combined_text).strip()
                    if clean_text:
                        transcript_lines.append(f"{current_timestamp} {clean_text}")
                        if debug and len(transcript_lines) <= 10:
                            print(f"  📝 Added line {len(transcript_lines)}: {current_timestamp} {clean_text[:50]}...")
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
                        if debug and len(transcript_lines) <= 10:
                            print(f"  📝 Added line {len(transcript_lines)}: {current_timestamp} {clean_text[:50]}...")
                
                # Extract start time for our format
                time_parts = line.split(' --> ')[0]
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
                except (ValueError, IndexError):
                    current_timestamp = "[00:00]"
                
                current_text_lines = []
                continue
            
            # Accumulate text lines for current timestamp
            if current_timestamp:
                current_text_lines.append(line)
        
        # Process any remaining cue at the end of file
        if current_timestamp and current_text_lines:
            combined_text = ' '.join(current_text_lines)
            clean_text = re.sub(r'<[^>]+>', '', combined_text).strip()
            if clean_text:
                transcript_lines.append(f"{current_timestamp} {clean_text}")
                if debug:
                    print(f"  📝 Added final line {len(transcript_lines)}: {current_timestamp} {clean_text[:50]}...")
        
        if debug:
            print(f"✅ Parsed {len(transcript_lines)} transcript lines from VTT")
        
        return {
            'method': 'yt-dlp',
            'success': True,
            'language': language,
            'lines': transcript_lines,
            'line_count': len(transcript_lines),
            'vtt_file_path': vtt_file,
            'vtt_content_preview': vtt_content[:500]
        }
        
    except subprocess.TimeoutExpired:
        return {
            'method': 'yt-dlp',
            'success': False,
            'error': "yt-dlp timed out",
            'lines': [],
            'line_count': 0
        }
    except Exception as e:
        return {
            'method': 'yt-dlp',
            'success': False,
            'error': str(e),
            'lines': [],
            'line_count': 0
        }
    finally:
        # Clean up temporary files
        if temp_dir and os.path.exists(temp_dir):
            try:
                shutil.rmtree(temp_dir)
                if debug:
                    print(f"🧹 Cleaned up temporary directory")
            except:
                if debug:
                    print(f"⚠️  Could not clean up {temp_dir}")


def analyze_duplicates(lines: List[str]) -> Dict[str, Any]:
    """Analyze transcript lines for duplicates with detailed information."""
    seen_lines = {}
    duplicates = []
    line_frequency = {}
    
    for i, line in enumerate(lines):
        # Count frequency
        line_frequency[line] = line_frequency.get(line, 0) + 1
        
        if line in seen_lines:
            duplicates.append({
                'line': line,
                'first_occurrence': seen_lines[line],
                'duplicate_occurrence': i,
                'line_number': i + 1
            })
        else:
            seen_lines[line] = i
    
    # Find lines that appear more than twice
    frequent_lines = {line: count for line, count in line_frequency.items() if count > 2}
    
    return {
        'total_lines': len(lines),
        'unique_lines': len(seen_lines),
        'duplicate_count': len(duplicates),
        'duplicates': duplicates,
        'frequent_lines': frequent_lines,
        'line_frequency': line_frequency
    }


def save_transcript_markdown(result: Dict[str, Any], video_url: str, output_dir: str, video_info: Dict[str, Any] = None) -> str:
    """Save transcript as markdown file optimized for MCP resource usage."""
    try:
        video_id = extract_video_id(video_url)
        title = video_info.get('title', 'Unknown Title') if video_info else f"Video {video_id}"
        
        # Clean title for filename
        safe_title = re.sub(r'[^\w\s-]', '', title).strip()
        safe_title = re.sub(r'[-\s]+', '-', safe_title)[:50]
        
        filename = f"{video_id}_{safe_title}_{result['method'].replace('-', '_')}.md"
        filepath = os.path.join(output_dir, filename)
        
        # Create markdown content optimized for MCP resources
        markdown_content = f"""# {title}

**Video ID:** `{video_id}`  
**URL:** {video_url}  
**Method:** {result['method']}  
**Language:** {result.get('language', 'unknown')}  
**Duration:** {video_info.get('duration_string', 'Unknown')} ({video_info.get('duration', 0)} seconds)  
**Upload Date:** {video_info.get('upload_date', 'Unknown')}  
**Channel:** {video_info.get('uploader', 'Unknown')}  
**View Count:** {video_info.get('view_count', 'Unknown')}  
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## Metadata

```json
{{
  "video_id": "{video_id}",
  "title": "{title}",
  "method": "{result['method']}",
  "language": "{result.get('language', 'unknown')}",
  "line_count": {result['line_count']},
  "generated_at": "{datetime.now().isoformat()}"
}}
```

---

## Available Languages

{', '.join(result.get('available_languages', ['N/A']))}

---

## Transcript

"""
        
        # Add transcript lines
        for line in result['lines']:
            markdown_content += f"{line}\n"
        
        # Add analysis section
        duplicate_analysis = analyze_duplicates(result['lines'])
        markdown_content += f"""

---

## Quality Analysis

- **Total Lines:** {duplicate_analysis['total_lines']}
- **Unique Lines:** {duplicate_analysis['unique_lines']}
- **Duplicate Lines:** {duplicate_analysis['duplicate_count']}
- **Quality Score:** {((duplicate_analysis['unique_lines'] / max(duplicate_analysis['total_lines'], 1)) * 100):.1f}%

"""
        
        if duplicate_analysis['duplicates']:
            markdown_content += "### ⚠️ Duplicate Lines Detected\n\n"
            for i, dup in enumerate(duplicate_analysis['duplicates'][:10], 1):
                markdown_content += f"{i}. **Line {dup['line_number']}:** `{dup['line'][:100]}{'...' if len(dup['line']) > 100 else ''}`\n"
                markdown_content += f"   *(First occurrence: Line {dup['first_occurrence'] + 1})*\n\n"
            
            if len(duplicate_analysis['duplicates']) > 10:
                markdown_content += f"*...and {len(duplicate_analysis['duplicates']) - 10} more duplicates*\n\n"
        
        if duplicate_analysis['frequent_lines']:
            markdown_content += "### 🔁 Frequently Repeated Lines\n\n"
            for line, count in list(duplicate_analysis['frequent_lines'].items())[:5]:
                markdown_content += f"- **{count}x:** `{line[:80]}{'...' if len(line) > 80 else ''}`\n"
        
        # Add MCP resource instructions
        markdown_content += f"""

---

## MCP Resource Usage

This transcript can be used as an MCP resource by referencing:

```
transcript://{video_id}
```

Or for programmatic access:

```python
# Access this transcript in your MCP server
video_id = "{video_id}"
transcript_content = await get_transcript_resource(video_id)
```

### Recommended Use Cases

- **Content Analysis:** Analyze themes, topics, and key points
- **Quote Extraction:** Find specific quotes or statements  
- **Study Notes:** Generate structured notes from educational content
- **Search & Reference:** Search within transcript content
- **Summarization:** Create summaries and abstracts

---

*Generated by YouTube Transcript CLI Tool v1.0*
"""
        
        # Save file
        os.makedirs(output_dir, exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        return filepath
        
    except Exception as e:
        print(f"❌ Error saving markdown: {e}")
        return ""


def main():
    parser = argparse.ArgumentParser(
        description="Advanced YouTube Transcript Extraction and Analysis Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Extract using both methods and compare
  python transcript_cli.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
  
  # Use only yt-dlp with detailed debugging
  python transcript_cli.py "https://youtu.be/dQw4w9WgXcQ" --method ytdlp --debug
  
  # Extract and save to specific directory
  python transcript_cli.py "https://youtu.be/dQw4w9WgXcQ" --output ./mcp_resources
  
  # Extract multiple videos
  python transcript_cli.py "https://youtu.be/dQw4w9WgXcQ" "https://youtu.be/oHg5SJYRHA0" --method both
        """
    )
    
    parser.add_argument('video_urls', nargs='+', help='YouTube video URLs')
    parser.add_argument('--method', choices=['api', 'ytdlp', 'both'], default='both',
                        help='Extraction method (default: both)')
    parser.add_argument('--lang', default='en', help='Language code (default: en)')
    parser.add_argument('--output', default='./mcp_transcripts', 
                        help='Output directory for markdown files (default: ./mcp_transcripts)')
    parser.add_argument('--debug', action='store_true', help='Enable detailed debugging output')
    parser.add_argument('--compare', action='store_true', help='Compare results when using both methods')
    
    args = parser.parse_args()
    
    print(f"🚀 Advanced YouTube Transcript Extraction Tool")
    print(f"=" * 60)
    print(f"Videos: {len(args.video_urls)}")
    print(f"Method: {args.method}")
    print(f"Language: {args.lang}")
    print(f"Output: {args.output}")
    print(f"Debug: {args.debug}")
    print()
    
    total_successes = 0
    total_failures = 0
    
    for i, video_url in enumerate(args.video_urls, 1):
        print(f"\n{'='*60}")
        print(f"🎥 Processing Video {i}/{len(args.video_urls)}")
        print(f"URL: {video_url}")
        print(f"{'='*60}")
        
        # Get video info
        video_info = get_video_info_ytdlp(video_url)
        if video_info:
            print(f"📺 Title: {video_info.get('title', 'Unknown')}")
            print(f"📅 Duration: {video_info.get('duration_string', 'Unknown')}")
            print(f"👤 Channel: {video_info.get('uploader', 'Unknown')}")
        
        results = []
        
        # Extract using API method
        if args.method in ['api', 'both']:
            print(f"\n📡 Testing youtube-transcript-api method...")
            api_result = extract_transcript_api(video_url, args.lang)
            results.append(api_result)
            
            if api_result['success']:
                print(f"✅ API method successful: {api_result['line_count']} lines")
                duplicate_analysis = analyze_duplicates(api_result['lines'])
                if duplicate_analysis['duplicate_count'] > 0:
                    print(f"⚠️  Found {duplicate_analysis['duplicate_count']} duplicate lines!")
                    if args.debug:
                        for dup in duplicate_analysis['duplicates'][:3]:
                            print(f"   Line {dup['line_number']}: {dup['line'][:60]}...")
                else:
                    print(f"✅ No duplicates found")
                
                # Save markdown
                filepath = save_transcript_markdown(api_result, video_url, args.output, video_info)
                if filepath:
                    print(f"💾 Saved: {os.path.basename(filepath)}")
                    total_successes += 1
            else:
                print(f"❌ API method failed: {api_result['error']}")
                total_failures += 1
        
        # Extract using yt-dlp method
        if args.method in ['ytdlp', 'both']:
            print(f"\n🛠️  Testing yt-dlp method...")
            ytdlp_result = extract_transcript_ytdlp(video_url, args.lang, args.debug)
            results.append(ytdlp_result)
            
            if ytdlp_result['success']:
                print(f"✅ yt-dlp method successful: {ytdlp_result['line_count']} lines")
                duplicate_analysis = analyze_duplicates(ytdlp_result['lines'])
                if duplicate_analysis['duplicate_count'] > 0:
                    print(f"⚠️  Found {duplicate_analysis['duplicate_count']} duplicate lines!")
                    if args.debug:
                        print("🔍 Duplicate details:")
                        for dup in duplicate_analysis['duplicates'][:5]:
                            print(f"   Line {dup['line_number']}: {dup['line'][:60]}...")
                else:
                    print(f"✅ No duplicates found")
                
                # Save markdown
                filepath = save_transcript_markdown(ytdlp_result, video_url, args.output, video_info)
                if filepath:
                    print(f"💾 Saved: {os.path.basename(filepath)}")
                    total_successes += 1
            else:
                print(f"❌ yt-dlp method failed: {ytdlp_result['error']}")
                total_failures += 1
        
        # Compare results if both methods were used
        if len(results) == 2 and all(r['success'] for r in results) and args.compare:
            print(f"\n🔍 Comparison Analysis")
            print(f"-" * 30)
            
            api_lines = set(results[0]['lines'])
            ytdlp_lines = set(results[1]['lines'])
            
            print(f"API lines: {len(api_lines)}")
            print(f"yt-dlp lines: {len(ytdlp_lines)}")
            print(f"Common lines: {len(api_lines.intersection(ytdlp_lines))}")
            print(f"API only: {len(api_lines - ytdlp_lines)}")
            print(f"yt-dlp only: {len(ytdlp_lines - api_lines)}")
            
            similarity = len(api_lines.intersection(ytdlp_lines)) / len(api_lines.union(ytdlp_lines)) * 100
            print(f"Similarity: {similarity:.1f}%")
            
            if similarity < 95:
                print("⚠️  Methods produced significantly different results!")
                
                if args.debug:
                    api_only = list(api_lines - ytdlp_lines)[:3]
                    ytdlp_only = list(ytdlp_lines - api_lines)[:3]
                    
                    if api_only:
                        print("\n📋 Sample API-only lines:")
                        for line in api_only:
                            print(f"   {line[:80]}...")
                    
                    if ytdlp_only:
                        print("\n📋 Sample yt-dlp-only lines:")
                        for line in ytdlp_only:
                            print(f"   {line[:80]}...")
            else:
                print("✅ Both methods produced very similar results!")
    
    print(f"\n" + "="*60)
    print(f"🎉 Processing Complete!")
    print(f"✅ Successful extractions: {total_successes}")
    print(f"❌ Failed extractions: {total_failures}")
    print(f"📁 Output directory: {args.output}")
    print(f"📝 Ready for MCP resource integration")
    print(f"="*60)


if __name__ == "__main__":
    main()
