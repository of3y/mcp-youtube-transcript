#!/usr/bin/env python3
"""
Dedicated YouTube Transcript Extractor

This script extracts YouTube transcripts using both the youtube-transcript-api 
and yt-dlp methods, saves them as markdown files, and helps investigate 
duplicate line issues.

Usage:
    python transcript_extractor.py <youtube_url> [--method ytdlp|api|both] [--lang en] [--output dir]
"""

import os
import sys
import argparse
import asyncio
import re
import subprocess
import glob
import tempfile
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

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


def get_video_title_ytdlp(video_url: str) -> str:
    """Get video title using yt-dlp."""
    try:
        cmd = ['yt-dlp', '--get-title', video_url]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            return result.stdout.strip()
    except:
        pass
    return "Unknown Title"


async def extract_transcript_api(video_url: str, language: str = "en") -> Dict[str, Any]:
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
            'raw_data': transcript_data
        }
        
    except Exception as e:
        return {
            'method': 'youtube-transcript-api',
            'success': False,
            'error': str(e),
            'lines': [],
            'line_count': 0
        }


async def extract_transcript_ytdlp(video_url: str, language: str = "en") -> Dict[str, Any]:
    """Extract transcript using yt-dlp."""
    print(f"🔍 Extracting transcript using yt-dlp...")
    
    temp_dir = None
    try:
        video_id = extract_video_id(video_url)
        
        # Create temporary directory for downloads
        temp_dir = tempfile.mkdtemp(prefix="ytdlp_transcript_")
        
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
        
        print(f"🚀 Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode != 0:
            print(f"⚠️  First attempt failed, trying auto-generated subtitles only...")
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
        print(f"📄 Found VTT file: {os.path.basename(vtt_file)}")
        
        # Read and parse VTT content
        with open(vtt_file, 'r', encoding='utf-8') as f:
            vtt_content = f.read()
        
        # Parse VTT content with detailed debugging
        print(f"📊 VTT file size: {len(vtt_content)} characters")
        
        lines = vtt_content.split('\n')
        transcript_lines = []
        
        current_timestamp = None
        current_text_lines = []
        
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
                print(f"  📝 Added final line {len(transcript_lines)}: {current_timestamp} {clean_text[:50]}...")
        
        print(f"✅ Parsed {len(transcript_lines)} transcript lines from VTT")
        
        return {
            'method': 'yt-dlp',
            'success': True,
            'language': language,
            'lines': transcript_lines,
            'line_count': len(transcript_lines),
            'vtt_file': vtt_file,
            'vtt_content': vtt_content
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
            import shutil
            try:
                shutil.rmtree(temp_dir)
                print(f"🧹 Cleaned up temporary directory")
            except:
                print(f"⚠️  Could not clean up {temp_dir}")


def analyze_duplicates(lines: List[str]) -> Dict[str, Any]:
    """Analyze transcript lines for duplicates."""
    seen_lines = {}
    duplicates = []
    
    for i, line in enumerate(lines):
        if line in seen_lines:
            duplicates.append({
                'line': line,
                'first_occurrence': seen_lines[line],
                'duplicate_occurrence': i
            })
        else:
            seen_lines[line] = i
    
    return {
        'total_lines': len(lines),
        'unique_lines': len(seen_lines),
        'duplicate_count': len(duplicates),
        'duplicates': duplicates
    }


def save_transcript_markdown(result: Dict[str, Any], video_url: str, output_dir: str) -> str:
    """Save transcript as markdown file."""
    try:
        video_id = extract_video_id(video_url)
        title = get_video_title_ytdlp(video_url)
        
        # Clean title for filename
        safe_title = re.sub(r'[^\w\s-]', '', title).strip()
        safe_title = re.sub(r'[-\s]+', '-', safe_title)[:50]
        
        filename = f"{video_id}_{safe_title}_{result['method'].replace('-', '_')}.md"
        filepath = os.path.join(output_dir, filename)
        
        # Create markdown content
        markdown_content = f"""# YouTube Transcript: {title}

**Video URL:** {video_url}  
**Video ID:** {video_id}  
**Extraction Method:** {result['method']}  
**Language:** {result.get('language', 'unknown')}  
**Lines:** {result['line_count']}  
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## Available Languages
{', '.join(result.get('available_languages', ['N/A']))}

---

## Transcript

"""
        
        for line in result['lines']:
            markdown_content += f"{line}\n"
        
        # Add analysis section
        duplicate_analysis = analyze_duplicates(result['lines'])
        markdown_content += f"""

---

## Analysis

- **Total Lines:** {duplicate_analysis['total_lines']}
- **Unique Lines:** {duplicate_analysis['unique_lines']}
- **Duplicates:** {duplicate_analysis['duplicate_count']}

"""
        
        if duplicate_analysis['duplicates']:
            markdown_content += "### Duplicate Lines Found:\n\n"
            for dup in duplicate_analysis['duplicates']:
                markdown_content += f"- Line {dup['duplicate_occurrence']}: `{dup['line'][:100]}...`\n"
                markdown_content += f"  (First seen at line {dup['first_occurrence']})\n\n"
        
        # Save file
        os.makedirs(output_dir, exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        return filepath
        
    except Exception as e:
        print(f"❌ Error saving markdown: {e}")
        return ""


async def main():
    parser = argparse.ArgumentParser(
        description="Extract YouTube transcripts and investigate duplicate issues",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python transcript_extractor.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
  python transcript_extractor.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --method ytdlp
  python transcript_extractor.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --method both --output ./transcripts
        """
    )
    
    parser.add_argument('video_url', help='YouTube video URL')
    parser.add_argument('--method', choices=['api', 'ytdlp', 'both'], default='both',
                        help='Extraction method (default: both)')
    parser.add_argument('--lang', default='en', help='Language code (default: en)')
    parser.add_argument('--output', default='./transcripts', 
                        help='Output directory for markdown files (default: ./transcripts)')
    
    args = parser.parse_args()
    
    print(f"🚀 YouTube Transcript Extractor")
    print(f"=" * 50)
    print(f"Video URL: {args.video_url}")
    print(f"Method: {args.method}")
    print(f"Language: {args.lang}")
    print(f"Output: {args.output}")
    print()
    
    results = []
    
    # Extract using API method
    if args.method in ['api', 'both']:
        print(f"📡 Testing youtube-transcript-api method...")
        api_result = await extract_transcript_api(args.video_url, args.lang)
        results.append(api_result)
        
        if api_result['success']:
            print(f"✅ API method successful: {api_result['line_count']} lines")
            duplicate_analysis = analyze_duplicates(api_result['lines'])
            if duplicate_analysis['duplicate_count'] > 0:
                print(f"⚠️  Found {duplicate_analysis['duplicate_count']} duplicate lines!")
            else:
                print(f"✅ No duplicates found")
            
            # Save markdown
            filepath = save_transcript_markdown(api_result, args.video_url, args.output)
            if filepath:
                print(f"💾 Saved: {filepath}")
        else:
            print(f"❌ API method failed: {api_result['error']}")
        print()
    
    # Extract using yt-dlp method
    if args.method in ['ytdlp', 'both']:
        print(f"🛠️  Testing yt-dlp method...")
        ytdlp_result = await extract_transcript_ytdlp(args.video_url, args.lang)
        results.append(ytdlp_result)
        
        if ytdlp_result['success']:
            print(f"✅ yt-dlp method successful: {ytdlp_result['line_count']} lines")
            duplicate_analysis = analyze_duplicates(ytdlp_result['lines'])
            if duplicate_analysis['duplicate_count'] > 0:
                print(f"⚠️  Found {duplicate_analysis['duplicate_count']} duplicate lines!")
                print("🔍 Duplicate details:")
                for dup in duplicate_analysis['duplicates'][:5]:  # Show first 5
                    print(f"   Line {dup['duplicate_occurrence']}: {dup['line'][:80]}...")
            else:
                print(f"✅ No duplicates found")
            
            # Save markdown
            filepath = save_transcript_markdown(ytdlp_result, args.video_url, args.output)
            if filepath:
                print(f"💾 Saved: {filepath}")
        else:
            print(f"❌ yt-dlp method failed: {ytdlp_result['error']}")
        print()
    
    # Compare results if both methods were used
    if len(results) == 2 and all(r['success'] for r in results):
        print(f"🔍 Comparison Analysis")
        print(f"-" * 30)
        
        api_lines = set(results[0]['lines'])
        ytdlp_lines = set(results[1]['lines'])
        
        print(f"API lines: {len(api_lines)}")
        print(f"yt-dlp lines: {len(ytdlp_lines)}")
        print(f"Common lines: {len(api_lines.intersection(ytdlp_lines))}")
        print(f"API only: {len(api_lines - ytdlp_lines)}")
        print(f"yt-dlp only: {len(ytdlp_lines - api_lines)}")
        
        if api_lines != ytdlp_lines:
            print("⚠️  Methods produced different results!")
            
            # Show some differences
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
            print("✅ Both methods produced identical results!")
    
    print(f"\n" + "=" * 50)
    print(f"🎉 Transcript extraction complete!")
    print(f"📁 Check output directory: {args.output}")


if __name__ == "__main__":
    asyncio.run(main())
