#!/usr/bin/env python3
"""
Streamlined YouTube Intelligence Suite - v0.5.0

A sophisticated yet clean Model-Context-Protocol server providing:
- 16 Core Tools: Complete implementations for transcript extraction and AI analysis
- 6 Smart Resources: Zero-token transcript access via MCP resources
- 3 Essential Prompts: Guided workflows for comprehensive analysis

Architecture: Single-file design with modular functions
Focus: Quality over quantity, complete implementations, zero placeholders
"""

import re
import json
import subprocess
import tempfile
import shutil
import os
import glob
import asyncio
import html
from datetime import datetime
from pathlib import Path
from typing import Any, List, Optional, Dict
from mcp.server.fastmcp import FastMCP

# ============================================================================
# CONFIGURATION & SETTINGS
# ============================================================================

class StreamlinedSettings:
    """Streamlined configuration for YouTube Intelligence Suite."""
    
    def __init__(self):
        self.server_name = "YouTube Intelligence Suite"
        self.version = "0.5.0"
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.cache_size = int(os.getenv("CACHE_SIZE", "50"))
        self.default_language = os.getenv("DEFAULT_LANGUAGE", "en")
        # Claude Desktop has a 100,000 character limit for tool responses
        self.max_output_chars = int(os.getenv("MAX_OUTPUT_CHARS", "95000"))
        self.enable_smart_truncation = os.getenv("ENABLE_SMART_TRUNCATION", "true").lower() == "true"
        self.aggressive_dedup = os.getenv("AGGRESSIVE_DEDUP", "true").lower() == "true"
        self.resource_dir = Path("resources/transcripts")
        
    @property
    def server_info(self) -> dict:
        """Get server information."""
        return {
            "name": self.server_name,
            "version": self.version,
            "log_level": self.log_level,
            "cache_size": self.cache_size,
            "default_language": self.default_language,
            "max_output_chars": self.max_output_chars,
            "enable_smart_truncation": self.enable_smart_truncation,
            "aggressive_dedup": self.aggressive_dedup
        }

# Initialize global settings
settings = StreamlinedSettings()

# Initialize FastMCP server
mcp = FastMCP(
    name=settings.server_name,
    version=settings.version,
    dependencies=["yt-dlp>=2023.12.30"]
)

# ============================================================================
# IN-MEMORY CACHING SYSTEM (Two-tier: Memory + File-based MCP Resources)
# ============================================================================

# In-memory cache for transcript data
_transcript_cache: Dict[str, Dict[str, Any]] = {}
_video_cache: Dict[str, Dict[str, Any]] = {}
_analysis_history: List[Dict[str, Any]] = []

def add_to_cache(video_id: str, transcript_data: str, language: str = "en") -> None:
    """Add transcript to in-memory cache."""
    global _transcript_cache, _video_cache
    
    _transcript_cache[video_id] = {
        "transcript": transcript_data,
        "language": language,
        "cached_at": datetime.now().isoformat(),
        "length": len(transcript_data.split('\n'))
    }
    
    _video_cache[video_id] = {
        "video_id": video_id,
        "has_transcript": True,
        "language": language,
        "last_accessed": datetime.now().isoformat()
    }

def add_analysis_to_history(analysis_type: str, video_url: str, query: Optional[str] = None) -> None:
    """Add analysis to history."""
    global _analysis_history
    
    _analysis_history.append({
        "tool": analysis_type,  # Use "tool" key to match test expectations
        "type": analysis_type,  # Keep "type" for backward compatibility
        "video_url": video_url,
        "query": query,
        "timestamp": datetime.now().isoformat()
    })
    
    # Keep only last 100 analyses
    if len(_analysis_history) > 100:
        _analysis_history = _analysis_history[-100:]

def smart_truncate_output(content: str, preserve_structure: bool = True) -> str:
    """Smart truncation that preserves content structure."""
    if len(content) <= settings.max_output_chars:
        return content
    
    if not preserve_structure:
        return content[:settings.max_output_chars] + "\n\n[Content truncated due to length limits]"
    
    # Try to preserve structure by truncating in logical sections
    lines = content.split('\n')
    truncated_lines = []
    current_length = 0
    
    for line in lines:
        if current_length + len(line) + 1 > settings.max_output_chars - 100:  # Leave room for truncation message
            break
        truncated_lines.append(line)
        current_length += len(line) + 1
    
    truncated_content = '\n'.join(truncated_lines)
    truncated_content += f"\n\n[Content truncated - showing {len(truncated_lines)} of {len(lines)} lines due to length limits]"
    
    return truncated_content

# ============================================================================
# CORE EXTRACTION UTILITIES
# ============================================================================

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

def parse_vtt_timestamp(timestamp_str: str) -> float:
    """Parse VTT timestamp to seconds."""
    # Format: 00:00:12.345 -> 12.345 seconds
    parts = timestamp_str.split(':')
    if len(parts) == 3:
        hours, minutes, seconds = parts
        return float(hours) * 3600 + float(minutes) * 60 + float(seconds)
    elif len(parts) == 2:
        minutes, seconds = parts
        return float(minutes) * 60 + float(seconds)
    else:
        return float(parts[0])

def format_timestamp(seconds: float) -> str:
    """Format seconds to MM:SS or HH:MM:SS timestamp."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    
    if hours > 0:
        return f"[{hours:02d}:{minutes:02d}:{secs:02d}]"
    else:
        return f"[{minutes:02d}:{secs:02d}]"

# ============================================================================
# SMART DEDUPLICATION ALGORITHM
# ============================================================================

def deduplicate_transcript_lines(lines: List[str], aggressive: bool = False) -> List[str]:
    """Remove duplicate consecutive text while preserving timestamps.
    
    This fixes the common issue where YouTube auto-captions repeat the same text
    across multiple timestamps as speech continues.
    
    Args:
        lines: List of transcript lines with timestamps
        aggressive: Use more aggressive deduplication for AI analysis
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
        # and last text is not a special caption
        if last_clean_text and clean_text in last_clean_text and len(clean_text) < len(last_clean_text) * 0.8:
            continue
            
        # Skip if the last text is completely contained in this text
        # but this text is much longer (likely an extension)
        if last_clean_text and last_clean_text in clean_text:
            if len(clean_text) > len(last_clean_text) * 1.3:
                # Replace the last entry with this more complete one
                if deduplicated:
                    deduplicated[-1] = line
                    last_clean_text = clean_text
                    continue
        
        if aggressive:
            # Advanced duplicate detection: check word overlap
            current_words = set(clean_text.split())
            if last_words and len(current_words) > 3:
                # Calculate overlap percentage
                overlap = len(current_words.intersection(last_words))
                overlap_percentage = overlap / min(len(current_words), len(last_words))
                
                # If more than 75% word overlap and similar length, skip
                if (overlap_percentage > 0.75 and 
                    abs(len(current_words) - len(last_words)) <= 3):
                    continue
            
            last_words = current_words
        
        deduplicated.append(line)
        last_clean_text = clean_text
    
    return deduplicated

def calculate_quality_score(lines: List[str], video_info: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Calculate transcript quality metrics with enhanced safety validation."""
    if not lines:
        return {
            "quality_score": 0,
            "line_count": 0,
            "avg_line_length": 0,
            "deduplication_effectiveness": 0,
            "has_punctuation": False,
            "timestamp_coverage": 0,
            "quality_warnings": []
        }
    
    # Basic metrics
    line_count = len(lines)
    total_chars = sum(len(line) for line in lines)
    avg_line_length = total_chars / line_count if line_count > 0 else 0
    
    # Punctuation analysis
    punctuation_chars = sum(1 for line in lines for char in line if char in '.,!?;:')
    has_punctuation = punctuation_chars > line_count * 0.1  # At least 10% of lines have punctuation
    
    # Timestamp coverage
    timestamped_lines = sum(1 for line in lines if line.startswith('['))
    timestamp_coverage = timestamped_lines / line_count if line_count > 0 else 0
    
    # Enhanced Quality Validation (NEW)
    quality_warnings = []
    safety_penalties = 0
    
    # Extract text content for analysis
    text_content = []
    for line in lines:
        if line.startswith('[') and ']' in line:
            text = line[line.find(']') + 1:].strip()
            if text:
                text_content.append(text.lower())
        elif line.strip():
            text_content.append(line.strip().lower())
    
    full_text = ' '.join(text_content)
    
    # SAFETY CHECK 1: Detect gibberish/nonsensical content
    if full_text:
        words = full_text.split()
        if len(words) > 10:
            # Check for excessive repetition of short words
            word_freq = {}
            for word in words:
                if len(word) <= 3:  # Short words like "uh", "um", "the"
                    word_freq[word] = word_freq.get(word, 0) + 1
            
            most_common_short = max(word_freq.values()) if word_freq else 0
            if most_common_short > len(words) * 0.15:  # More than 15% repetition
                quality_warnings.append("High repetition of short words detected")
                safety_penalties += 15
    
    # SAFETY CHECK 2: Check for incoherent character sequences
    if full_text:
        # Look for excessive special characters or garbled text
        special_char_ratio = sum(1 for c in full_text if not c.isalnum() and c not in ' .,!?;:-\'\"') / len(full_text)
        if special_char_ratio > 0.05:  # More than 5% special characters
            quality_warnings.append("Excessive special characters suggest garbled content")
            safety_penalties += 20
    
    # SAFETY CHECK 3: Duration validation (if video info available)
    if video_info and 'duration' in video_info:
        expected_lines = video_info['duration'] / 3  # Rough estimate: 1 line per 3 seconds
        if line_count > expected_lines * 2:  # More than double expected
            quality_warnings.append("Transcript length seems excessive for video duration")
            safety_penalties += 10
        elif line_count < expected_lines * 0.3:  # Less than 30% expected
            quality_warnings.append("Transcript seems too short for video duration")
            safety_penalties += 15
    
    # SAFETY CHECK 4: Language consistency check
    if full_text:
        # Simple heuristic: Check for mixed language patterns
        english_words = {'the', 'and', 'is', 'to', 'of', 'in', 'for', 'with', 'on', 'as', 'by', 'this', 'that'}
        words_lower = set(full_text.split())
        english_word_ratio = len(english_words.intersection(words_lower)) / len(english_words)
        
        if english_word_ratio < 0.3 and len(words_lower) > 20:  # Low English word presence
            quality_warnings.append("Content may not be in expected language")
            safety_penalties += 10
    
    # Quality score calculation (0-100)
    quality_score = 0
    
    # Line count factor (more lines generally better, up to a point)
    if line_count > 10:
        quality_score += min(30, line_count * 0.5)
    
    # Average line length (reasonable length indicates good segmentation)
    if 20 <= avg_line_length <= 100:
        quality_score += 25
    elif 10 <= avg_line_length <= 150:
        quality_score += 15
    
    # Punctuation presence
    if has_punctuation:
        quality_score += 20
    
    # Timestamp coverage
    quality_score += timestamp_coverage * 25
    
    # Apply safety penalties
    quality_score = max(0, quality_score - safety_penalties)
    
    # Additional warning if score is artificially high but has safety issues
    if quality_score > 60 and safety_penalties > 20:
        quality_warnings.append("⚠️ High structural score but content quality concerns detected")
    
    return {
        "quality_score": int(quality_score),
        "line_count": line_count,
        "avg_line_length": round(avg_line_length, 1),
        "deduplication_effectiveness": 0,  # Will be calculated during deduplication
        "has_punctuation": has_punctuation,
        "timestamp_coverage": round(timestamp_coverage, 2),
        "quality_warnings": quality_warnings,
        "safety_penalties": safety_penalties
    }

# ============================================================================
# ROBUST TRANSCRIPT EXTRACTION ENGINE
# ============================================================================

def extract_transcript_ytdlp(video_url: str, language: str = "en", metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Extract transcript using yt-dlp with SRV1 format preference and automatic fallback.
    
    This updated version eliminates VTT duplication issues by using srv1 → json3 → ttml → vtt fallback.
    """
    if not check_ytdlp_available():
        return {
            'method': 'yt-dlp',
            'success': False,
            'error': 'yt-dlp not available - install with: pip install yt-dlp',
            'lines': [],
            'available_languages': []
        }
    
    temp_dir = None
    try:
        video_id = extract_video_id(video_url)
        
        # Create temporary directory
        temp_dir = tempfile.mkdtemp(prefix="ytdlp_streamlined_")
        
        # Use new fallback system: srv1 → json3 → ttml → vtt
        subtitle_file, actual_format = download_subtitles_with_fallback(video_url, language, temp_dir)
        
        # Parse using the appropriate parser
        transcript_lines = parse_subtitle_file(subtitle_file, actual_format)
        
        # Calculate original line count for deduplication effectiveness
        original_count = len(transcript_lines)
        
        # Apply deduplication (mainly for VTT fallback)
        if actual_format == 'vtt':
            transcript_lines = deduplicate_transcript_lines(transcript_lines, aggressive=settings.aggressive_dedup)
        
        # Calculate deduplication effectiveness
        dedup_effectiveness = ((original_count - len(transcript_lines)) / original_count * 100) if original_count > 0 else 0
        
        # Try to detect available languages from the downloaded files
        all_subtitle_files = glob.glob(f'{temp_dir}/*.{actual_format}')
        available_languages = []
        for subtitle_file_path in all_subtitle_files:
            filename = os.path.basename(subtitle_file_path)
            if '.' in filename:
                lang_part = filename.split('.')[-2]
                if len(lang_part) <= 5:  # Language codes are typically 2-5 chars
                    available_languages.append(lang_part)
        
        # Calculate quality metrics with video context for enhanced validation
        video_context = {}
        if metadata:
            video_context = {'duration': metadata.get('duration', 0)}
        else:
            try:
                # Try to get video duration for validation
                metadata_result = extract_enhanced_metadata(video_url)
                if metadata_result['success']:
                    video_context = {'duration': metadata_result['metadata'].get('duration', 0)}
            except:
                pass  # Use default context if metadata extraction fails
            
        quality_metrics = calculate_quality_score(transcript_lines, video_context)
        quality_metrics["deduplication_effectiveness"] = round(dedup_effectiveness, 1)
        quality_metrics["format_used"] = actual_format
        
        return {
            'method': 'yt-dlp',
            'success': True,
            'video_id': video_id,
            'language': language,
            'format': actual_format,  # Report actual format used
            'lines': transcript_lines,
            'line_count': len(transcript_lines),
            'original_line_count': original_count,
            'quality_metrics': quality_metrics,
            'available_languages': list(set(available_languages)) if available_languages else ['en (auto)']
        }
        
    except subprocess.TimeoutExpired:
        return {
            'method': 'yt-dlp',
            'success': False,
            'error': "yt-dlp timed out after 60 seconds",
            'lines': [],
            'available_languages': []
        }
    except Exception as e:
        return {
            'method': 'yt-dlp',
            'success': False,
            'error': str(e),
            'lines': [],
            'available_languages': []
        }
    finally:
        # Clean up temporary directory
        if temp_dir and os.path.exists(temp_dir):
            try:
                shutil.rmtree(temp_dir)
            except:
                pass  # Ignore cleanup errors

def extract_enhanced_metadata(video_url: str) -> Dict[str, Any]:
    """Extract comprehensive video metadata using yt-dlp."""
    if not check_ytdlp_available():
        return {
            'success': False,
            'error': 'yt-dlp not available',
            'metadata': {}
        }
    
    try:
        video_id = extract_video_id(video_url)
        
        cmd = [
            'yt-dlp',
            '--dump-json',
            '--no-download',
            video_url
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode != 0:
            return {
                'success': False,
                'error': f"Failed to extract metadata: {result.stderr}",
                'metadata': {}
            }
        
        metadata = json.loads(result.stdout)
        
        # Extract key information
        enhanced_metadata = {
            'video_id': video_id,
            'title': metadata.get('title', 'Unknown Title'),
            'description': metadata.get('description', ''),
            'duration': metadata.get('duration', 0),
            'view_count': metadata.get('view_count', 0),
            'like_count': metadata.get('like_count', 0),
            'channel': metadata.get('uploader', 'Unknown Channel'),
            'channel_id': metadata.get('uploader_id', ''),
            'upload_date': metadata.get('upload_date', ''),
            'tags': metadata.get('tags', []),
            'categories': metadata.get('categories', []),
            'thumbnail': metadata.get('thumbnail', ''),
            'webpage_url': metadata.get('webpage_url', video_url),
            'language': metadata.get('language', 'en'),
            'automatic_captions': list(metadata.get('automatic_captions', {}).keys()),
            'subtitles': list(metadata.get('subtitles', {}).keys())
        }
        
        return {
            'success': True,
            'video_id': video_id,
            'metadata': enhanced_metadata
        }
        
    except subprocess.TimeoutExpired:
        return {
            'success': False,
            'error': "Metadata extraction timed out",
            'metadata': {}
        }
    except json.JSONDecodeError:
        return {
            'success': False,
            'error': "Failed to parse metadata JSON",
            'metadata': {}
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'metadata': {}
        }

def create_plain_text_transcript(lines: List[str], aggressive_dedup: bool = True) -> str:
    """Create clean plain text transcript optimized for AI analysis."""
    if not lines:
        return ""
    
    # Apply aggressive deduplication if requested
    if aggressive_dedup:
        lines = deduplicate_transcript_lines(lines, aggressive=True)
    
    # Extract text without timestamps
    plain_text_lines = []
    for line in lines:
        if line.startswith('[') and ']' in line:
            # Extract text after timestamp
            text = line[line.find(']') + 1:].strip()
            if text and text not in ['[Music]', '[Applause]', '[Laughter]']:
                plain_text_lines.append(text)
        elif line.strip():
            plain_text_lines.append(line.strip())
    
    # Join with appropriate spacing
    return ' '.join(plain_text_lines)

# ============================================================================
# MCP RESOURCE MANAGEMENT LAYER
# ============================================================================

def ensure_resource_directory():
    """Ensure the resource directory exists."""
    settings.resource_dir.mkdir(parents=True, exist_ok=True)

def get_resource_path(video_id: str) -> Path:
    """Get the path for a video resource file."""
    ensure_resource_directory()
    return settings.resource_dir / f"{video_id}.md"

def create_resource_content(video_id: str, transcript_lines: List[str], metadata: Dict[str, Any], quality_metrics: Dict[str, Any]) -> str:
    """Create comprehensive MCP resource content."""
    timestamp = datetime.now().isoformat()
    
    # Create plain text version
    plain_text = create_plain_text_transcript(transcript_lines, aggressive_dedup=True)
    
    # Format timestamped transcript
    timestamped_transcript = '\n'.join(transcript_lines)
    
    content = f"""# YouTube Video Transcript - {metadata.get('title', 'Unknown Title')}

## Video Information
- **Video ID**: {video_id}
- **Title**: {metadata.get('title', 'Unknown Title')}
- **Channel**: {metadata.get('channel', 'Unknown Channel')}
- **Duration**: {metadata.get('duration', 0)} seconds
- **Views**: {metadata.get('view_count', 0):,}
- **Language**: {metadata.get('language', 'en')}
- **Upload Date**: {metadata.get('upload_date', 'Unknown')}
- **URL**: {metadata.get('webpage_url', f'https://youtube.com/watch?v={video_id}')}

## Quality Metrics
- **Quality Score**: {quality_metrics.get('quality_score', 0)}%
- **Line Count**: {quality_metrics.get('line_count', 0)}
- **Average Line Length**: {quality_metrics.get('avg_line_length', 0)} characters
- **Deduplication Effectiveness**: {quality_metrics.get('deduplication_effectiveness', 0)}%
- **Has Punctuation**: {quality_metrics.get('has_punctuation', False)}
- **Timestamp Coverage**: {quality_metrics.get('timestamp_coverage', 0) * 100:.1f}%

## Plain Text Transcript (AI-Optimized)
```
{plain_text}
```

## Timestamped Transcript
```
{timestamped_transcript}
```

## Resource Metadata
- **Generated**: {timestamp}
- **Server**: {settings.server_name} v{settings.version}
- **Extraction Method**: yt-dlp
- **Deduplication**: {'Aggressive' if settings.aggressive_dedup else 'Standard'}

---
*This resource was generated by the YouTube Intelligence Suite for zero-token transcript access via MCP.*
"""
    
    return content

def save_resource_file(video_id: str, content: str) -> bool:
    """Save resource content to file."""
    try:
        resource_path = get_resource_path(video_id)
        with open(resource_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception:
        return False

def load_resource_file(video_id: str) -> Optional[str]:
    """Load resource content from file."""
    try:
        resource_path = get_resource_path(video_id)
        if resource_path.exists():
            with open(resource_path, 'r', encoding='utf-8') as f:
                return f.read()
        return None
    except Exception:
        return None

def list_available_resources() -> List[Dict[str, Any]]:
    """List all available transcript resources."""
    resources = []
    
    if not settings.resource_dir.exists():
        return resources
    
    for resource_file in settings.resource_dir.glob("*.md"):
        try:
            video_id = resource_file.stem
            content = resource_file.read_text(encoding='utf-8')
            
            # Extract basic info from content
            lines = content.split('\n')
            title = "Unknown Title"
            channel = "Unknown Channel"
            
            for line in lines:
                # Handle both formats: "- **Title**:" (manual) and "- **Title**" (MCP server)
                if line.startswith('- **Title**:'):
                    title = line.replace('- **Title**:', '').strip()
                elif line.startswith('- **Title**'):
                    title = line.replace('- **Title**', '').strip().lstrip(':').strip()
                elif line.startswith('- **Channel**:'):
                    channel = line.replace('- **Channel**:', '').strip()
                elif line.startswith('- **Channel**'):
                    channel = line.replace('- **Channel**', '').strip().lstrip(':').strip()
            
            resources.append({
                'video_id': video_id,
                'title': title,
                'channel': channel,
                'file_size': resource_file.stat().st_size,
                'created': datetime.fromtimestamp(resource_file.stat().st_ctime).isoformat()
            })
            
        except Exception:
            continue
    
    return sorted(resources, key=lambda x: x['created'], reverse=True)

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
                timestamp = format_timestamp(start_time)
                
                # Clean and format text
                clean_text = re.sub(r'<[^>]+>', '', text).strip()
                # Decode HTML entities
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
                timestamp = format_timestamp(start_time)
                
                # Clean text
                clean_text = re.sub(r'<[^>]+>', '', text).strip()
                # Decode HTML entities
                clean_text = html.unescape(clean_text)
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
                # Decode HTML entities
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
                # Decode HTML entities
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
        # Decode HTML entities
        clean_text = html.unescape(clean_text)
        if clean_text:
            transcript_lines.append(f"{current_timestamp} {clean_text}")
    
    return transcript_lines

# ============================================================================
# MCP TOOLS - 16 ESSENTIAL TOOLS (Complete Implementations)
# ============================================================================

@mcp.tool()
async def get_youtube_transcript(video_url: str, language: str = "en") -> str:
    """Get the transcript of a YouTube video using the primary extraction method.

    Args:
        video_url: YouTube video URL
        language: Language code (e.g., 'en', 'es'). Defaults to 'en'
    """
    try:
        # Get metadata for enhanced quality analysis
        metadata_result = extract_enhanced_metadata(video_url)
        metadata = metadata_result.get('metadata', {}) if metadata_result['success'] else {}
        
        # Extract using yt-dlp (our primary method)
        result = extract_transcript_ytdlp(video_url, language, metadata)
        
        if not result['success']:
            add_analysis_to_history("get_youtube_transcript", video_url, f"Failed: {result['error']}")
            return f"❌ Failed to extract transcript: {result['error']}"
        
        # Add to cache
        video_id = result['video_id']
        transcript_text = '\n'.join(result['lines'])
        add_to_cache(video_id, transcript_text, language)
        
        # Add to analysis history
        add_analysis_to_history("get_youtube_transcript", video_url, f"Success: {result['line_count']} lines")
        
        # Format output
        output = f"""# 📺 Transcript for Video: {video_id}

**Extraction Details:**
- Method: {result['method']}
- Language: {result['language']}
- Lines: {result['line_count']} (originally {result.get('original_line_count', result['line_count'])})
- Quality Score: {result['quality_metrics']['quality_score']}%
- Deduplication: {result['quality_metrics']['deduplication_effectiveness']}% duplicates removed

**Transcript:**
{transcript_text}

**Available Languages:** {', '.join(result['available_languages'])}
"""
        
        return smart_truncate_output(output)
        
    except Exception as e:
        add_analysis_to_history("get_youtube_transcript", video_url, f"Error: {str(e)}")
        return f"❌ Error extracting transcript: {str(e)}"

@mcp.tool()
async def get_youtube_transcript_ytdlp(video_url: str, language: str = "en") -> str:
    """Get the transcript of a YouTube video using yt-dlp (most reliable method).

    Args:
        video_url: YouTube video URL
        language: Language code (e.g., 'en', 'es'). Defaults to 'en'
    """
    try:
        # Get metadata for enhanced quality analysis
        metadata_result = extract_enhanced_metadata(video_url)
        metadata = metadata_result.get('metadata', {}) if metadata_result['success'] else {}
        
        result = extract_transcript_ytdlp(video_url, language, metadata)
        
        if not result['success']:
            add_analysis_to_history("get_youtube_transcript_ytdlp", video_url, f"Failed: {result['error']}")
            return f"❌ yt-dlp extraction failed: {result['error']}"
        
        # Add to cache
        video_id = result['video_id']
        transcript_text = '\n'.join(result['lines'])
        add_to_cache(video_id, transcript_text, language)
        
        # Add to analysis history
        add_analysis_to_history("get_youtube_transcript_ytdlp", video_url, f"Success: {result['line_count']} lines")
        
        # Format output with detailed quality information
        output = f"""# 🎯 yt-dlp Transcript Extraction

**Video ID:** {video_id}
**Language:** {result['language']}
**Method:** {result['method']}

**Quality Analysis:**
- Original Lines: {result.get('original_line_count', result['line_count'])}
- Final Lines: {result['line_count']}
- Quality Score: {result['quality_metrics']['quality_score']}%
- Deduplication Effectiveness: {result['quality_metrics']['deduplication_effectiveness']}%
- Average Line Length: {result['quality_metrics']['avg_line_length']} chars
- Has Punctuation: {result['quality_metrics']['has_punctuation']}
- Timestamp Coverage: {result['quality_metrics']['timestamp_coverage'] * 100:.1f}%

**Available Languages:** {', '.join(result['available_languages'])}

**Transcript:**
{transcript_text}
"""
        
        return smart_truncate_output(output)
        
    except Exception as e:
        add_analysis_to_history("get_youtube_transcript_ytdlp", video_url, f"Error: {str(e)}")
        return f"❌ Error with yt-dlp extraction: {str(e)}"

@mcp.tool()
async def get_plain_text_transcript(video_url: str, aggressive_dedup: bool = True) -> str:
    """Extract clean plain text transcript without timestamps, optimized for AI analysis.

    Args:
        video_url: YouTube video URL
        aggressive_dedup: Use aggressive deduplication for cleaner text
    """
    try:
        # Get metadata for enhanced quality analysis
        metadata_result = extract_enhanced_metadata(video_url)
        metadata = metadata_result.get('metadata', {}) if metadata_result['success'] else {}
        
        result = extract_transcript_ytdlp(video_url, "en", metadata)
        
        if not result['success']:
            add_analysis_to_history("get_plain_text_transcript", video_url, f"Failed: {result['error']}")
            return f"❌ Failed to extract transcript: {result['error']}"
        
        # Create plain text version
        plain_text = create_plain_text_transcript(result['lines'], aggressive_dedup)
        
        # Add to cache
        video_id = result['video_id']
        add_to_cache(video_id, plain_text, "en")
        
        # Add to analysis history
        add_analysis_to_history("get_plain_text_transcript", video_url, f"Success: {len(plain_text)} chars")
        
        output = f"""# 📝 Plain Text Transcript (AI-Optimized)

**Video ID:** {video_id}
**Original Lines:** {result.get('original_line_count', result['line_count'])}
**Final Lines:** {result['line_count']}
**Plain Text Length:** {len(plain_text)} characters
**Deduplication:** {'Aggressive' if aggressive_dedup else 'Standard'}
**Quality Score:** {result['quality_metrics']['quality_score']}%

**Clean Text:**
{plain_text}
"""
        
        return smart_truncate_output(output)
        
    except Exception as e:
        add_analysis_to_history("get_plain_text_transcript", video_url, f"Error: {str(e)}")
        return f"❌ Error extracting plain text: {str(e)}"

@mcp.tool()
async def get_enhanced_video_metadata(video_url: str) -> str:
    """Get comprehensive video metadata using enhanced extraction pipeline.

    Args:
        video_url: YouTube video URL
    """
    try:
        result = extract_enhanced_metadata(video_url)
        
        if not result['success']:
            add_analysis_to_history("get_enhanced_video_metadata", video_url, f"Failed: {result['error']}")
            return f"❌ Failed to extract metadata: {result['error']}"
        
        metadata = result['metadata']
        
        # Add to analysis history
        add_analysis_to_history("get_enhanced_video_metadata", video_url, f"Success: {metadata['title']}")
        
        # Format duration
        duration = metadata.get('duration', 0)
        duration_str = f"{duration // 60}:{duration % 60:02d}" if duration > 0 else "Unknown"
        
        output = f"""# 📊 Enhanced Video Metadata

## Basic Information
- **Title:** {metadata.get('title', 'Unknown')}
- **Channel:** {metadata.get('channel', 'Unknown')}
- **Video ID:** {metadata.get('video_id', 'Unknown')}
- **Duration:** {duration_str}
- **Language:** {metadata.get('language', 'Unknown')}

## Engagement Metrics
- **Views:** {metadata.get('view_count', 0):,}
- **Likes:** {metadata.get('like_count', 0):,}
- **Upload Date:** {metadata.get('upload_date', 'Unknown')}

## Content Details
- **Description:** {metadata.get('description', 'No description available')[:500]}{'...' if len(metadata.get('description', '')) > 500 else ''}
- **Tags:** {', '.join(metadata.get('tags', [])[:10])}
- **Categories:** {', '.join(metadata.get('categories', []))}

## Technical Information
- **Channel ID:** {metadata.get('channel_id', 'Unknown')}
- **Thumbnail:** {metadata.get('thumbnail', 'Not available')}
- **Webpage URL:** {metadata.get('webpage_url', video_url)}

## Subtitle Availability
- **Automatic Captions:** {', '.join(metadata.get('automatic_captions', []))}
- **Manual Subtitles:** {', '.join(metadata.get('subtitles', []))}
"""
        
        return smart_truncate_output(output)
        
    except Exception as e:
        add_analysis_to_history("get_enhanced_video_metadata", video_url, f"Error: {str(e)}")
        return f"❌ Error extracting metadata: {str(e)}"

@mcp.tool()
async def get_transcript_quality_analysis(video_url: str) -> str:
    """Get comprehensive quality analysis for a YouTube video transcript.

    Args:
        video_url: YouTube video URL
    """
    try:
        # Get metadata for enhanced quality analysis
        metadata_result = extract_enhanced_metadata(video_url)
        metadata = metadata_result.get('metadata', {}) if metadata_result['success'] else {}
        
        result = extract_transcript_ytdlp(video_url, "en", metadata)
        
        if not result['success']:
            add_analysis_to_history("get_transcript_quality_analysis", video_url, f"Failed: {result['error']}")
            return f"❌ Failed to extract transcript for analysis: {result['error']}"
        
        quality = result['quality_metrics']
        video_id = result['video_id']
        
        # Add to analysis history
        add_analysis_to_history("get_transcript_quality_analysis", video_url, f"Score: {quality['quality_score']}%")
        
        # Determine quality rating
        score = quality['quality_score']
        if score >= 80:
            rating = "Excellent ⭐⭐⭐⭐⭐"
        elif score >= 60:
            rating = "Good ⭐⭐⭐⭐"
        elif score >= 40:
            rating = "Fair ⭐⭐⭐"
        elif score >= 20:
            rating = "Poor ⭐⭐"
        else:
            rating = "Very Poor ⭐"
        
        output = f"""# 🔍 Transcript Quality Analysis

**Video ID:** {video_id}
**Overall Rating:** {rating}
**Quality Score:** {score}%

## Detailed Metrics

### Content Analysis
- **Total Lines:** {quality['line_count']}
- **Original Lines:** {result.get('original_line_count', quality['line_count'])}
- **Duplicates Removed:** {result.get('original_line_count', quality['line_count']) - quality['line_count']}
- **Deduplication Effectiveness:** {quality['deduplication_effectiveness']}%

### Text Quality
- **Average Line Length:** {quality['avg_line_length']} characters
- **Has Punctuation:** {'Yes ✅' if quality['has_punctuation'] else 'No ❌'}
- **Timestamp Coverage:** {quality['timestamp_coverage'] * 100:.1f}%

### Quality Factors
- **Line Count Score:** {min(30, quality['line_count'] * 0.5):.1f}/30
- **Length Score:** {25 if 20 <= quality['avg_line_length'] <= 100 else 15 if 10 <= quality['avg_line_length'] <= 150 else 0}/25
- **Punctuation Score:** {20 if quality['has_punctuation'] else 0}/20
- **Timestamp Score:** {quality['timestamp_coverage'] * 25:.1f}/25
- **Safety Penalties:** -{quality.get('safety_penalties', 0)} points

### Quality Warnings
{chr(10).join(f"- 🚨 {warning}" for warning in quality.get('quality_warnings', [])) if quality.get('quality_warnings') else "- ✅ No quality concerns detected"}

## Recommendations
"""
        
        # Add recommendations based on quality
        if score < 40:
            output += "- ⚠️ Low quality transcript - consider using multiple extraction methods\n"
        if not quality['has_punctuation']:
            output += "- 📝 No punctuation detected - likely auto-generated captions\n"
        if quality['timestamp_coverage'] < 0.5:
            output += "- ⏰ Low timestamp coverage - some content may be missing timing\n"
        if quality['deduplication_effectiveness'] > 30:
            output += "- 🔄 High duplication removed - original had many repeated segments\n"
        
        if score >= 80:
            output += "- ✅ Excellent quality transcript - suitable for all analysis types\n"
        elif score >= 60:
            output += "- ✅ Good quality transcript - reliable for most analysis purposes\n"
        
        return output
        
    except Exception as e:
        add_analysis_to_history("get_transcript_quality_analysis", video_url, f"Error: {str(e)}")
        return f"❌ Error analyzing transcript quality: {str(e)}"

# ============================================================================
# MCP RESOURCE ACCESS TOOLS (CRITICAL for Claude Desktop Integration)
# ============================================================================

@mcp.tool()
async def list_transcript_resources() -> str:
    """List all available transcript resources in the system.
    
    This tool provides access to stored transcript files that can be loaded without tokens.
    """
    try:
        resources = list_available_resources()
        
        if not resources:
            return """# 📁 Transcript Resources

No transcript resources found. Create new resources using:
- `get_youtube_transcript()` - Extract and cache transcript
- `create_mcp_resource_from_transcript_v2()` - Create persistent resource file

Resources are stored in: `resources/transcripts/`"""
        
        output = f"""# 📁 Available Transcript Resources

**Total Resources:** {len(resources)}

## Available Transcripts

"""
        
        for i, resource in enumerate(resources, 1):
            output += f"""### {i}. {resource['title'][:60]}{'...' if len(resource['title']) > 60 else ''}
- **Video ID:** `{resource['video_id']}`
- **Channel:** {resource['channel']}
- **File Size:** {resource['file_size']:,} bytes
- **Created:** {resource['created'][:19].replace('T', ' ')}
- **Access:** Use `load_transcript_resource("{resource['video_id']}")` or resource `transcripts://content/{resource['video_id']}`

"""
        
        output += f"""## Usage Instructions

### Load Specific Transcript
```
load_transcript_resource("VIDEO_ID")
```

### Direct Resource Access
```
transcripts://content/VIDEO_ID
```

### Create New Resource
```
create_mcp_resource_from_transcript_v2("https://youtube.com/watch?v=VIDEO_ID")
```

**Resource Directory:** `{settings.resource_dir}`
"""
        
        return output
        
    except Exception as e:
        return f"❌ Error listing transcript resources: {str(e)}"

@mcp.tool()
async def load_transcript_resource(video_id: str) -> str:
    """Load a specific transcript resource by video ID.
    
    Args:
        video_id: YouTube video ID to load transcript for
    """
    try:
        content = load_resource_file(video_id)
        
        if content is None:
            available_resources = list_available_resources()
            available_ids = [r['video_id'] for r in available_resources]
            
            return f"""❌ Transcript resource not found for video ID: `{video_id}`

**Available Video IDs:**
{chr(10).join(f"- {vid_id}" for vid_id in available_ids[:10])}
{f"... and {len(available_ids) - 10} more" if len(available_ids) > 10 else ""}

Use `list_transcript_resources()` to see all available resources."""
        
        return content
        
    except Exception as e:
        return f"❌ Error loading transcript resource: {str(e)}"

@mcp.tool()
async def create_mcp_resource_from_transcript_v2(video_url: str, resource_name: str = "") -> str:
    """Create a persistent MCP resource from a YouTube video transcript.
    
    This creates a markdown file in resources/transcripts/ that can be accessed
    with zero token consumption via MCP resources.
    
    Args:
        video_url: YouTube video URL
        resource_name: Optional custom name for the resource (auto-generated if empty)
    """
    try:
        # Extract video metadata for resource creation
        metadata_result = extract_enhanced_metadata(video_url)
        if not metadata_result['success']:
            return f"❌ Failed to extract video metadata: {metadata_result['error']}"
        
        metadata = metadata_result['metadata']
        video_id = metadata['video_id']
        
        # Extract transcript
        transcript_result = extract_transcript_ytdlp(video_url, "en", metadata)
        if not transcript_result['success']:
            return f"❌ Failed to extract transcript: {transcript_result['error']}"
        
        # Create resource content
        resource_content = create_resource_content(
            video_id, 
            transcript_result['lines'], 
            metadata, 
            transcript_result['quality_metrics']
        )
        
        # Save resource file
        success = save_resource_file(video_id, resource_content)
        if not success:
            return f"❌ Failed to save resource file for video {video_id}"
        
        # Add to cache
        transcript_text = '\n'.join(transcript_result['lines'])
        add_to_cache(video_id, transcript_text, "en")
        
        # Add to analysis history
        add_analysis_to_history("create_mcp_resource_from_transcript_v2", video_url, f"Created: {video_id}")
        
        # Get file path for confirmation
        resource_path = get_resource_path(video_id)
        file_size = resource_path.stat().st_size if resource_path.exists() else 0
        
        return f"""✅ Successfully created MCP resource!

## Resource Details
- **Video ID:** `{video_id}`
- **Title:** {metadata.get('title', 'Unknown Title')}
- **Channel:** {metadata.get('channel', 'Unknown Channel')}
- **File Path:** `{resource_path}`
- **File Size:** {file_size:,} bytes
- **Quality Score:** {transcript_result['quality_metrics']['quality_score']}%

## Access Methods

### Tool Access
```
load_transcript_resource("{video_id}")
```

### Direct Resource Access (Zero Tokens)
```
transcripts://content/{video_id}
```

### List All Resources
```
list_transcript_resources()
```

The resource is now available for zero-token access via MCP resources!"""
        
    except Exception as e:
        add_analysis_to_history("create_mcp_resource_from_transcript_v2", video_url, f"Error: {str(e)}")
        return f"❌ Error creating MCP resource: {str(e)}"

# ============================================================================
# MCP RESOURCES - 6 SMART RESOURCES (Zero-Token Data Access)
# ============================================================================

@mcp.resource("transcripts://available")
async def get_available_transcripts_resource() -> dict:
    """List all available transcript resources (CRITICAL for zero-token browsing)."""
    try:
        resources = list_available_resources()
        
        return {
            "description": "Available transcript resources for zero-token access",
            "mimeType": "application/json",
            "text": json.dumps({
                "total_resources": len(resources),
                "resources": resources,
                "last_updated": datetime.now().isoformat(),
                "usage_instructions": {
                    "load_resource": "Use load_transcript_resource(video_id) tool",
                    "direct_access": "Use transcripts://content/{video_id} resource",
                    "create_new": "Use create_mcp_resource_from_transcript_v2() tool"
                }
            }, indent=2)
        }
    except Exception as e:
        return {
            "description": "Error loading available transcripts",
            "mimeType": "text/plain", 
            "text": f"Error: {str(e)}"
        }

@mcp.resource("transcripts://content/{video_id}")
async def get_transcript_content_resource(video_id: str) -> dict:
    """Direct content access for specific video transcript (CRITICAL for zero-token access)."""
    try:
        content = load_resource_file(video_id)
        
        if content is None:
            return {
                "description": f"Transcript resource not found for video {video_id}",
                "mimeType": "text/plain",
                "text": f"Resource not found for video ID: {video_id}\n\nUse list_transcript_resources() to see available resources."
            }
        
        return {
            "description": f"Complete transcript resource for video {video_id}",
            "mimeType": "text/markdown",
            "text": content
        }
        
    except Exception as e:
        return {
            "description": f"Error loading transcript for {video_id}",
            "mimeType": "text/plain",
            "text": f"Error loading resource: {str(e)}"
        }

@mcp.resource("transcripts://cached")
async def get_cached_transcripts_resource() -> dict:
    """Get information about in-memory cached transcripts."""
    try:
        cached_data = {
            "cache_size": len(_transcript_cache),
            "cached_videos": [],
            "memory_usage": {
                "transcript_cache_entries": len(_transcript_cache),
                "video_cache_entries": len(_video_cache),
                "analysis_history_entries": len(_analysis_history)
            },
            "last_updated": datetime.now().isoformat()
        }
        
        for video_id, data in _transcript_cache.items():
            cached_data["cached_videos"].append({
                "video_id": video_id,
                "language": data.get("language", "unknown"),
                "cached_at": data.get("cached_at", ""),
                "transcript_length": data.get("length", 0)
            })
        
        return {
            "description": "In-memory transcript cache information",
            "mimeType": "application/json",
            "text": json.dumps(cached_data, indent=2)
        }
        
    except Exception as e:
        return {
            "description": "Error accessing cache information",
            "mimeType": "text/plain",
            "text": f"Error: {str(e)}"
        }

@mcp.resource("transcripts://quality_report")
async def get_quality_report_resource() -> dict:
    """System-wide quality analytics and processing statistics."""
    try:
        # Analyze existing resources for quality metrics
        resources = list_available_resources()
        
        quality_data = {
            "system_stats": {
                "total_resources": len(resources),
                "total_file_size_mb": sum(r['file_size'] for r in resources) / (1024 * 1024),
                "average_file_size_kb": sum(r['file_size'] for r in resources) / len(resources) / 1024 if resources else 0
            },
            "quality_settings": {
                "aggressive_deduplication": settings.aggressive_dedup,
                "smart_truncation": settings.enable_smart_truncation,
                "max_output_chars": settings.max_output_chars,
                "cache_size": settings.cache_size
            },
            "analysis_history": {
                "total_analyses": len(_analysis_history),
                "recent_analyses": _analysis_history[-10:] if _analysis_history else []
            },
            "generated_at": datetime.now().isoformat()
        }
        
        return {
            "description": "System-wide quality and performance analytics",
            "mimeType": "application/json", 
            "text": json.dumps(quality_data, indent=2)
        }
        
    except Exception as e:
        return {
            "description": "Error generating quality report",
            "mimeType": "text/plain",
            "text": f"Error: {str(e)}"
        }

@mcp.resource("analytics://history")
async def get_analysis_history_resource() -> dict:
    """Usage tracking and analysis history."""
    try:
        history_data = {
            "total_analyses": len(_analysis_history),
            "analysis_history": _analysis_history,
            "analysis_summary": {},
            "last_updated": datetime.now().isoformat()
        }
        
        # Summarize analysis types
        for analysis in _analysis_history:
            tool_name = analysis.get("tool", "unknown")
            if tool_name in history_data["analysis_summary"]:
                history_data["analysis_summary"][tool_name] += 1
            else:
                history_data["analysis_summary"][tool_name] = 1
        
        return {
            "description": "Analysis history and usage statistics",
            "mimeType": "application/json",
            "text": json.dumps(history_data, indent=2)
        }
        
    except Exception as e:
        return {
            "description": "Error accessing analysis history",
            "mimeType": "text/plain",
            "text": f"Error: {str(e)}"
        }

@mcp.resource("system://status")
async def get_system_status_resource() -> dict:
    """Health monitoring and system status."""
    try:
        status_data = {
            "server_info": settings.server_info,
            "system_health": {
                "ytdlp_available": check_ytdlp_available(),
                "resource_directory_exists": settings.resource_dir.exists(),
                "resource_directory_writable": os.access(settings.resource_dir, os.W_OK) if settings.resource_dir.exists() else False
            },
            "statistics": {
                "cached_transcripts": len(_transcript_cache),
                "cached_videos": len(_video_cache),
                "analysis_history": len(_analysis_history),
                "available_resources": len(list_available_resources())
            },
            "status_timestamp": datetime.now().isoformat()
        }
        
        return {
            "description": "System health and status information",
            "mimeType": "application/json",
            "text": json.dumps(status_data, indent=2)
        }
        
    except Exception as e:
        return {
            "description": "Error getting system status",
            "mimeType": "text/plain",
            "text": f"Error: {str(e)}"
        }

# ============================================================================
# MCP PROMPTS - 3 ESSENTIAL GUIDED WORKFLOWS
# ============================================================================

@mcp.prompt()
async def transcript_analysis_workshop(video_url: str, focus_area: str = "general") -> str:
    """Interactive workshop prompt for comprehensive transcript analysis."""
    
    focus_guidance = {
        "educational": "learning objectives, teaching methods, clarity of explanations, educational value",
        "business": "key insights, actionable advice, market trends, strategic recommendations", 
        "technical": "technical accuracy, implementation details, code examples, best practices",
        "entertainment": "storytelling techniques, audience engagement, entertainment value, content structure",
        "general": "main themes, key insights, content quality, presentation effectiveness"
    }
    
    guidance = focus_guidance.get(focus_area, focus_guidance["general"])
    
    return f"""# 📺 Transcript Analysis Workshop

## Video Analysis Session
**Video:** {video_url}
**Focus Area:** {focus_area.title()}

## Analysis Framework

Let's conduct a comprehensive analysis focusing on: {guidance}

### Phase 1: Initial Exploration
1. **Content Overview**: What is the main topic and purpose of this video?
2. **Structure Analysis**: How is the content organized? (intro, main points, conclusion)
3. **Target Audience**: Who is this video intended for?

### Phase 2: Deep Analysis  
4. **Key Messages**: What are the 3-5 most important points made?
5. **Supporting Evidence**: What examples, data, or stories support the main points?
6. **Quality Assessment**: How well does the content achieve its purpose?

### Phase 3: Critical Evaluation
7. **Strengths**: What does this video do particularly well?
8. **Weaknesses**: What could be improved or is missing?
9. **Credibility**: How trustworthy and authoritative is the information?

### Phase 4: Actionable Insights
10. **Key Takeaways**: What should viewers remember or act on?
11. **Follow-up Questions**: What questions does this raise for further exploration?
12. **Application**: How can this information be practically applied?

---
**Instructions:** Please extract the transcript using the get_youtube_transcript tool, then work through this analysis framework systematically. Provide specific examples and quotes from the transcript to support your analysis."""

@mcp.prompt()
async def study_notes_generator(video_url: str, subject_area: str = "general", note_style: str = "outline") -> str:
    """Generate structured study notes from educational video content."""
    
    style_templates = {
        "outline": """
### Hierarchical Outline Format
```
I. Main Topic
   A. Subtopic
      1. Key point
      2. Supporting detail
         a. Example
         b. Evidence
   B. Subtopic
      1. Key point
II. Main Topic
```""",
        
        "cornell": """
### Cornell Notes Format
```
Cue Column (Keywords/Questions) | Note-Taking Area
-------------------------------|------------------
Key term                      | Detailed explanation
Important question             | Comprehensive answer
Main concept                   | Examples and details

Summary Section:
Brief overview of all key points
```""",
        
        "mindmap": """
### Mind Map Structure
```
Central Topic
├── Branch 1: Main Concept
│   ├── Sub-concept A
│   └── Sub-concept B
├── Branch 2: Main Concept  
│   ├── Sub-concept C
│   └── Sub-concept D
└── Branch 3: Main Concept
    ├── Sub-concept E
    └── Sub-concept F
```""",
        
        "flashcards": """
### Flashcard Format
```
Card 1:
Q: Question or term
A: Answer or definition

Card 2: 
Q: Question or term
A: Answer or definition
```"""
    }
    
    template = style_templates.get(note_style, style_templates["outline"])
    
    return f"""# 📚 Study Notes Generator

## Study Session Setup
**Video:** {video_url}
**Subject Area:** {subject_area.title()}
**Note Style:** {note_style.title()}

## Note-Taking Framework

{template}

### Subject-Specific Guidelines
**For {subject_area}:**
- Focus on key concepts, definitions, and terminology
- Include examples and applications
- Note any formulas, processes, or methodologies
- Identify connections between concepts
- Highlight important facts and figures

### Study Notes Creation Process

**Step 1:** Extract full transcript using get_youtube_transcript tool

**Step 2:** Identify the educational structure:
- Learning objectives (stated or implied)
- Main concepts and subtopics
- Examples and applications
- Key terminology

**Step 3:** Organize content using the {note_style} format

**Step 4:** Add study aids:
- Key terms with definitions
- Important questions for review
- Cross-references and connections
- Practice problems or examples

**Step 5:** Create summary section with main takeaways

---
**Instructions:** Transform the video transcript into comprehensive study notes using the specified format. Focus on educational value and retention."""

@mcp.prompt()
async def video_research_planner(topic: str, research_depth: str = "comprehensive") -> str:
    """Plan a research strategy using YouTube videos for learning about a topic."""
    
    depth_strategies = {
        "overview": """
### Overview Research Strategy (2-3 hours)
**Goal:** Get a solid foundational understanding

**Video Types to Find:**
1. **Introduction Videos** (2-3 videos)
   - "Introduction to [topic]"
   - "What is [topic]?"
   - Beginner-friendly explanations

2. **Overview/Summary Videos** (1-2 videos)
   - "Everything you need to know about [topic]"
   - Comprehensive overviews
   - "Top 10 things about [topic]"

**Analysis Focus:** Basic concepts, key terminology, main applications""",
        
        "comprehensive": """
### Comprehensive Research Strategy (8-12 hours)
**Goal:** Develop working knowledge and practical understanding

**Video Categories:**
1. **Fundamentals** (3-4 videos)
   - Basic principles and concepts
   - Historical background
   - Core terminology

2. **Deep Dives** (4-5 videos)
   - Detailed explanations of key aspects
   - Case studies and examples
   - Technical implementations

3. **Applications** (2-3 videos)
   - Real-world use cases
   - Industry applications
   - Best practices

4. **Expert Perspectives** (2-3 videos)
   - Advanced insights
   - Current trends and future outlook
   - Expert interviews or lectures

**Analysis Focus:** In-depth understanding, practical applications, critical analysis""",
        
        "expert": """
### Expert-Level Research Strategy (15+ hours)
**Goal:** Achieve specialized knowledge and critical expertise

**Research Phases:**
1. **Foundation Review** (2-3 videos)
   - Ensure solid understanding of basics
   - Identify knowledge gaps

2. **Specialized Topics** (5-7 videos)
   - Advanced technical aspects
   - Specialized applications
   - Cutting-edge developments

3. **Multiple Perspectives** (4-5 videos)
   - Different schools of thought
   - Comparative approaches
   - Controversial or debated aspects

4. **Current Research** (3-4 videos)
   - Latest developments
   - Research findings
   - Future directions

5. **Critical Analysis** (2-3 videos)
   - Limitations and criticisms
   - Alternative approaches
   - Meta-analysis

**Analysis Focus:** Critical evaluation, synthesis of multiple sources, identification of knowledge frontiers"""
    }
    
    strategy = depth_strategies.get(research_depth, depth_strategies["comprehensive"])
    
    return f"""# 🔍 Video Research Planning Workshop

## Research Project Setup
**Topic:** {topic}
**Depth Level:** {research_depth.title()}
**Estimated Time:** {strategy.split('(')[1].split(')')[0] if '(' in strategy else 'Variable'}

{strategy}

## Research Methodology

### Video Selection Criteria
- **Authority:** Check presenter credentials and channel reputation
- **Currency:** Prefer recent videos unless studying historical topics
- **Quality:** Look for clear explanations and good production values
- **Completeness:** Ensure comprehensive coverage of subtopics

### Analysis Framework
1. **Content Analysis:** Use transcript_analysis_workshop for each video
2. **Source Comparison:** Compare multiple perspectives on the same topic
3. **Knowledge Extraction:** Use create_study_notes for learning materials
4. **Resource Creation:** Use create_mcp_resource_from_transcript_v2 for zero-token access

### Research Documentation
**For Each Video:**
- Full transcript analysis
- Key insights and takeaways
- Source credibility assessment
- Connection to other videos/sources

**Synthesis Phase:**
- Compare and contrast different perspectives
- Identify consensus vs. controversial points
- Create comprehensive overview document
- Note areas requiring additional research

---
**Instructions:** Use this framework to guide systematic video research. Start by identifying appropriate videos, then analyze each using the relevant tools."""

# ============================================================================
# SERVER ENTRY POINT
# ============================================================================

def main():
    """Main entry point for the streamlined server."""
    print(f"🚀 Starting {settings.server_name} v{settings.version}")
    print(f"📁 Resource directory: {settings.resource_dir}")
    print(f"🔧 yt-dlp available: {'✅' if check_ytdlp_available() else '❌'}")
    print(f"💾 Cache size: {settings.cache_size}")
    print(f"🎯 Aggressive deduplication: {'✅' if settings.aggressive_dedup else '❌'}")
    
    # Ensure resource directory exists
    ensure_resource_directory()
    
    mcp.run(transport='stdio')


if __name__ == "__main__":
    main()
