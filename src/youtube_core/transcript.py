"""
YouTube transcript extraction using yt-dlp.

Provides robust transcript extraction with:
- Multi-format fallback (srv1 → json3 → ttml → vtt)
- Advanced deduplication
- Quality analysis
- HTML entity decoding
"""

import re
import json
import subprocess
import tempfile
import shutil
import glob
import html
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime


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


def get_video_metadata(video_url: str, timeout: int = 30) -> Dict[str, Any]:
    """Get comprehensive video metadata using yt-dlp."""
    if not check_ytdlp_available():
        return {}

    try:
        cmd = ['yt-dlp', '--dump-json', '--no-download', video_url]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)

        if result.returncode == 0:
            metadata = json.loads(result.stdout)
            return metadata
        else:
            print(f"⚠️  Metadata extraction failed: {result.stderr}")
            return {}

    except subprocess.TimeoutExpired:
        print(f"⚠️  Metadata extraction timed out after {timeout} seconds")
        return {}
    except json.JSONDecodeError as e:
        print(f"⚠️  Failed to parse metadata JSON: {e}")
        return {}
    except Exception as e:
        print(f"⚠️  Could not get video metadata: {e}")
        return {}


def download_subtitles_with_fallback(
    video_url: str,
    language: str = "en",
    temp_dir: Optional[str] = None,
    timeout: int = 60
) -> tuple[str, str]:
    """
    Download subtitles with format fallback chain: srv1 → json3 → ttml → vtt.

    Args:
        video_url: YouTube video URL
        language: Language code (default: en)
        temp_dir: Temporary directory for downloads
        timeout: Command timeout in seconds

    Returns:
        Tuple of (file_path, format) for the downloaded subtitle file
    """
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
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)

            if result.returncode == 0:
                # Check if files were actually created
                subtitle_files = (
                    glob.glob(f'{temp_dir}/*.{language}.{fmt}') or
                    glob.glob(f'{temp_dir}/*.en.{fmt}')
                )
                if subtitle_files:
                    return subtitle_files[0], fmt

        except subprocess.TimeoutExpired:
            continue
        except Exception:
            continue

    raise Exception(f"No subtitle formats available for language: {language}")


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
                clean_text = html.unescape(clean_text)
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
                clean_text = html.unescape(clean_text)
                if clean_text:
                    transcript_lines.append(f"{timestamp} {clean_text}")

    return transcript_lines


def parse_vtt_content(vtt_file_path: str) -> List[str]:
    """Parse VTT subtitle file and return timestamped transcript lines."""
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
                clean_text = html.unescape(clean_text)
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
                clean_text = html.unescape(clean_text)
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
        clean_text = html.unescape(clean_text)
        if clean_text:
            transcript_lines.append(f"{current_timestamp} {clean_text}")

    return transcript_lines


def parse_subtitle_file(file_path: str, format_type: str) -> List[str]:
    """Parse subtitle file based on format type."""
    if format_type == 'srv1':
        return parse_srv1_content(file_path)
    elif format_type == 'json3':
        return parse_json3_content(file_path)
    elif format_type == 'ttml':
        # TTML uses similar structure to VTT
        return parse_vtt_content(file_path)
    elif format_type == 'vtt':
        return parse_vtt_content(file_path)
    else:
        raise ValueError(f"Unsupported subtitle format: {format_type}")


def deduplicate_transcript_lines(lines: List[str]) -> List[str]:
    """
    Remove duplicate consecutive text while preserving timestamps.

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


def extract_transcript(
    video_url: str,
    language: str = "en",
    metadata: Optional[Dict[str, Any]] = None,
    timeout: int = 60
) -> Dict[str, Any]:
    """
    Extract transcript using yt-dlp with automatic format fallback.

    Args:
        video_url: YouTube video URL
        language: Language code for subtitles
        metadata: Optional video metadata (will fetch if not provided)
        timeout: Command timeout in seconds

    Returns:
        Dictionary containing extraction results
    """
    if not check_ytdlp_available():
        return {
            'method': 'yt-dlp',
            'success': False,
            'error': 'yt-dlp not available - install with: pip install yt-dlp',
            'lines': []
        }

    temp_dir = None
    try:
        # Create temporary directory
        temp_dir = tempfile.mkdtemp(prefix="ytdlp_transcript_")

        # Download subtitles with fallback
        subtitle_file, actual_format = download_subtitles_with_fallback(
            video_url, language, temp_dir, timeout
        )

        # Parse using the appropriate parser
        transcript_lines = parse_subtitle_file(subtitle_file, actual_format)

        # Apply deduplication (mainly needed for VTT fallback)
        original_count = len(transcript_lines)
        if actual_format == 'vtt':
            transcript_lines = deduplicate_transcript_lines(transcript_lines)

        # Calculate deduplication effectiveness
        dedup_effectiveness = (
            (original_count - len(transcript_lines)) / original_count * 100
            if original_count > 0 else 0
        )

        return {
            'method': 'yt-dlp',
            'success': True,
            'format': actual_format,
            'language': language,
            'lines': transcript_lines,
            'line_count': len(transcript_lines),
            'original_line_count': original_count,
            'deduplication_effectiveness': round(dedup_effectiveness, 1)
        }

    except subprocess.TimeoutExpired:
        return {
            'method': 'yt-dlp',
            'success': False,
            'error': "yt-dlp timed out",
            'lines': []
        }
    except Exception as e:
        return {
            'method': 'yt-dlp',
            'success': False,
            'error': str(e),
            'lines': []
        }
    finally:
        # Clean up
        if temp_dir and Path(temp_dir).exists():
            try:
                shutil.rmtree(temp_dir)
            except:
                pass
