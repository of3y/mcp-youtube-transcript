#!/usr/bin/env python3
"""
YouTube Transcript to MCP Resource Tool

This standalone tool extracts YouTube transcripts using yt-dlp and saves them as markdown files
that can be used as MCP resources. It provides debugging capabilities to investigate
potential duplicate line issues.

Usage:
    uv run python scripts/youtube_to_mcp.py <url> [options]
    
Features:
- Extracts transcripts using yt-dlp (reliable on all environments)
- Detects and reports duplicate lines
- Saves clean markdown files for MCP resource usage
- Provides detailed debugging information
- Works as a standalone tool independent of Claude Desktop
- No cloud server blocking issues (unlike youtube-transcript-api)
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
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional, Optional
import html

# Note: This tool now uses only yt-dlp for transcript extraction
# The youtube-transcript-api has been removed due to frequent blocking issues
# on cloud servers and VPS environments.

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

def get_video_metadata(video_url: str) -> Dict[str, Any]:
    """Get video metadata using yt-dlp with enhanced error handling."""
    if not check_ytdlp_available():
        print("⚠️  yt-dlp not available for metadata extraction")
        return {}
    
    try:
        cmd = ['yt-dlp', '--dump-json', '--no-download', video_url]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            metadata = json.loads(result.stdout)
            print(f"✅ Successfully extracted metadata for: {metadata.get('title', 'Unknown Title')}")
            return metadata
        else:
            print(f"❌ yt-dlp metadata extraction failed:")
            print(f"   Return code: {result.returncode}")
            print(f"   Error: {result.stderr}")
            return {}
            
    except subprocess.TimeoutExpired:
        print("⚠️  Metadata extraction timed out after 30 seconds")
        return {}
    except json.JSONDecodeError as e:
        print(f"⚠️  Failed to parse yt-dlp JSON output: {e}")
        return {}
    except Exception as e:
        print(f"⚠️  Could not get video metadata: {e}")
        return {}

def extract_transcript(video_url: str, language: str = "en", metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Extract transcript using yt-dlp with SRV1 format preference and automatic fallback.
    
    This updated version eliminates VTT duplication issues by using srv1 → json3 → ttml → vtt fallback.
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
        temp_dir = tempfile.mkdtemp(prefix="ytdlp_mcp_")
        
        # Use new fallback system instead of hardcoded VTT
        subtitle_file, actual_format = download_subtitles_with_fallback(video_url, language, temp_dir)
        
        # Parse using the appropriate parser
        transcript_lines = parse_subtitle_file(subtitle_file, actual_format)
        
        # Apply deduplication (mainly needed for VTT fallback)
        original_count = len(transcript_lines)
        if actual_format == 'vtt':
            transcript_lines = deduplicate_transcript_lines(transcript_lines)
        
        # Calculate deduplication effectiveness
        dedup_effectiveness = ((original_count - len(transcript_lines)) / original_count * 100) if original_count > 0 else 0
        
        # Calculate quality metrics with video context for enhanced validation
        video_context = {}
        if metadata:
            video_context = {'duration': metadata.get('duration', 0)}
        
        quality_metrics = analyze_transcript_quality(transcript_lines, video_context)
        
        return {
            'method': 'yt-dlp',
            'success': True,
            'format': actual_format,  # Report which format was actually used
            'language': language,
            'lines': transcript_lines,
            'line_count': len(transcript_lines),
            'original_line_count': original_count,
            'deduplication_effectiveness': round(dedup_effectiveness, 1),
            'quality_metrics': quality_metrics
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
        if temp_dir and os.path.exists(temp_dir):
            try:
                shutil.rmtree(temp_dir)
            except:
                pass

def analyze_duplicates(lines: List[str]) -> Dict[str, Any]:
    """Analyze transcript lines for duplicates."""
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
    
    return {
        'total_lines': len(lines),
        'unique_lines': len(seen_lines),
        'duplicate_count': len(duplicates),
        'duplicates': duplicates,
        'line_frequency': line_frequency
    }

def analyze_transcript_quality(lines: List[str], video_info: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Analyze the quality of a transcript with enhanced safety validation."""
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
    
    # Enhanced Quality Validation (NEW)
    quality_warnings = []
    safety_penalties = 0
    
    full_text = ' '.join(text_lines).lower()
    
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
        if total_lines > expected_lines * 2:  # More than double expected
            quality_warnings.append("Transcript length seems excessive for video duration")
            safety_penalties += 10
        elif total_lines < expected_lines * 0.3:  # Less than 30% expected
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
    
    # Punctuation analysis
    punctuation_chars = sum(1 for line in text_lines for char in line if char in '.,!?;:')
    has_punctuation = punctuation_chars > len(text_lines) * 0.1  # At least 10% of lines have punctuation
    
    # Timestamp coverage
    timestamped_lines = sum(1 for line in lines if line.startswith('['))
    timestamp_coverage = timestamped_lines / total_lines if total_lines > 0 else 0
    
    # Calculate enhanced quality score (0-100)
    quality_score = 0
    
    # Line count factor (more lines generally better, up to a point)
    if total_lines > 10:
        quality_score += min(30, total_lines * 0.5)
    
    # Average line length (reasonable length indicates good segmentation)
    avg_line_length = sum(len(line) for line in lines) / total_lines if total_lines > 0 else 0
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
    
    # Legacy duplicate penalty calculation for backward compatibility
    duplicate_penalty = (exact_duplicates + partial_duplicates) / total_lines * 100 if total_lines > 0 else 0
    legacy_quality_score = max(0, 100 - duplicate_penalty)
    
    return {
        'total_lines': total_lines,
        'text_lines': len(text_lines),
        'exact_duplicates': exact_duplicates,
        'partial_duplicates': partial_duplicates,
        'total_words': total_words,
        'avg_words_per_line': round(avg_words_per_line, 1),
        'avg_line_length': round(avg_line_length, 1),
        'has_punctuation': has_punctuation,
        'timestamp_coverage': round(timestamp_coverage, 2),
        'deduplicated_lines': len(deduplicated),
        'reduction_percentage': round(dedupe_reduction, 1),
        'quality_score': round(quality_score, 1),
        'legacy_quality_score': round(legacy_quality_score, 1),  # Keep for comparison
        'safety_penalties': safety_penalties,
        'quality_warnings': quality_warnings,
        'quality_rating': 'Excellent' if quality_score >= 80 else 
                         'Good' if quality_score >= 60 else 
                         'Fair' if quality_score >= 40 else 
                         'Poor' if quality_score >= 20 else 'Very Poor'
    }

def create_mcp_markdown(result: Dict[str, Any], video_url: str, metadata: Dict[str, Any], minimal: bool = False) -> str:
    """Create markdown content optimized for MCP resource usage.
    
    Args:
        result: Transcript extraction result
        video_url: YouTube video URL
        metadata: Video metadata
        minimal: If True, generate minimal format optimized for Claude
    """
    video_id = extract_video_id(video_url)
    title = metadata.get('title', f'Video {video_id}')
    
    if minimal:
        # Minimal format optimized for Claude Desktop
        duration_str = metadata.get('duration_string', 'Unknown')
        channel = metadata.get('uploader', 'Unknown')
        quality_rating = result.get('quality_metrics', {}).get('quality_rating', 'Unknown')
        
        # Generate clean plain text script 
        plain_script = create_plain_text_script(result['lines'], remove_duplicates=True, aggressive_dedup=True)
        
        markdown_content = f"""# {title}

**Channel:** {channel} | **Duration:** {duration_str} | **ID:** {video_id}
**URL:** {video_url}

---

{plain_script}

---
*Extracted: {datetime.now().strftime('%Y-%m-%d')} | Quality: {quality_rating}*
"""
        return markdown_content
    
    # Full format (existing verbose format)
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
    
    # Get enhanced quality analysis from the result
    quality_analysis = result.get('quality_metrics', {})
    
    markdown_content += f"""

## Enhanced Quality Analysis

### Core Metrics
- **Total Lines:** {result.get('original_line_count', result['line_count'])} → {result['line_count']} (after deduplication)
- **Deduplication Effectiveness:** {result.get('deduplication_effectiveness', 0):.1f}%
- **Quality Score:** {quality_analysis.get('quality_score', 0):.1f}%
- **Quality Rating:** {quality_analysis.get('quality_rating', 'Unknown')}
- **Safety Penalties:** -{quality_analysis.get('safety_penalties', 0)} points

### Content Quality
- **Total Words:** {quality_analysis.get('total_words', 0):,}
- **Average Words per Line:** {quality_analysis.get('avg_words_per_line', 0)}
- **Average Line Length:** {quality_analysis.get('avg_line_length', 0)} characters
- **Has Punctuation:** {'Yes ✅' if quality_analysis.get('has_punctuation', False) else 'No ❌'}
- **Timestamp Coverage:** {quality_analysis.get('timestamp_coverage', 0) * 100:.1f}%

### Duplicate Analysis
- **Exact Duplicates:** {quality_analysis.get('exact_duplicates', 0)}
- **Partial Duplicates:** {quality_analysis.get('partial_duplicates', 0)}

"""
    
    # Add quality warnings if any
    quality_warnings = quality_analysis.get('quality_warnings', [])
    if quality_warnings:
        markdown_content += "### 🚨 Quality Warnings\n\n"
        for warning in quality_warnings:
            markdown_content += f"- {warning}\n"
        markdown_content += "\n"
    else:
        markdown_content += "### ✅ Quality Assessment\n\nNo quality concerns detected.\n\n"
    
    # Add recommendations based on quality score
    score = quality_analysis.get('quality_score', 0)
    markdown_content += "### 📋 Recommendations\n\n"
    if score < 40:
        markdown_content += "- ⚠️ Low quality transcript - consider manual review\n"
        markdown_content += "- 🔄 Try extracting with different language settings\n"
    elif score < 60:
        markdown_content += "- ✅ Fair quality transcript - suitable for basic analysis\n"
        markdown_content += "- 📝 May need manual cleanup for detailed work\n"
    else:
        markdown_content += "- ✅ Good quality transcript - suitable for analysis\n"
        markdown_content += "- 🎯 Ready for AI processing and content analysis\n"
    
    if quality_analysis.get('safety_penalties', 0) > 15:
        markdown_content += "- 🔍 Review content carefully due to detected quality issues\n"
    
    markdown_content += "\n"
    
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

def save_mcp_resource(result: Dict[str, Any], video_url: str, metadata: Dict[str, Any], output_dir: str, minimal: bool = False) -> str:
    """Save transcript as MCP-ready markdown resource."""
    try:
        video_id = extract_video_id(video_url)
        title = metadata.get('title', f'Video {video_id}')
        
        # Create safe filename
        safe_title = re.sub(r'[^\w\s-]', '', title).strip()
        safe_title = re.sub(r'[-\s]+', '-', safe_title)[:50]
        
        # Add format indicator to filename for minimal format
        format_suffix = "_minimal" if minimal else ""
        filename = f"{video_id}_{safe_title}{format_suffix}.md"
        filepath = os.path.join(output_dir, filename)
        
        # Create markdown content
        markdown_content = create_mcp_markdown(result, video_url, metadata, minimal)
        
        # Save file
        os.makedirs(output_dir, exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        return filepath
        
    except Exception as e:
        print(f"❌ Error saving MCP resource: {e}")
        return ""

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
        # and last text is not a special caption
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
    # First, split on sentence boundaries
    sentences = re.split(r'(?<=[.!?])\s+', full_text)
    
    # Group sentences into coherent paragraphs
    paragraphs = []
    current_paragraph = []
    
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        
        current_paragraph.append(sentence)
        
        # End paragraph conditions:
        # 1. Have 2-4 sentences and current sentence ends with punctuation
        # 2. Paragraph is getting too long (>300 chars)
        # 3. Topic shift indicators (certain phrases)
        
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

# ============================================================================
# SUBTITLE FORMAT PARSERS (Added in VTT → SRV1 Migration)
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
                minutes = int(start_time // 60)
                seconds = int(start_time % 60)
                timestamp = f"[{minutes:02d}:{seconds:02d}]"
                
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

def main():
    parser = argparse.ArgumentParser(
        description="Extract YouTube transcripts as MCP resources using yt-dlp",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Extract transcript from YouTube video
  uv run python scripts/youtube_to_mcp.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
  
  # Extract with specific language
  uv run python scripts/youtube_to_mcp.py "https://youtu.be/dQw4w9WgXcQ" --lang es
  
  # Save to specific directory
  uv run python scripts/youtube_to_mcp.py "https://youtu.be/dQw4w9WgXcQ" --output ./resources/transcripts
  
  # Generate minimal format optimized for Claude
  uv run python scripts/youtube_to_mcp.py "https://youtu.be/dQw4w9WgXcQ" --minimal
        """
    )
    
    parser.add_argument('video_url', help='YouTube video URL')
    parser.add_argument('--lang', default='en', help='Language code (default: en)')
    parser.add_argument('--output', default='./resources/transcripts', 
                        help='Output directory (default: ./resources/transcripts)')
    parser.add_argument('--debug', action='store_true', help='Enable debug output')
    parser.add_argument('--minimal', action='store_true', 
                        help='Generate minimal format optimized for Claude (less verbose)')
    parser.add_argument('--test-script', action='store_true', 
                        help='Test script generation with current transcript')
    
    args = parser.parse_args()
    
    print(f"🚀 YouTube to MCP Resource Tool")
    print(f"=" * 50)
    print(f"Video: {args.video_url}")
    print(f"Method: yt-dlp (reliable)")
    print(f"Language: {args.lang}")
    print(f"Format: {'Minimal (Claude-optimized)' if args.minimal else 'Full (detailed)'}")
    print(f"Output: {args.output}")
    print()
    
    # Get video metadata
    print("📊 Getting video metadata...")
    metadata = get_video_metadata(args.video_url)
    if metadata:
        print(f"📺 Title: {metadata.get('title', 'Unknown')}")
        print(f"📅 Duration: {metadata.get('duration_string', 'Unknown')}")
        print(f"👤 Channel: {metadata.get('uploader', 'Unknown')}")
    
    # Extract transcript using yt-dlp
    print(f"\n⚙️  Extracting transcript with yt-dlp...")
    result = extract_transcript(args.video_url, args.lang, metadata)
    
    if result['success']:
        print(f"✅ Success: {result['line_count']} lines")
        
        # Display enhanced quality analysis
        quality_metrics = result.get('quality_metrics', {})
        quality_score = quality_metrics.get('quality_score', 0)
        quality_warnings = quality_metrics.get('quality_warnings', [])
        safety_penalties = quality_metrics.get('safety_penalties', 0)
        
        print(f"📊 Quality Score: {quality_score:.1f}% ({quality_metrics.get('quality_rating', 'Unknown')})")
        
        if result.get('deduplication_effectiveness', 0) > 0:
            print(f"🔄 Deduplication: {result.get('deduplication_effectiveness', 0):.1f}% duplicates removed")
        
        if safety_penalties > 0:
            print(f"⚠️  Safety penalties: -{safety_penalties} points")
        
        if quality_warnings:
            print(f"🚨 Quality warnings detected:")
            for warning in quality_warnings[:3]:  # Show first 3 warnings
                print(f"   • {warning}")
            if len(quality_warnings) > 3:
                print(f"   • ... and {len(quality_warnings) - 3} more warnings")
        else:
            print(f"✅ No quality concerns detected")
        
        if args.debug:
            print(f"\n🔍 Debug Info:")
            print(f"   Original lines: {result.get('original_line_count', result['line_count'])}")
            print(f"   Final lines: {result['line_count']}")
            print(f"   Exact duplicates: {quality_metrics.get('exact_duplicates', 0)}")
            print(f"   Partial duplicates: {quality_metrics.get('partial_duplicates', 0)}")
            print(f"   Has punctuation: {quality_metrics.get('has_punctuation', False)}")
            print(f"   Timestamp coverage: {quality_metrics.get('timestamp_coverage', 0) * 100:.1f}%")
        
        # Save MCP resource
        filepath = save_mcp_resource(result, args.video_url, metadata, args.output, args.minimal)
        if filepath:
            print(f"💾 Saved: {os.path.basename(filepath)}")
            print(f"\n" + "=" * 50)
            print(f"🎉 Successfully created MCP resource!")
            print(f"� Check output directory: {args.output}")
            print(f"📝 File is ready for MCP integration")
        else:
            print(f"\n" + "=" * 50)
            print(f"❌ Failed to save MCP resource")
    else:
        print(f"❌ Failed: {result['error']}")
        if args.debug:
            print(f"   Debug: Check if yt-dlp is installed and video has subtitles")
            print(f"   Install yt-dlp with: pip install yt-dlp")
        
        print(f"\n" + "=" * 50)
        print(f"❌ No transcript extracted successfully")
        print(f"💡 Troubleshooting:")
        print(f"   • Ensure yt-dlp is installed: pip install yt-dlp")
        print(f"   • Check that the video has subtitles/captions")
        print(f"   • Try a different language code with --lang")
    
    print(f"=" * 50)

if __name__ == "__main__":
    main()
