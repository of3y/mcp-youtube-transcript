"""
Shared transcript extraction and processing functions.

This module provides advanced transcript extraction, deduplication, quality analysis,
and markdown generation capabilities shared between the MCP server and standalone CLI.
"""

import re
import json
import subprocess
import tempfile
import shutil
import os
import glob
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
import html

# Import configuration
from .config import settings

# Note: youtube-transcript-api removed due to cloud server blocking issues
# This module now uses only yt-dlp for reliable transcript extraction


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


def check_ytdlp_available() -> bool:
    """Check if yt-dlp is available."""
    try:
        subprocess.run(['yt-dlp', '--version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


async def get_video_metadata(video_url: str) -> Dict[str, Any]:
    """Get comprehensive video metadata using yt-dlp."""
    if not check_ytdlp_available():
        return {}
    
    try:
        cmd = ['yt-dlp', '--dump-json', '--no-download', video_url]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            return json.loads(result.stdout)
    except Exception as e:
        print(f"⚠️  Could not get video metadata: {e}")
    return {}


async def extract_transcript_api(video_url: str, language: str = "en") -> Dict[str, Any]:
    """Extract transcript using youtube-transcript-api - DEPRECATED.
    
    This method has been removed due to cloud server blocking issues.
    Use extract_transcript_ytdlp instead.
    """
    return {
        'method': 'youtube-transcript-api',
        'success': False,
        'error': 'youtube-transcript-api method deprecated - use yt-dlp instead',
        'lines': [],
        'line_count': 0,
        'available_languages': []
    }


async def extract_transcript_ytdlp(video_url: str, language: str = "en") -> Dict[str, Any]:
    """Extract transcript using yt-dlp with SRV1 format preference and automatic fallback.
    
    This updated version uses the improved format chain: srv1 → json3 → ttml → vtt
    to eliminate the VTT duplication issue discovered in the analysis.
    """
    if not check_ytdlp_available():
        return {
            'method': 'yt-dlp',
            'success': False,
            'error': 'yt-dlp not available - install with: pip install yt-dlp',
            'lines': [],
            'line_count': 0
        }
    
    temp_dir = None
    try:
        # Create temporary directory
        temp_dir = tempfile.mkdtemp(prefix="ytdlp_mcp_")
        
        # Use new fallback system instead of hardcoded VTT
        subtitle_file, actual_format = download_subtitles_with_fallback(video_url, language, temp_dir)
        
        # Parse using the appropriate parser
        transcript_lines = parse_subtitle_file(subtitle_file, actual_format)
        
        # Apply deduplication (mainly needed for VTT fallback)
        if actual_format == 'vtt':
            transcript_lines = deduplicate_transcript_lines(transcript_lines)
        
        return {
            'method': 'yt-dlp',
            'success': True,
            'format': actual_format,  # Report which format was actually used
            'language': language,
            'lines': transcript_lines,
            'line_count': len(transcript_lines)
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
        # Clean up
        if temp_dir and os.path.exists(temp_dir):
            try:
                shutil.rmtree(temp_dir)
            except:
                pass


def parse_vtt_content(vtt_content: str) -> List[str]:
    """Parse VTT content and extract timestamped lines."""
    lines = []
    vtt_lines = vtt_content.split('\n')
    
    current_timestamp = ""
    current_text = ""
    
    for line in vtt_lines:
        line = line.strip()
        
        # Skip VTT headers and empty lines
        if not line or line.startswith('WEBVTT') or line.startswith('NOTE'):
            continue
        
        # Timestamp line format: 00:00:01.000 --> 00:00:03.000
        if '-->' in line:
            # Extract start timestamp
            start_time = line.split('-->')[0].strip()
            # Convert to [MM:SS] format
            if ':' in start_time:
                time_parts = start_time.split(':')
                if len(time_parts) >= 2:
                    minutes = int(float(time_parts[-2]))
                    seconds = int(float(time_parts[-1].split('.')[0]))
                    current_timestamp = f"[{minutes:02d}:{seconds:02d}]"
        
        # Text line
        elif line and not line.isdigit():
            # Clean HTML tags and decode entities
            clean_text = re.sub(r'<[^>]+>', '', line)
            clean_text = html.unescape(clean_text)
            
            if clean_text.strip() and current_timestamp:
                lines.append(f"{current_timestamp} {clean_text.strip()}")
                current_timestamp = ""  # Reset after use
    
    return lines


def deduplicate_transcript_lines(lines: List[str]) -> List[str]:
    """Remove duplicate consecutive text while preserving timestamps.
    
    This fixes the common issue where YouTube auto-captions repeat the same text
    across multiple timestamps as speech continues.
    """
    if not lines:
        return lines
    
    deduplicated = []
    last_clean_text = ""
    last_words = set()
    
    for line in lines:
        # Extract timestamp and text
        if line.startswith('[') and ']' in line:
            timestamp_end = line.find(']') + 1
            timestamp = line[:timestamp_end]
            text = line[timestamp_end:].strip()
        else:
            timestamp = ""
            text = line.strip()
        
        if not text or text in ['[Music]', '[Applause]', '[Laughter]']:
            continue
            
        # Clean text for comparison (remove extra spaces, normalize)
        clean_text = ' '.join(text.split()).lower()
        
        # Skip if this is an exact duplicate of the last line
        if clean_text == last_clean_text:
            continue
            
        # Skip if this text is completely contained in the last text
        if last_clean_text and clean_text in last_clean_text and last_clean_text not in ['[Music]', '[Applause]', '[Laughter]']:
            continue
            
        # Skip if the last text is completely contained in this text
        # but this text is much longer (likely an extension)
        if last_clean_text and last_clean_text in clean_text:
            if len(clean_text) > len(last_clean_text) * 1.2:
                # Replace the last entry with this longer version
                if deduplicated:
                    deduplicated[-1] = line
                    last_clean_text = clean_text
                    last_words = set(clean_text.split())
                    continue
        
        # Advanced duplicate detection: check word overlap
        current_words = set(clean_text.split())
        if last_words and len(current_words) > 3:
            # Calculate overlap percentage
            overlap = len(current_words.intersection(last_words))
            overlap_percentage = overlap / min(len(current_words), len(last_words))
            
            # If more than 80% word overlap and similar length, skip
            if (overlap_percentage > 0.8 and 
                abs(len(current_words) - len(last_words)) <= 2):
                continue
        
        deduplicated.append(line)
        last_clean_text = clean_text
        last_words = current_words
    
    return deduplicated


def create_plain_text_script(lines: List[str], remove_duplicates: bool = True, aggressive_dedup: bool = False) -> str:
    """Create a clean plain text script from timestamped transcript lines.
    
    Args:
        lines: List of transcript lines with timestamps
        remove_duplicates: Whether to remove consecutive duplicate text
        aggressive_dedup: Whether to use aggressive deduplication (removes more potential duplicates)
        
    Returns:
        Clean plain text script without timestamps
    """
    if not lines:
        return ""
    
    # First, deduplicate if requested
    working_lines = deduplicate_transcript_lines(lines) if remove_duplicates else lines
    
    # Extract just the text parts and clean them
    text_parts = []
    last_text = ""
    
    for line in working_lines:
        # Extract text from timestamped line
        if line.startswith('[') and ']' in line:
            timestamp_end = line.find(']') + 1
            text = line[timestamp_end:].strip()
        else:
            text = line.strip()
        
        if not text or text in ['[Music]', '[Applause]', '[Laughter]']:
            continue
        
        # Aggressive deduplication for script generation
        if aggressive_dedup and last_text:
            # Skip if this text has significant overlap with previous
            current_words = set(text.lower().split())
            last_words = set(last_text.lower().split())
            
            if len(current_words) > 2 and len(last_words) > 2:
                overlap = len(current_words.intersection(last_words))
                overlap_percentage = overlap / min(len(current_words), len(last_words))
                
                # Skip if more than 60% overlap
                if overlap_percentage > 0.6:
                    continue
        
        text_parts.append(text)
        last_text = text
    
    # Join all text parts with proper spacing
    full_text = ' '.join(text_parts)
    
    # Clean up extra spaces and normalize
    full_text = re.sub(r'\s+', ' ', full_text).strip()
    
    # Fix common spacing issues from overlapping captions
    full_text = re.sub(r'(\w+)\s+\1\b', r'\1', full_text)  # Remove repeated words
    full_text = re.sub(r'\s+', ' ', full_text).strip()  # Clean up again
    
    # Split into sentences and create natural paragraphs
    sentences = re.split(r'(?<=[.!?])\s+', full_text)
    
    # Group sentences into coherent paragraphs
    paragraphs = []
    current_paragraph = []
    
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        
        current_paragraph.append(sentence)
        
        # End paragraph conditions
        paragraph_text = ' '.join(current_paragraph)
        
        if ((len(current_paragraph) >= 2 and sentence.endswith(('.', '!', '?'))) or
            len(paragraph_text) > 300 or
            any(phrase in sentence.lower() for phrase in [
                'so let me', 'now let me', 'so basically', 'now i want to',
                'let me show you', 'so the idea', 'so what we have'
            ])):
            
            if len(paragraph_text) > 50:  # Only keep substantial paragraphs
                paragraphs.append(paragraph_text)
            current_paragraph = []
    
    # Add any remaining sentences
    if current_paragraph:
        paragraph_text = ' '.join(current_paragraph)
        if len(paragraph_text.strip()) > 50:
            paragraphs.append(paragraph_text)
    
    return '\n\n'.join(paragraphs)


def analyze_transcript_quality(lines: List[str]) -> Dict[str, Any]:
    """Analyze the quality of a transcript and provide detailed metrics."""
    if not lines:
        return {'error': 'No lines to analyze'}
    
    # Basic metrics
    total_lines = len(lines)
    
    # Extract text content
    text_lines = []
    for line in lines:
        if line.startswith('[') and ']' in line:
            timestamp_end = line.find(']') + 1
            text = line[timestamp_end:].strip()
        else:
            text = line.strip()
        
        if text and text not in ['[Music]', '[Applause]', '[Laughter]']:
            text_lines.append(text)
    
    # Duplicate analysis
    exact_duplicates = 0
    partial_duplicates = 0
    seen_texts = set()
    
    for text in text_lines:
        clean_text = ' '.join(text.split()).lower()
        if clean_text in seen_texts:
            exact_duplicates += 1
        else:
            # Check for partial duplicates
            for seen_text in seen_texts:
                if (clean_text in seen_text or seen_text in clean_text) and clean_text != seen_text:
                    partial_duplicates += 1
                    break
            seen_texts.add(clean_text)
    
    # After deduplication metrics
    deduplicated = deduplicate_transcript_lines(lines)
    dedupe_reduction = ((total_lines - len(deduplicated)) / total_lines * 100) if total_lines > 0 else 0
    
    # Text quality metrics
    total_words = sum(len(text.split()) for text in text_lines)
    avg_words_per_line = total_words / len(text_lines) if text_lines else 0
    
    # Calculate quality score
    duplicate_penalty = (exact_duplicates + partial_duplicates) / total_lines * 100 if total_lines > 0 else 0
    quality_score = max(0, 100 - duplicate_penalty)
    
    return {
        'total_lines': total_lines,
        'text_lines': len(text_lines),
        'exact_duplicates': exact_duplicates,
        'partial_duplicates': partial_duplicates,
        'total_words': total_words,
        'avg_words_per_line': round(avg_words_per_line, 1),
        'deduplicated_lines': len(deduplicated),
        'reduction_percentage': round(dedupe_reduction, 1),
        'quality_score': round(quality_score, 1),
        'quality_rating': 'Excellent' if quality_score >= 90 else 
                         'Good' if quality_score >= 70 else 
                         'Fair' if quality_score >= 50 else 'Poor'
    }


def create_mcp_markdown(result: Dict[str, Any], video_url: str, metadata: Dict[str, Any]) -> str:
    """Create markdown content optimized for MCP resource usage."""
    video_id = extract_video_id(video_url)
    title = metadata.get('title', f'Video {video_id}')
    
    # Create clean markdown content
    markdown_content = f"""# {title}

## Video Information

- **Video ID:** `{video_id}`
- **URL:** {video_url}
- **Title:** {title}
- **Channel:** {metadata.get('uploader', 'Unknown')}
- **Duration:** {metadata.get('duration_string', 'Unknown')} ({metadata.get('duration', 0)} seconds)
- **Upload Date:** {metadata.get('upload_date', 'Unknown')}
- **View Count:** {metadata.get('view_count', 'Unknown'):,} views

## Transcript Metadata

- **Extraction Method:** {result['method']}
- **Language:** {result.get('language', 'unknown')}
- **Line Count:** {result['line_count']}
- **Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Available Languages

{', '.join(result.get('available_languages', ['N/A']))}

## Plain Text Script

"""
    
    # Generate clean plain text script with aggressive deduplication
    plain_script = create_plain_text_script(result['lines'], remove_duplicates=True, aggressive_dedup=True)
    markdown_content += plain_script
    
    markdown_content += f"""

## Timestamped Transcript

"""
    
    # Add original transcript lines with timestamps
    for line in result['lines']:
        # Clean up HTML entities for better readability
        clean_line = html.unescape(line)
        markdown_content += f"{clean_line}\n"
    
    # Add quality analysis
    quality_analysis = analyze_transcript_quality(result['lines'])
    
    markdown_content += f"""

## Quality Analysis

- **Total Lines:** {quality_analysis['total_lines']}
- **Unique Lines:** {quality_analysis['deduplicated_lines']}
- **Duplicate Lines:** {quality_analysis['exact_duplicates']}
- **Quality Score:** {quality_analysis['quality_score']}%
- **Quality Rating:** {quality_analysis['quality_rating']}

"""
    
    if quality_analysis['exact_duplicates'] > 0:
        markdown_content += f"### ⚠️ Quality Issues\n\n"
        markdown_content += f"Found {quality_analysis['exact_duplicates']} duplicate lines. "
        markdown_content += f"Reduction after deduplication: {quality_analysis['reduction_percentage']}%\n\n"
    else:
        markdown_content += "### ✅ High Quality Transcript\n\nNo duplicate lines detected.\n\n"
    
    # Add MCP usage instructions
    markdown_content += f"""

## MCP Resource Usage

This transcript can be used as an MCP resource:

### Resource URI
```
transcript://{video_id}
```

### Programmatic Access
```python
# In your MCP server
async def get_transcript(video_id: str):
    return await load_transcript_resource(video_id)
```

### Use Cases
- **Content Analysis:** Analyze themes, topics, and sentiment
- **Quote Extraction:** Find specific quotes or statements  
- **Study Notes:** Generate structured educational notes
- **Search & Discovery:** Full-text search within video content
- **Summarization:** Create abstracts and key points
- **Fact Checking:** Verify claims and statements

---

*Generated by YouTube to MCP Resource Tool v1.0*  
*For more information: https://github.com/your-repo/mcp-youtube-transcript*
"""
    
    return markdown_content


async def extract_enhanced_transcript(video_url: str, language: str = "en", quality_analysis: bool = True) -> Dict[str, Any]:
    """Extract transcript with full enhancement pipeline.
    
    This is the main function that combines all advanced features:
    - Multiple extraction methods with fallbacks
    - Advanced deduplication
    - Quality analysis
    - Rich metadata extraction
    - Comprehensive formatting
    """
    try:
        # Get video metadata first
        metadata = await get_video_metadata(video_url)
        
        # Try youtube-transcript-api first
        result = await extract_transcript_api(video_url, language)
        
        if not result['success']:
            # Fallback to yt-dlp
            result = await extract_transcript_ytdlp(video_url, language)
        
        if not result['success']:
            return {
                'success': False,
                'error': f"Failed to extract transcript: {result.get('error', 'Unknown error')}",
                'video_url': video_url,
                'video_id': extract_video_id(video_url)
            }
        
        # Apply deduplication
        deduplicated_lines = deduplicate_transcript_lines(result['lines'])
        
        # Create plain text version
        plain_text = create_plain_text_script(result['lines'], remove_duplicates=True, aggressive_dedup=True)
        
        # Analyze quality if requested
        quality_metrics = analyze_transcript_quality(result['lines']) if quality_analysis else {}
        
        # Create comprehensive markdown
        markdown_content = create_mcp_markdown(result, video_url, metadata)
        
        return {
            'success': True,
            'video_id': extract_video_id(video_url),
            'video_url': video_url,
            'method': result['method'],
            'language': result.get('language', language),
            'raw_lines': result['lines'],
            'deduplicated_lines': deduplicated_lines,
            'plain_text': plain_text,
            'markdown_content': markdown_content,
            'metadata': metadata,
            'quality_metrics': quality_metrics,
            'line_count': len(result['lines']),
            'deduplicated_count': len(deduplicated_lines),
            'available_languages': result.get('available_languages', [])
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'video_url': video_url,
            'video_id': extract_video_id(video_url) if video_url else 'unknown'
        }


# ============================================================================
# SUBTITLE FORMAT PARSERS
# ============================================================================

def parse_srv1_content(srv1_file_path: str) -> List[str]:
    """Parse SRV1 (XML) subtitle file and return timestamped transcript lines."""
    import xml.etree.ElementTree as ET
    
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


def download_subtitles_with_fallback(video_url: str, language: str = "en", temp_dir: Optional[str] = None) -> tuple[str, str]:
    """Download subtitles with format fallback chain: srv1 → json3 → ttml → vtt."""
    formats = ['srv1', 'json3', 'ttml', 'vtt']  # Order by quality
    
    for fmt in formats:
        cmd = [
            'yt-dlp',
            '--write-auto-subs',
            '--write-subs', 
            '--sub-lang', language,
            '--sub-format', fmt,
            '--skip-download',
            '--output', f'{temp_dir}/%(title)s.%(ext)s',
            video_url
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                # Check if files were actually created
                subtitle_files = glob.glob(f'{temp_dir}/*.{language}.{fmt}') or glob.glob(f'{temp_dir}/*.en.{fmt}')
                if subtitle_files:
                    return subtitle_files[0], fmt
        except subprocess.TimeoutExpired:
            continue
        except Exception:
            continue
    
    raise Exception("No subtitle formats available")


def parse_subtitle_file(file_path: str, format_type: str) -> List[str]:
    """Parse subtitle file based on format type."""
    if format_type == 'srv1':
        return parse_srv1_content(file_path)
    elif format_type == 'json3':
        return parse_json3_content(file_path)
    elif format_type == 'ttml':
        # For now, fallback to VTT parsing logic for TTML
        return parse_vtt_content_legacy(file_path)
    elif format_type == 'vtt':
        return parse_vtt_content_legacy(file_path)
    else:
        raise ValueError(f"Unsupported subtitle format: {format_type}")


def parse_vtt_content_legacy(vtt_file_path: str) -> List[str]:
    """Legacy VTT parser for fallback compatibility."""
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
            
            # Extract start time
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
        
        # Accumulate text lines
        if current_timestamp:
            current_text_lines.append(line)
    
    # Process final cue
    if current_timestamp and current_text_lines:
        combined_text = ' '.join(current_text_lines)
        clean_text = re.sub(r'<[^>]+>', '', combined_text).strip()
        if clean_text:
            transcript_lines.append(f"{current_timestamp} {clean_text}")
    
    return transcript_lines
