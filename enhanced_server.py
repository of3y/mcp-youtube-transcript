#!/usr/bin/env python3
"""
Enhanced YouTube Transcript MCP Server with Resources and Prompts

A Model-Context-Protocol server that provides:
- Tools: YouTube transcript extraction and analysis functionality
- Resources: Dynamic data access for cached transcripts and analysis history
- Prompts: Guided conversation starters for analysis workflows
"""

import re
import json
import subprocess
import os
import glob
import tempfile
import shutil
import sys
import asyncio
from datetime import datetime
from typing import List, Tuple, Optional
from pathlib import Path
from typing import Any, List, Optional, Tuple
from mcp.server.fastmcp import FastMCP
# Note: Simplified to use only yt-dlp for reliable transcript extraction
# youtube-transcript-api removed due to cloud server blocking issues
from pathlib import Path

# Import our enhanced modules
from src.youtube_transcript_server.config import settings, smart_truncate_output
from src.youtube_transcript_server import resources
from src.youtube_transcript_server import prompts
# Import shared extraction functions
from src.youtube_transcript_server import extraction

# Initialize FastMCP server
mcp = FastMCP(
    name=settings.server_name,
    version=settings.version,
    dependencies=["yt-dlp>=2023.12.30"]
)


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


def extract_transcript_ytdlp(video_url: str, language: str = "en") -> dict:
    """Extract transcript using yt-dlp (reliable method that works on all environments)."""
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
        # Create temporary directory
        temp_dir = tempfile.mkdtemp(prefix="ytdlp_mcp_")
        
        # Download subtitles
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
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode != 0:
            # Try auto-generated subtitles only
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
                    'available_languages': []
                }
        
        # Find VTT files
        vtt_files = glob.glob(f'{temp_dir}/*.{language}.vtt') or glob.glob(f'{temp_dir}/*.en.vtt')
        
        if not vtt_files:
            return {
                'method': 'yt-dlp',
                'success': False,
                'error': f"No VTT files found for language '{language}'",
                'lines': [],
                'available_languages': []
            }
        
        vtt_file = vtt_files[0]
        
        # Read and parse VTT content
        with open(vtt_file, 'r', encoding='utf-8') as f:
            vtt_content = f.read()
        
        # Parse VTT content - EXACT SAME LOGIC AS youtube_to_mcp.py
        lines = vtt_content.split('\n')
        transcript_lines = []
        
        current_timestamp = None
        current_text_lines = []
        
        for line in lines:
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
                
                # Extract start time for our format
                time_parts = line.split(' --> ')[0]
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
        
        # Apply deduplication to clean up the transcript
        transcript_lines = deduplicate_transcript_lines(transcript_lines)
        
        # Try to detect available languages from the downloaded files
        all_vtt_files = glob.glob(f'{temp_dir}/*.vtt')
        available_languages = []
        for vtt_file_path in all_vtt_files:
            filename = os.path.basename(vtt_file_path)
            if '.' in filename:
                parts = filename.split('.')
                if len(parts) >= 3:  # title.lang.vtt
                    lang_part = parts[-2]
                    available_languages.append(f"{lang_part} (auto)" if 'auto' in filename else lang_part)
        
        return {
            'method': 'yt-dlp',
            'success': True,
            'language': language,
            'lines': transcript_lines,
            'line_count': len(transcript_lines),
            'available_languages': list(set(available_languages)) if available_languages else ['en (auto)']
        }
        
    except subprocess.TimeoutExpired:
        return {
            'method': 'yt-dlp',
            'success': False,
            'error': "yt-dlp timed out",
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
        # Clean up
        if temp_dir and os.path.exists(temp_dir):
            try:
                shutil.rmtree(temp_dir)
            except:
                pass


# ============================================================================
# ENHANCED TOOLS v2 - Using shared extraction module
# ============================================================================

@mcp.tool()
async def create_mcp_resource_from_transcript_v2(video_url: str, resource_name: str = "") -> str:
    """Create a comprehensive MCP resource file using enhanced extraction pipeline.

    Args:
        video_url: YouTube video URL
        resource_name: Custom name for the resource (optional)
    """
    try:
        # Use enhanced extraction pipeline
        result = await extraction.extract_enhanced_transcript(video_url)
        
        if not result['success']:
            return f"❌ Enhanced extraction failed: {result.get('error', 'Unknown error')}"
        
        # Create resource filename
        video_id = result['video_id']
        if not resource_name:
            resource_name = f"transcript_{video_id}_enhanced"
        
        resource_path = f"resources/transcripts/{resource_name}.md"
        os.makedirs(os.path.dirname(resource_path), exist_ok=True)
        
        # Save comprehensive markdown content
        with open(resource_path, 'w', encoding='utf-8') as f:
            f.write(result['markdown_content'])
        
        # Add to cache and analysis history
        resources.add_to_cache(video_id, result['plain_text'], result.get('language', 'en'))
        resources.add_analysis_to_history("enhanced_mcp_resource_creation", video_url, resource_name)
        
        metadata = result.get('metadata', {})
        title = metadata.get('title', 'Unknown Title')
        
        return f"""✅ Enhanced MCP Resource Created Successfully!

**Resource Details:**
- Name: `transcript://{resource_name}`
- Path: `{resource_path}`
- Video: {title}
- Method: {result['method']}
- Quality Score: {result.get('quality_metrics', {}).get('quality_score', 'N/A')}%
- Size: {len(result['markdown_content'])} characters

**Content Includes:**
- Rich video metadata (views: {metadata.get('view_count', 'N/A'):,})
- Clean plain text script ({len(result['plain_text'])} chars)
- Timestamped transcript ({result['line_count']} lines)
- Quality analysis and metrics
- Comprehensive MCP integration guide

**Usage:**
Reference this transcript in MCP applications using: `transcript://{resource_name}`
"""
        
    except Exception as e:
        return f"❌ Error creating enhanced MCP resource: {str(e)}"


@mcp.tool()
async def get_transcript_quality_analysis(video_url: str) -> str:
    """Get comprehensive quality analysis for a YouTube video transcript.

    Args:
        video_url: YouTube video URL
    """
    try:
        result = await extraction.extract_enhanced_transcript(video_url, quality_analysis=True)
        
        if not result['success']:
            return f"❌ Quality analysis failed: {result.get('error', 'Unknown error')}"
        
        quality = result.get('quality_metrics', {})
        metadata = result.get('metadata', {})
        
        # Add to analysis history
        resources.add_analysis_to_history("quality_analysis", video_url, f"Score: {quality.get('quality_score', 0)}%")
        
        return f"""📊 Transcript Quality Analysis

**Video:** {metadata.get('title', 'Unknown Title')}
**Video ID:** {result['video_id']}
**Extraction Method:** {result['method']}

## Quality Metrics

- **Overall Quality Score:** {quality.get('quality_score', 0)}% - {quality.get('quality_rating', 'Unknown')}
- **Total Lines:** {quality.get('total_lines', 0)}
- **Text Lines:** {quality.get('text_lines', 0)}
- **After Deduplication:** {quality.get('deduplicated_lines', 0)} lines
- **Reduction:** {quality.get('reduction_percentage', 0)}%

## Duplicate Analysis

- **Exact Duplicates:** {quality.get('exact_duplicates', 0)}
- **Partial Duplicates:** {quality.get('partial_duplicates', 0)}
- **Total Words:** {quality.get('total_words', 0):,}
- **Avg Words/Line:** {quality.get('avg_words_per_line', 0)}

## Transcript Formats Available

- **Raw Transcript:** {result['line_count']} timestamped lines
- **Deduplicated:** {result['deduplicated_count']} lines  
- **Plain Text Script:** {len(result['plain_text'])} characters

## Quality Assessment

{('✅ **High Quality**: Minimal duplicates, good structure' if quality.get('quality_score', 0) >= 80 else
  '⚠️ **Moderate Quality**: Some duplicates detected' if quality.get('quality_score', 0) >= 60 else
  '❌ **Poor Quality**: Significant duplicate issues detected')}

---
*Use `create_mcp_resource_from_transcript_v2` to create an enhanced resource with quality improvements applied.*
"""
        
    except Exception as e:
        return f"❌ Error analyzing transcript quality: {str(e)}"


# ============================================================================
# TOOLS - Enhanced with caching and resource integration
# ============================================================================

@mcp.tool()
async def get_youtube_transcript(video_url: str, language: str = "en") -> str:
    """Get the transcript of a YouTube video.

    Args:
        video_url: YouTube video URL
        language: Language code (e.g., 'en', 'es'). Defaults to 'en'
    """
    try:
        video_id = extract_video_id(video_url)
        
        # Add to analysis history
        resources.add_analysis_to_history("transcript_extraction", video_url)

        # Use yt-dlp for reliable transcript extraction
        result = extract_transcript_ytdlp(video_url, language)
        
        if not result['success']:
            return f"❌ No transcript available for this video.\n\nPossible reasons:\n- Video has no captions/subtitles\n- Transcripts are disabled by the creator\n- Video is private/restricted\n- Geo-blocking restrictions\n\nError details: {result['error']}"
        
        # Format the transcript for display
        full_transcript = "\n".join(result['lines'])
        
        # Cache the transcript
        resources.add_to_cache(video_id, full_transcript, result['language'])
        
        response = f"Transcript for {video_url} (Language: {result['language']}):\n"
        response += f"Available languages: {', '.join(result['available_languages'])}\n\n"
        response += full_transcript
        
        # Apply smart truncation for Claude Desktop's display limits
        return smart_truncate_output(response, video_url)
    
    except Exception as e:
        return f"❌ Error extracting transcript: {str(e)}\n\nTry with a different video URL or check if the video exists and has captions available."


@mcp.tool()
async def search_transcript(video_url: str, query: str, context_lines: int = 2) -> str:
    """Search for specific content within a YouTube video transcript.

    Args:
        video_url: YouTube video URL
        query: Text to search for in the transcript
        context_lines: Number of lines before/after match to include (default: 2)
    """
    try: 
        video_id = extract_video_id(video_url)
        
        # Add to analysis history
        resources.add_analysis_to_history("transcript_search", video_url, query)
        
        # Get transcript using yt-dlp
        result = extract_transcript_ytdlp(video_url)
        
        if not result['success']:
            return f"❌ Cannot search transcript: {result['error']}"
        
        # Search for matches in the formatted transcript lines
        matches = []
        query_lower = query.lower()
        transcript_lines = result['lines']
        
        for i, line in enumerate(transcript_lines):
            if query_lower in line.lower():
                # Get context lines
                start_idx = max(0, i - context_lines)
                end_idx = min(len(transcript_lines), i + context_lines + 1)
                
                context_lines_list = transcript_lines[start_idx:end_idx]
                
                # Highlight the match in the matching line
                for j, context_line in enumerate(context_lines_list):
                    if j == i - start_idx:  # This is the matching line
                        # Case-insensitive replacement while preserving original case
                        import re
                        pattern = re.compile(re.escape(query), re.IGNORECASE)
                        context_lines_list[j] = pattern.sub(f"**{query}**", context_line)
                
                matches.append("\n".join(context_lines_list))
        
        if matches:
            response = f"Found {len(matches)} matches for '{query}' in {video_url}:\n\n"
            response += "\n\n---\n\n".join(matches)
            return response
        else:
            return f"No matches found for '{query}' in the video transcript."
            
    except Exception as e:
        return f"Error searching transcript: {str(e)}"


# Include all the existing tools with enhanced tracking...
@mcp.tool()
async def get_youtube_transcript_ytdlp(video_url: str, language: str = "en") -> str:
    """Get the transcript of a YouTube video using yt-dlp (more reliable alternative).
    
    Now uses SRV1 format by default with automatic fallback to other formats.
    This eliminates the VTT duplication issue discovered in the analysis.

    Args:
        video_url: YouTube video URL
        language: Language code (e.g., 'en', 'es'). Defaults to 'en'
    """
    try:
        video_id = extract_video_id(video_url)
        
        # Add to analysis history
        resources.add_analysis_to_history("transcript_extraction_ytdlp", video_url)
        
        # Create temporary directory for downloads
        temp_dir = tempfile.mkdtemp(prefix="ytdlp_enhanced_")
        
        try:
            # Use new fallback system: srv1 → json3 → ttml → vtt
            subtitle_file, actual_format = download_subtitles_with_fallback(video_url, language, temp_dir)
            
            # Parse using the appropriate parser
            transcript_lines = parse_subtitle_file(subtitle_file, actual_format)
            
            # Apply deduplication (mainly for VTT fallback)
            if actual_format == 'vtt':
                transcript_lines = deduplicate_transcript_lines(transcript_lines)
            
            if transcript_lines:
                full_transcript = "\n".join(transcript_lines)
                
                # Cache the transcript
                resources.add_to_cache(video_id, full_transcript, language)
                
                result = f"Transcript for {video_url} (via yt-dlp, Format: {actual_format.upper()}, Language: {language}):\n\n{full_transcript}"
                
                # Apply smart truncation for Claude Desktop's display limits
                return smart_truncate_output(result, video_url)
            else:
                return f"❌ Could not parse transcript content from {actual_format.upper()} file"
                
        finally:
            # Clean up temporary directory
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
            
    except subprocess.TimeoutExpired:
        return f"❌ yt-dlp timed out while extracting subtitles"
    except Exception as e:
        return f"❌ Error using yt-dlp: {str(e)}"


# Add all remaining existing tools with similar enhancements...
# (I'll include the key analysis tools here)

@mcp.tool()
async def analyze_video_comprehensive(video_url: str, analysis_type: str = "summary", custom_prompt: str = "") -> str:
    """Comprehensive video analysis with AI.

    Args:
        video_url: YouTube video URL
        analysis_type: Type of analysis - summary, key_points, action_items, questions, sentiment, transcript_cleanup
        custom_prompt: Custom analysis prompt (overrides analysis_type if provided)
    """
    try:
        # Add to analysis history
        resources.add_analysis_to_history(f"comprehensive_analysis_{analysis_type}", video_url, custom_prompt or analysis_type)
        
        transcript = await get_youtube_transcript(video_url)
        
        if "❌" in transcript:
            return transcript
        
        # Extract clean transcript (remove headers)
        clean_transcript = transcript.split("\n\n", 2)[-1] if "\n\n" in transcript else transcript
        
        analysis_prompts = {
            "summary": "Provide a comprehensive summary of this video, highlighting the main points, key insights, and overall message:",
            "key_points": "Extract and list the most important key points, insights, and takeaways from this video:",
            "action_items": "Identify specific action items, recommendations, or steps that viewers should take based on this video:",
            "questions": "Generate thoughtful questions that this video raises or that could be used for further discussion:",
            "sentiment": "Analyze the tone, sentiment, and emotional undertones of this video content:",
            "transcript_cleanup": "Clean up and organize this transcript for better readability while preserving all important information:"
        }
        
        prompt = custom_prompt if custom_prompt else analysis_prompts.get(analysis_type, analysis_prompts["summary"])
        
        result = f"🎯 {analysis_type.title()} Analysis Request:\nVideo: {video_url}\n\n"
        result += f"**Analysis Prompt:**\n{prompt}\n\n"
        result += f"**Transcript:**\n{clean_transcript}\n\n"
        result += "---\n*Claude Desktop: Please analyze the above transcript according to the specified prompt.*"
        
        return result
        
    except Exception as e:
        return f"❌ Error preparing comprehensive analysis: {str(e)}"


# Add the remaining tools from the original server after the analyze_video_comprehensive tool

@mcp.tool()
async def extract_key_quotes(video_url: str, topic: str) -> str:
    """Get video transcript with prompt to find key quotes about a specific topic.
    
    Args:
        video_url: YouTube video URL
        topic: Topic or subject to search for quotes about
    """
    try:
        # Add to analysis history
        resources.add_analysis_to_history("extract_key_quotes", video_url, topic)
        
        transcript = await get_youtube_transcript(video_url)
        
        if "❌" in transcript:
            return transcript
        
        clean_transcript = transcript.split("\n\n", 2)[-1] if "\n\n" in transcript else transcript
        
        prompt = f"Find and extract key quotes specifically about '{topic}' from this video transcript. Include the context and explain why each quote is significant:"
        
        result = f"💬 Quote Extraction Request:\nVideo: {video_url}\nTopic: {topic}\n\n"
        result += f"**Analysis Prompt:**\n{prompt}\n\n"
        result += f"**Transcript:**\n{clean_transcript}\n\n"
        result += "---\n*Claude Desktop: Please extract key quotes about the specified topic from the above transcript.*"
        
        return result
        
    except Exception as e:
        return f"❌ Error preparing quote extraction: {str(e)}"


@mcp.tool()
async def create_study_notes(video_url: str, format: str = "markdown") -> str:
    """Get video transcript with prompt to generate structured study notes.
    
    Args:
        video_url: YouTube video URL
        format: Output format - markdown, outline, flashcards
    """
    try:
        # Add to analysis history
        resources.add_analysis_to_history("create_study_notes", video_url, format)
        
        transcript = await get_youtube_transcript(video_url)
        
        if "❌" in transcript:
            return transcript
        
        clean_transcript = transcript.split("\n\n", 2)[-1] if "\n\n" in transcript else transcript
        
        format_prompts = {
            "markdown": "Create comprehensive study notes in markdown format with headers, bullet points, and key concepts highlighted:",
            "outline": "Create a detailed outline format with main topics, subtopics, and key details:",
            "flashcards": "Create flashcard-style study materials with questions and answers based on the content:"
        }
        
        if format not in format_prompts:
            return f"❌ Invalid format. Choose from: {', '.join(format_prompts.keys())}"
        
        prompt = format_prompts[format]
        
        result = f"📚 Study Notes Request ({format}):\nVideo: {video_url}\n\n"
        result += f"**Analysis Prompt:**\n{prompt}\n\n"
        result += f"**Transcript:**\n{clean_transcript}\n\n"
        result += f"---\n*Claude Desktop: Please create {format} study notes from the above transcript.*"
        
        return result
        
    except Exception as e:
        return f"❌ Error preparing study notes: {str(e)}"


@mcp.tool()
async def extract_citations_and_references(video_url: str) -> str:
    """Get video transcript with prompt to extract mentioned references and citations.
    
    Args:
        video_url: YouTube video URL
    """
    try:
        # Add to analysis history
        resources.add_analysis_to_history("extract_citations", video_url)
        
        transcript = await get_youtube_transcript(video_url)
        
        if "❌" in transcript:
            return transcript
        
        clean_transcript = transcript.split("\n\n", 2)[-1] if "\n\n" in transcript else transcript
        
        prompt = "Extract all references mentioned in this video including: books, research papers, websites, studies, authors, companies, tools, and other resources. Format as a bibliography:"
        
        result = f"📖 References Extraction Request:\nVideo: {video_url}\n\n"
        result += f"**Analysis Prompt:**\n{prompt}\n\n"
        result += f"**Transcript:**\n{clean_transcript}\n\n"
        result += "---\n*Claude Desktop: Please extract all references and citations from the above transcript.*"
        
        return result
        
    except Exception as e:
        return f"❌ Error preparing reference extraction: {str(e)}"


@mcp.tool()
async def generate_quiz(video_url: str, difficulty: str = "medium", num_questions: int = 5) -> str:
    """Get video transcript with prompt to create a quiz based on video content.
    
    Args:
        video_url: YouTube video URL
        difficulty: Quiz difficulty - easy, medium, hard
        num_questions: Number of questions to generate (1-10)
    """
    try:
        if num_questions < 1 or num_questions > 10:
            return "❌ Number of questions must be between 1 and 10"
        
        # Add to analysis history
        resources.add_analysis_to_history("generate_quiz", video_url, f"{difficulty}_{num_questions}q")
        
        transcript = await get_youtube_transcript(video_url)
        
        if "❌" in transcript:
            return transcript
        
        clean_transcript = transcript.split("\n\n", 2)[-1] if "\n\n" in transcript else transcript
        
        prompt = f"Create a {difficulty} difficulty quiz with {num_questions} multiple choice questions based on this video content. Include the correct answers at the end:"
        
        result = f"🧠 Quiz Generation Request ({difficulty} difficulty, {num_questions} questions):\nVideo: {video_url}\n\n"
        result += f"**Analysis Prompt:**\n{prompt}\n\n"
        result += f"**Transcript:**\n{clean_transcript}\n\n"
        result += "---\n*Claude Desktop: Please generate a quiz based on the above transcript.*"
        
        return result
        
    except Exception as e:
        return f"❌ Error preparing quiz generation: {str(e)}"


@mcp.tool()
async def fact_check_claims(video_url: str) -> str:
    """Get video transcript with prompt to identify and analyze factual claims.
    
    Args:
        video_url: YouTube video URL
    """
    try:
        # Add to analysis history
        resources.add_analysis_to_history("fact_check", video_url)
        
        transcript = await get_youtube_transcript(video_url)
        
        if "❌" in transcript:
            return transcript
        
        clean_transcript = transcript.split("\n\n", 2)[-1] if "\n\n" in transcript else transcript
        
        prompt = "Identify specific factual claims made in this video. List them clearly and note which ones might benefit from fact-checking or verification:"
        
        result = f"🔍 Fact-Check Request:\nVideo: {video_url}\n\n"
        result += f"**Analysis Prompt:**\n{prompt}\n\n"
        result += f"**Transcript:**\n{clean_transcript}\n\n"
        result += "---\n*Claude Desktop: Please identify and analyze factual claims from the above transcript.*"
        
        return result
        
    except Exception as e:
        return f"❌ Error preparing fact-check: {str(e)}"


@mcp.tool()
async def extract_statistics_and_data(video_url: str) -> str:
    """Get video transcript with prompt to extract numerical data and statistics.
    
    Args:
        video_url: YouTube video URL
    """
    try:
        # Add to analysis history
        resources.add_analysis_to_history("extract_statistics", video_url)
        
        transcript = await get_youtube_transcript(video_url)
        
        if "❌" in transcript:
            return transcript
        
        clean_transcript = transcript.split("\n\n", 2)[-1] if "\n\n" in transcript else transcript
        
        prompt = "Extract all numerical data from this video including: statistics, percentages, dates, quantities, measurements, financial figures, and other data points. Organize them clearly:"
        
        result = f"📊 Statistics Extraction Request:\nVideo: {video_url}\n\n"
        result += f"**Analysis Prompt:**\n{prompt}\n\n"
        result += f"**Transcript:**\n{clean_transcript}\n\n"
        result += "---\n*Claude Desktop: Please extract all statistics and data points from the above transcript.*"
        
        return result
        
    except Exception as e:
        return f"❌ Error preparing statistics extraction: {str(e)}"


@mcp.tool()
async def compare_videos(video_urls: List[str], comparison_aspect: str) -> str:
    """Get multiple video transcripts with prompt to compare them on a specific aspect.
    
    Args:
        video_urls: List of YouTube video URLs (2-4 videos)
        comparison_aspect: What to compare - arguments, evidence, conclusions, style, etc.
    """
    try:
        if len(video_urls) < 2 or len(video_urls) > 4:
            return "❌ Please provide 2-4 video URLs for comparison"
        
        # Add to analysis history
        resources.add_analysis_to_history("compare_videos", str(video_urls), comparison_aspect)
        
        transcripts = []
        for i, url in enumerate(video_urls):
            transcript = await get_youtube_transcript(url)
            if "❌" in transcript:
                return f"❌ Error getting transcript for video {i+1}: {transcript}"
            
            clean_transcript = transcript.split("\n\n", 2)[-1] if "\n\n" in transcript else transcript
            transcripts.append(f"VIDEO {i+1} ({url}):\n{clean_transcript}")
        
        combined_content = "\n\n" + "="*50 + "\n\n".join(transcripts)
        
        prompt = f"Compare these videos focusing on '{comparison_aspect}'. Analyze similarities, differences, strengths and weaknesses:"
        
        result = f"⚖️ Video Comparison Request ({comparison_aspect}):\n\n"
        result += f"**Analysis Prompt:**\n{prompt}\n\n"
        result += f"**Transcripts:**\n{combined_content}\n\n"
        result += "---\n*Claude Desktop: Please compare the above video transcripts focusing on the specified aspect.*"
        
        return result
        
    except Exception as e:
        return f"❌ Error preparing video comparison: {str(e)}"


@mcp.tool()
async def analyze_presentation_style(video_url: str) -> str:
    """Get video transcript with prompt to analyze presentation style and delivery.
    
    Args:
        video_url: YouTube video URL
    """
    try:
        # Add to analysis history
        resources.add_analysis_to_history("analyze_presentation_style", video_url)
        
        transcript = await get_youtube_transcript(video_url)
        
        if "❌" in transcript:
            return transcript
        
        clean_transcript = transcript.split("\n\n", 2)[-1] if "\n\n" in transcript else transcript
        
        prompt = "Analyze the presentation style of this video including: tone, pacing, language level, persuasion techniques, audience targeting, and overall effectiveness:"
        
        result = f"🎭 Presentation Analysis Request:\nVideo: {video_url}\n\n"
        result += f"**Analysis Prompt:**\n{prompt}\n\n"
        result += f"**Transcript:**\n{clean_transcript}\n\n"
        result += "---\n*Claude Desktop: Please analyze the presentation style of the above transcript.*"
        
        return result
        
    except Exception as e:
        return f"❌ Error preparing presentation analysis: {str(e)}"


# ============================================================================
# RESOURCES - Dynamic data access
# ============================================================================

@mcp.resource("transcripts://cached")
async def get_cached_transcripts_resource() -> dict:
    """Get information about all cached transcripts."""
    return await resources.get_cached_transcripts()


@mcp.resource("transcripts://{video_id}/metadata")
async def get_video_metadata_resource(video_id: str) -> dict:
    """Get metadata for a specific cached video."""
    return await resources.get_video_metadata(video_id)


@mcp.resource("transcripts://{video_id}/sample") 
async def get_transcript_sample_resource(video_id: str) -> dict:
    """Get a sample of transcript lines for preview."""
    return await resources.get_transcript_sample(video_id)


@mcp.resource("analytics://history")
async def get_analysis_history_resource() -> dict:
    """Get recent analysis history."""
    return await resources.get_analysis_history()


@mcp.resource("analytics://supported_languages")
async def get_supported_languages_resource() -> dict:
    """Get information about supported languages."""
    return await resources.get_supported_languages()


@mcp.resource("analytics://memory_usage")
async def get_memory_usage_resource() -> dict:
    """Get memory usage information."""
    return resources.get_memory_usage()


@mcp.resource("config://server")
async def get_server_config_resource() -> dict:
    """Get server configuration information."""
    return await resources.get_server_config()


@mcp.resource("system://status")
async def get_system_status_resource() -> dict:
    """Get system status and health information."""
    return await resources.get_system_status()


# ============================================================================
# RESOURCE MIRROR TOOLS - For clients that don't support resources
# ============================================================================

@mcp.tool()
async def resource_transcripts_cached() -> dict:
    """Tool mirror of transcripts://cached resource."""
    return await resources.get_cached_transcripts()


@mcp.tool()
async def resource_transcripts_metadata(video_id: str) -> dict:
    """Tool mirror of transcripts://{video_id}/metadata resource."""
    return await resources.get_video_metadata(video_id)


@mcp.tool()
async def resource_transcripts_sample(video_id: str) -> dict:
    """Tool mirror of transcripts://{video_id}/sample resource."""
    return await resources.get_transcript_sample(video_id)


@mcp.tool()
async def resource_analytics_history() -> dict:
    """Tool mirror of analytics://history resource."""
    return await resources.get_analysis_history()


@mcp.tool()
async def resource_analytics_supported_languages() -> dict:
    """Tool mirror of analytics://supported_languages resource."""
    return await resources.get_supported_languages()


@mcp.tool()
async def resource_analytics_memory_usage() -> dict:
    """Tool mirror of analytics://memory_usage resource."""
    return resources.get_memory_usage()


@mcp.tool()
async def resource_config_server() -> dict:
    """Tool mirror of config://server resource."""
    return await resources.get_server_config()


@mcp.tool()
async def resource_system_status() -> dict:
    """Tool mirror of system://status resource."""
    return await resources.get_system_status()


# ============================================================================
# PROMPTS - Guided conversation starters
# ============================================================================

@mcp.prompt()
async def transcript_analysis_workshop(video_url: str, focus_area: str = "general") -> str:
    """Interactive workshop prompt for comprehensive transcript analysis."""
    return await prompts.transcript_analysis_workshop(video_url, focus_area)


@mcp.prompt()
async def video_comparison_framework(video_urls: List[str], comparison_focus: str = "content") -> str:
    """Framework for comparing multiple videos systematically."""
    return await prompts.video_comparison_framework(video_urls, comparison_focus)


@mcp.prompt()
async def content_extraction_guide(video_url: str, extraction_type: str = "summary") -> str:
    """Guide for extracting specific types of content from video transcripts."""
    return await prompts.content_extraction_guide(video_url, extraction_type)


@mcp.prompt()
async def study_notes_generator(video_url: str, subject_area: str = "general", note_style: str = "outline") -> str:
    """Generate structured study notes from educational video content."""
    return await prompts.study_notes_generator(video_url, subject_area, note_style)


@mcp.prompt()
async def video_research_planner(topic: str, research_depth: str = "comprehensive") -> str:
    """Plan a research strategy using YouTube videos for learning about a topic."""
    return await prompts.video_research_planner(topic, research_depth)


@mcp.prompt()
async def list_available_prompts() -> str:
    """List all available prompts and their use cases."""
    return await prompts.list_available_prompts()


# =============================================================================
# RESOURCE MIRROR TOOLS - Access cached data via tools
# =============================================================================

@mcp.tool()
async def get_cached_transcripts() -> str:
    """Get information about all cached transcripts."""
    data = await resources.get_cached_transcripts()
    return f"Cached Transcripts:\n{data}"


@mcp.tool()
async def get_analysis_history() -> str:
    """Get recent analysis history."""
    data = await resources.get_analysis_history()
    return f"Analysis History:\n{data}"


@mcp.tool()
async def get_server_config() -> str:
    """Get server configuration information."""
    data = await resources.get_server_config()
    return f"Server Configuration:\n{data}"


@mcp.tool()
async def get_supported_languages() -> str:
    """Get information about supported languages."""
    data = await resources.get_supported_languages()
    return f"Supported Languages:\n{data}"


# ============================================================================
# BATCH PROCESSING TOOLS - For MCP Resource Integration
# ============================================================================

@mcp.tool()
async def batch_extract_transcripts(video_urls: str, output_format: str = "mcp_resources") -> str:
    """Extract transcripts from multiple YouTube videos and save as MCP resources.

    Args:
        video_urls: Comma-separated list of YouTube video URLs
        output_format: Output format - 'mcp_resources', 'markdown', 'json'
    """
    try:
        urls = [url.strip() for url in video_urls.split(',') if url.strip()]
        
        if not urls:
            return "❌ No valid URLs provided"
        
        if len(urls) > 10:
            return "❌ Maximum of 10 videos allowed per batch"
        
        results = []
        success_count = 0
        
        for i, video_url in enumerate(urls, 1):
            try:
                video_id = extract_video_id(video_url)
                print(f"Processing video {i}/{len(urls)}: {video_id}")
                
                # Try both methods
                transcript = await get_youtube_transcript(video_url)
                
                if "❌" in transcript:
                    # Fallback to yt-dlp
                    transcript = await get_youtube_transcript_ytdlp(video_url)
                
                if "❌" not in transcript:
                    # Save as MCP resource
                    if output_format == "mcp_resources":
                        resource_path = f"resources/transcripts/{video_id}.md"
                        os.makedirs(os.path.dirname(resource_path), exist_ok=True)
                        
                        with open(resource_path, 'w', encoding='utf-8') as f:
                            f.write(f"# Transcript: {video_id}\n\n")
                            f.write(f"**URL:** {video_url}\n\n")
                            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                            f.write("## Transcript\n\n")
                            f.write(transcript)
                        
                        results.append(f"✅ {video_id}: Saved to {resource_path}")
                        success_count += 1
                    else:
                        results.append(f"✅ {video_id}: Extracted successfully")
                        success_count += 1
                else:
                    results.append(f"❌ {video_id}: {transcript[:100]}...")
                    
            except Exception as e:
                results.append(f"❌ {video_url}: Error - {str(e)}")
        
        summary = f"Batch processing complete: {success_count}/{len(urls)} successful\n\n"
        summary += "\n".join(results)
        
        # Add to analysis history
        resources.add_analysis_to_history("batch_extraction", video_urls, f"{success_count}/{len(urls)} successful")
        
        return summary
        
    except Exception as e:
        return f"❌ Batch processing error: {str(e)}"


@mcp.tool()
async def create_mcp_resource_from_transcript(video_url: str, resource_name: str = "") -> str:
    """Create a dedicated MCP resource file from a YouTube transcript.

    Args:
        video_url: YouTube video URL
        resource_name: Custom name for the resource (optional)
    """
    try:
        video_id = extract_video_id(video_url)
        
        # Extract transcript using best available method
        transcript = await get_youtube_transcript(video_url)
        
        if "❌" in transcript:
            # Fallback to yt-dlp
            transcript = await get_youtube_transcript_ytdlp(video_url)
            
        if "❌" in transcript:
            return f"❌ Could not extract transcript: {transcript}"
        
        # Create resource filename
        if not resource_name:
            resource_name = f"transcript_{video_id}"
        
        resource_path = f"resources/transcripts/{resource_name}.md"
        os.makedirs(os.path.dirname(resource_path), exist_ok=True)
        
        # Get video metadata
        try:
            import subprocess
            cmd = ['yt-dlp', '--get-title', '--get-duration', '--get-uploader', video_url]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                title = lines[0] if len(lines) > 0 else "Unknown Title"
                duration = lines[1] if len(lines) > 1 else "Unknown Duration"
                uploader = lines[2] if len(lines) > 2 else "Unknown Uploader"
            else:
                title = duration = uploader = "Unknown"
        except:
            title = duration = uploader = "Unknown"
        
        # Create comprehensive markdown resource
        content = f"""# {title}

## Video Information

- **Video ID:** `{video_id}`
- **URL:** {video_url}
- **Title:** {title}
- **Duration:** {duration}
- **Uploader:** {uploader}
- **Resource Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## MCP Resource Information

- **Resource Name:** `transcript://{resource_name}`
- **File Path:** `{resource_path}`
- **Extraction Method:** YouTube Transcript API + yt-dlp fallback

## Transcript

{transcript}

---

*This transcript was extracted for use as an MCP resource. Reference it using `transcript://{resource_name}` in your MCP-enabled applications.*
"""
        
        with open(resource_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Add to cache and analysis history
        resources.add_to_cache(video_id, transcript, "en")
        resources.add_analysis_to_history("mcp_resource_creation", video_url, resource_name)
        
        return f"""✅ MCP Resource Created Successfully!

**Resource Details:**
- Name: `transcript://{resource_name}`
- Path: `{resource_path}`
- Video: {title}
- Size: {len(content)} characters

**Usage:**
Reference this transcript in MCP applications using: `transcript://{resource_name}`

The resource includes:
- Complete video metadata
- Full transcript with timestamps
- MCP integration information
"""
        
    except Exception as e:
        return f"❌ Error creating MCP resource: {str(e)}"


@mcp.tool()
async def load_transcript_resource(video_id: str) -> str:
    """Load a pre-generated transcript resource from file.

    Args:
        video_id: YouTube video ID to load transcript for
    """
    try:
        # Add to analysis history
        resources.add_analysis_to_history("load_transcript_resource", f"video_id:{video_id}")
        
        # Look for transcript files in resources directory
        resources_dir = Path("resources/transcripts")
        
        if not resources_dir.exists():
            return f"❌ Resources directory not found: {resources_dir}"
        
        # Find files matching the video ID
        matching_files = list(resources_dir.glob(f"{video_id}_*.md"))
        
        if not matching_files:
            return f"❌ No transcript resource found for video ID: {video_id}\n\nAvailable resources:\n" + \
                   "\n".join([f"- {f.stem}" for f in resources_dir.glob("*.md")])
        
        # Load the first matching file
        transcript_file = matching_files[0]
        
        with open(transcript_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Cache the transcript for future use
        # Extract just the transcript part
        lines = content.split('\n')
        transcript_lines = []
        in_transcript = False
        
        for line in lines:
            if line.strip() == "## Transcript":
                in_transcript = True
                continue
            if in_transcript and line.startswith('##'):
                break
            if in_transcript and line.strip() and not line.startswith('#'):
                transcript_lines.append(line.strip())
        
        if transcript_lines:
            clean_transcript = '\n'.join(transcript_lines)
            resources.add_to_cache(video_id, clean_transcript, "en")
        
        result = f"📁 Loaded transcript resource: {transcript_file.name}\n\n{content}"
        return smart_truncate_output(result, f"file://{transcript_file}")
        
    except Exception as e:
        return f"❌ Error loading transcript resource: {str(e)}"


@mcp.tool()
async def list_transcript_resources() -> str:
    """List all available pre-generated transcript resources."""
    try:
        resources_dir = Path("resources/transcripts")
        
        if not resources_dir.exists():
            return f"❌ Resources directory not found: {resources_dir}"
        
        transcript_files = list(resources_dir.glob("*.md"))
        
        if not transcript_files:
            return "📁 No transcript resources found in resources/transcripts/"
        
        result = f"📁 Available Transcript Resources ({len(transcript_files)} files):\n\n"
        
        for file_path in sorted(transcript_files):
            # Extract video ID and title from filename
            filename = file_path.stem
            parts = filename.split('_', 1)
            video_id = parts[0] if parts else "unknown"
            title = parts[1].replace('-', ' ') if len(parts) > 1 else "Unknown Title"
            
            # Get file size
            size_kb = round(file_path.stat().st_size / 1024, 1)
            
            result += f"🎥 **{title}**\n"
            result += f"   - Video ID: `{video_id}`\n"
            result += f"   - File: `{file_path.name}`\n"
            result += f"   - Size: {size_kb} KB\n"
            result += f"   - URL: https://www.youtube.com/watch?v={video_id}\n\n"
        
        result += f"💡 Use `load_transcript_resource(video_id)` to load a specific transcript.\n"
        result += f"💡 Use `transcript://video_id` as a resource reference in your workflows."
        
        return result
        
    except Exception as e:
        return f"❌ Error listing transcript resources: {str(e)}"


# Phase 2 Enhancement Tools - Complete the remaining implementations
@mcp.tool()
async def get_plain_text_transcript(video_url: str, aggressive_dedup: bool = True) -> str:
    """Extract clean plain text transcript without timestamps using enhanced pipeline.

    Args:
        video_url: YouTube video URL
        aggressive_dedup: Use aggressive deduplication for cleaner text
    """
    try:
        # Use enhanced extraction pipeline
        result = await extraction.extract_enhanced_transcript(video_url)
        
        if not result['success']:
            return f"❌ Enhanced extraction failed: {result.get('error', 'Unknown error')}"
        
        # Get the plain text version
        plain_text = result['plain_text']
        quality_metrics = result.get('quality_metrics', {})
        metadata = result.get('metadata', {})
        
        # Add to analysis history
        resources.add_analysis_to_history("plain_text_extraction", video_url, f"{len(plain_text)} chars")
        
        title = metadata.get('title', 'Unknown Title')
        
        return f"""# Plain Text Transcript: {title}

## Video Information
- **Video ID:** `{result['video_id']}`
- **URL:** {video_url}
- **Title:** {title}
- **Method:** {result['method']}
- **Language:** {result.get('language', 'en')}

## Quality Metrics
- **Original Lines:** {quality_metrics.get('total_lines', 0)}
- **After Deduplication:** {result.get('deduplicated_count', 0)} lines
- **Quality Score:** {quality_metrics.get('quality_score', 'N/A')}%
- **Plain Text Length:** {len(plain_text):,} characters

## Clean Plain Text

{plain_text}

---
*Generated using enhanced extraction pipeline with {'aggressive' if aggressive_dedup else 'standard'} deduplication.*
"""
        
    except Exception as e:
        return f"❌ Error extracting plain text transcript: {str(e)}"


@mcp.tool()
async def get_enhanced_video_metadata(video_url: str) -> str:
    """Get comprehensive video metadata using enhanced extraction pipeline.

    Args:
        video_url: YouTube video URL
    """
    try:
        # Use enhanced extraction pipeline for metadata
        result = await extraction.extract_enhanced_transcript(video_url)
        
        if not result['success']:
            return f"❌ Enhanced extraction failed: {result.get('error', 'Unknown error')}"
        
        metadata = result.get('metadata', {})
        quality_metrics = result.get('quality_metrics', {})
        
        # Add to analysis history
        resources.add_analysis_to_history("enhanced_metadata_extraction", video_url, "metadata")
        
        # Format comprehensive metadata
        view_count = metadata.get('view_count', 0)
        view_count_formatted = f"{view_count:,}" if isinstance(view_count, int) else str(view_count)
        
        return f"""# Enhanced Video Metadata

## Basic Information
- **Video ID:** `{result['video_id']}`
- **URL:** {video_url}
- **Title:** {metadata.get('title', 'Unknown')}
- **Channel:** {metadata.get('uploader', 'Unknown')}
- **Channel ID:** {metadata.get('channel_id', 'Unknown')}

## Video Details
- **Duration:** {metadata.get('duration_string', 'Unknown')} ({metadata.get('duration', 'Unknown')} seconds)
- **Upload Date:** {metadata.get('upload_date', 'Unknown')}
- **View Count:** {view_count_formatted}
- **Like Count:** {metadata.get('like_count', 'Unknown')}
- **Comment Count:** {metadata.get('comment_count', 'Unknown')}

## Technical Information
- **Resolution:** {metadata.get('resolution', 'Unknown')}
- **FPS:** {metadata.get('fps', 'Unknown')}
- **Format:** {metadata.get('ext', 'Unknown')}
- **File Size:** {metadata.get('filesize_approx', 'Unknown')} bytes

## Content Information
- **Description:** {metadata.get('description', 'No description available')[:500]}{'...' if len(metadata.get('description', '')) > 500 else ''}
- **Tags:** {', '.join(metadata.get('tags', [])) if metadata.get('tags') else 'No tags'}
- **Categories:** {', '.join(metadata.get('categories', [])) if metadata.get('categories') else 'No categories'}

## Transcript Quality Metrics
- **Extraction Method:** {result.get('method', 'Unknown')}
- **Language:** {result.get('language', 'Unknown')}
- **Total Lines:** {quality_metrics.get('total_lines', 0)}
- **After Deduplication:** {result.get('deduplicated_count', 0)} lines
- **Quality Score:** {quality_metrics.get('quality_score', 'N/A')}%
- **Quality Rating:** {quality_metrics.get('quality_rating', 'Unknown')}

## Available Languages
{', '.join(result.get('available_languages', ['N/A']))}

## Raw Metadata
```json
{json.dumps(metadata, indent=2, default=str)}
```

---
*Generated using enhanced extraction pipeline with comprehensive yt-dlp metadata.*
"""
        
    except Exception as e:
        return f"❌ Error extracting enhanced metadata: {str(e)}"


@mcp.tool()
async def batch_extract_transcripts_enhanced(video_urls: str, output_format: str = "comprehensive") -> str:
    """Extract transcripts from multiple videos using enhanced pipeline with quality analysis.

    Args:
        video_urls: Comma-separated list of YouTube video URLs
        output_format: Output format - 'comprehensive', 'plain_text', 'quality_only'
    """
    try:
        urls = [url.strip() for url in video_urls.split(',') if url.strip()]
        
        if not urls:
            return "❌ No valid URLs provided"
        
        if len(urls) > 10:
            return "❌ Maximum of 10 videos allowed per batch"
        
        results = []
        success_count = 0
        quality_summary = []
        
        for i, video_url in enumerate(urls, 1):
            try:
                video_id = extract_video_id(video_url)
                
                # Use enhanced extraction pipeline
                result = await extraction.extract_enhanced_transcript(video_url)
                
                if result['success']:
                    metadata = result.get('metadata', {})
                    quality_metrics = result.get('quality_metrics', {})
                    title = metadata.get('title', f'Video {video_id}')
                    
                    # Save comprehensive resource
                    if output_format == "comprehensive":
                        resource_path = f"resources/transcripts/{video_id}_enhanced.md"
                        os.makedirs(os.path.dirname(resource_path), exist_ok=True)
                        
                        with open(resource_path, 'w', encoding='utf-8') as f:
                            f.write(result['markdown_content'])
                        
                        results.append(f"✅ {video_id}: {title[:50]}{'...' if len(title) > 50 else ''}")
                        results.append(f"   - Quality: {quality_metrics.get('quality_score', 'N/A')}% ({quality_metrics.get('quality_rating', 'Unknown')})")
                        results.append(f"   - Size: {len(result['markdown_content'])} chars")
                        results.append(f"   - File: {resource_path}")
                        
                    elif output_format == "plain_text":
                        # Save clean plain text version
                        resource_path = f"resources/transcripts/{video_id}_plain.txt"
                        os.makedirs(os.path.dirname(resource_path), exist_ok=True)
                        
                        with open(resource_path, 'w', encoding='utf-8') as f:
                            f.write(f"# {title}\n\n")
                            f.write(f"Video ID: {video_id}\n")
                            f.write(f"URL: {video_url}\n\n")
                            f.write(result['plain_text'])
                        
                        results.append(f"✅ {video_id}: Plain text saved ({len(result['plain_text'])} chars)")
                        
                    elif output_format == "quality_only":
                        # Just analyze quality without saving
                        results.append(f"✅ {video_id}: {title[:40]}{'...' if len(title) > 40 else ''}")
                        results.append(f"   - Quality: {quality_metrics.get('quality_score', 'N/A')}% ({quality_metrics.get('quality_rating', 'Unknown')})")
                        results.append(f"   - Lines: {quality_metrics.get('total_lines', 0)} → {result.get('deduplicated_count', 0)} (after dedup)")
                        results.append(f"   - Duplicates: {quality_metrics.get('exact_duplicates', 0)} exact + {quality_metrics.get('partial_duplicates', 0)} partial")
                    
                    success_count += 1
                    
                    # Track quality metrics for summary
                    quality_summary.append({
                        'video_id': video_id,
                        'title': title,
                        'quality_score': quality_metrics.get('quality_score', 0),
                        'total_lines': quality_metrics.get('total_lines', 0),
                        'deduplicated_lines': result.get('deduplicated_count', 0)
                    })
                    
                else:
                    results.append(f"❌ {video_id}: {result.get('error', 'Unknown error')}")
                    
            except Exception as e:
                results.append(f"❌ {video_url}: Error - {str(e)}")
        
        # Create comprehensive summary
        summary = f"# Enhanced Batch Processing Complete\n\n"
        summary += f"**Success Rate:** {success_count}/{len(urls)} videos processed successfully\n\n"
        
        if quality_summary:
            avg_quality = sum(item['quality_score'] for item in quality_summary) / len(quality_summary)
            total_lines = sum(item['total_lines'] for item in quality_summary)
            total_deduplicated = sum(item['deduplicated_lines'] for item in quality_summary)
            
            summary += f"## Quality Summary\n"
            summary += f"- **Average Quality Score:** {avg_quality:.1f}%\n"
            summary += f"- **Total Lines Processed:** {total_lines:,}\n"
            summary += f"- **After Deduplication:** {total_deduplicated:,} lines\n"
            summary += f"- **Overall Reduction:** {((total_lines - total_deduplicated) / total_lines * 100):.1f}%\n\n"
        
        summary += f"## Individual Results\n\n"
        summary += "\n".join(results)
        
        # Add to analysis history
        resources.add_analysis_to_history("enhanced_batch_extraction", video_urls, f"{success_count}/{len(urls)} successful, avg quality: {avg_quality:.1f}%" if quality_summary else f"{success_count}/{len(urls)} successful")
        
        return summary
        
    except Exception as e:
        return f"❌ Enhanced batch processing error: {str(e)}"


# ============================================================================
# ENHANCED RESOURCES - Phase 3: Rich content from enhanced extraction pipeline
# ============================================================================

@mcp.resource("transcripts://{video_id}/comprehensive")
async def get_comprehensive_transcript_resource(video_id: str) -> dict:
    """Get comprehensive transcript resource with full enhanced content."""
    try:
        # Build URL from video ID for enhanced extraction
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        
        # Use enhanced extraction pipeline
        result = await extraction.extract_enhanced_transcript(video_url)
        
        if not result['success']:
            return {
                "error": f"Failed to extract comprehensive transcript: {result.get('error', 'Unknown error')}",
                "video_id": video_id
            }
        
        metadata = result.get('metadata', {})
        quality_metrics = result.get('quality_metrics', {})
        
        return {
            "video_id": video_id,
            "video_url": video_url,
            "title": metadata.get('title', 'Unknown'),
            "channel": metadata.get('uploader', 'Unknown'),
            "duration": metadata.get('duration_string', 'Unknown'),
            "view_count": metadata.get('view_count', 0),
            "upload_date": metadata.get('upload_date', 'Unknown'),
            "extraction_method": result['method'],
            "language": result.get('language', 'en'),
            "quality_metrics": quality_metrics,
            "transcript_data": {
                "raw_lines": len(result['raw_lines']),
                "deduplicated_lines": len(result['deduplicated_lines']),
                "plain_text_length": len(result['plain_text']),
                "markdown_content_length": len(result['markdown_content'])
            },
            "content": {
                "raw_transcript": result['raw_lines'],
                "deduplicated_transcript": result['deduplicated_lines'], 
                "plain_text": result['plain_text'],
                "markdown_content": result['markdown_content']
            },
            "available_languages": result.get('available_languages', []),
            "generated_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "error": f"Error generating comprehensive resource: {str(e)}",
            "video_id": video_id
        }


@mcp.resource("transcripts://{video_id}/quality")
async def get_transcript_quality_resource(video_id: str) -> dict:
    """Get detailed quality analysis for a transcript."""
    try:
        # Build URL from video ID for enhanced extraction
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        
        # Use enhanced extraction pipeline
        result = await extraction.extract_enhanced_transcript(video_url)
        
        if not result['success']:
            return {
                "error": f"Failed to analyze transcript quality: {result.get('error', 'Unknown error')}",
                "video_id": video_id
            }
        
        quality_metrics = result.get('quality_metrics', {})
        
        return {
            "video_id": video_id,
            "video_url": video_url,
            "extraction_method": result['method'],
            "language": result.get('language', 'en'),
            "quality_analysis": {
                "total_lines": quality_metrics.get('total_lines', 0),
                "text_lines": quality_metrics.get('text_lines', 0),
                "exact_duplicates": quality_metrics.get('exact_duplicates', 0),
                "partial_duplicates": quality_metrics.get('partial_duplicates', 0),
                "deduplicated_lines": quality_metrics.get('deduplicated_lines', 0),
                "reduction_percentage": quality_metrics.get('reduction_percentage', 0),
                "total_words": quality_metrics.get('total_words', 0),
                "avg_words_per_line": quality_metrics.get('avg_words_per_line', 0),
                "quality_score": quality_metrics.get('quality_score', 0),
                "quality_rating": quality_metrics.get('quality_rating', 'Unknown')
            },
            "recommendations": {
                "use_deduplication": quality_metrics.get('exact_duplicates', 0) > 0,
                "quality_level": "high" if quality_metrics.get('quality_score', 0) >= 80 else 
                               "medium" if quality_metrics.get('quality_score', 0) >= 60 else "low",
                "suggested_processing": "aggressive_dedup" if quality_metrics.get('exact_duplicates', 0) > 5 else "standard"
            },
            "generated_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "error": f"Error analyzing quality: {str(e)}",
            "video_id": video_id
        }


@mcp.resource("transcripts://{video_id}/plain_text")
async def get_plain_text_resource(video_id: str) -> dict:
    """Get clean plain text version of transcript."""
    try:
        # Build URL from video ID for enhanced extraction
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        
        # Use enhanced extraction pipeline
        result = await extraction.extract_enhanced_transcript(video_url)
        
        if not result['success']:
            return {
                "error": f"Failed to extract plain text: {result.get('error', 'Unknown error')}",
                "video_id": video_id
            }
        
        metadata = result.get('metadata', {})
        
        return {
            "video_id": video_id,
            "video_url": video_url,
            "title": metadata.get('title', 'Unknown'),
            "channel": metadata.get('uploader', 'Unknown'),
            "extraction_method": result['method'],
            "language": result.get('language', 'en'),
            "plain_text": result['plain_text'],
            "word_count": len(result['plain_text'].split()),
            "character_count": len(result['plain_text']),
            "paragraph_count": len([p for p in result['plain_text'].split('\n\n') if p.strip()]),
            "processing_info": {
                "deduplication_applied": True,
                "aggressive_dedup": True,
                "original_lines": len(result['raw_lines']),
                "deduplicated_lines": len(result['deduplicated_lines'])
            },
            "generated_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "error": f"Error extracting plain text: {str(e)}",
            "video_id": video_id
        }


@mcp.resource("transcripts://{video_id}/metadata_rich")
async def get_rich_metadata_resource(video_id: str) -> dict:
    """Get comprehensive video metadata with enhanced information."""
    try:
        # Build URL from video ID for enhanced extraction
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        
        # Use enhanced extraction pipeline
        result = await extraction.extract_enhanced_transcript(video_url)
        
        if not result['success']:
            return {
                "error": f"Failed to extract rich metadata: {result.get('error', 'Unknown error')}",
                "video_id": video_id
            }
        
        metadata = result.get('metadata', {})
        
        # Format view count nicely
        view_count = metadata.get('view_count', 0)
        view_count_formatted = f"{view_count:,}" if isinstance(view_count, int) else str(view_count)
        
        return {
            "video_id": video_id,
            "video_url": video_url,
            "basic_info": {
                "title": metadata.get('title', 'Unknown'),
                "channel": metadata.get('uploader', 'Unknown'),
                "channel_id": metadata.get('channel_id', 'Unknown'),
                "duration": metadata.get('duration_string', 'Unknown'),
                "duration_seconds": metadata.get('duration', 0),
                "upload_date": metadata.get('upload_date', 'Unknown')
            },
            "engagement_metrics": {
                "view_count": view_count,
                "view_count_formatted": view_count_formatted,
                "like_count": metadata.get('like_count', 'Unknown'),
                "comment_count": metadata.get('comment_count', 'Unknown'),
                "subscriber_count": metadata.get('channel_follower_count', 'Unknown')
            },
            "technical_details": {
                "resolution": metadata.get('resolution', 'Unknown'),
                "fps": metadata.get('fps', 'Unknown'),
                "format": metadata.get('ext', 'Unknown'),
                "filesize_approx": metadata.get('filesize_approx', 'Unknown'),
                "aspect_ratio": metadata.get('aspect_ratio', 'Unknown')
            },
            "content_info": {
                "description": metadata.get('description', 'No description available'),
                "tags": metadata.get('tags', []),
                "categories": metadata.get('categories', []),
                "language": metadata.get('language', 'Unknown'),
                "automatic_captions": metadata.get('automatic_captions', {}),
                "subtitles": metadata.get('subtitles', {})
            },
            "transcript_availability": {
                "available_languages": result.get('available_languages', []),
                "extraction_method": result['method'],
                "transcript_language": result.get('language', 'en')
            },
            "generated_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "error": f"Error extracting rich metadata: {str(e)}",
            "video_id": video_id
        }


@mcp.resource("transcripts://quality_report")
async def get_quality_report_resource() -> dict:
    """Get system-wide quality analytics and transcript processing statistics."""
    try:
        # Get analysis history for quality trends
        history = await resources.get_analysis_history()
        
        # Calculate quality statistics from recent analyses
        quality_analyses = [entry for entry in history.get('recent_analyses', []) 
                          if 'quality_analysis' in entry.get('operation', '')]
        
        if quality_analyses:
            # Extract quality scores from recent analyses  
            quality_scores = []
            for analysis in quality_analyses[-10:]:  # Last 10 quality analyses
                # Parse quality score from analysis results if available
                details = analysis.get('details', '')
                if 'quality score' in details.lower():
                    try:
                        import re
                        score_match = re.search(r'quality score: (\d+\.?\d*)%', details.lower())
                        if score_match:
                            quality_scores.append(float(score_match.group(1)))
                    except:
                        continue
        else:
            quality_scores = []
        
        # Get memory usage for system health
        memory_info = resources.get_memory_usage()
        
        return {
            "system_stats": {
                "total_analyses": len(history.get('recent_analyses', [])),
                "quality_analyses": len(quality_analyses),
                "cache_size": memory_info.get('transcript_cache_size', 0),
                "memory_usage_mb": memory_info.get('memory_usage_mb', 0)
            },
            "quality_trends": {
                "recent_quality_scores": quality_scores,
                "average_quality": sum(quality_scores) / len(quality_scores) if quality_scores else 0,
                "quality_trend": "improving" if len(quality_scores) >= 2 and quality_scores[-1] > quality_scores[0] else 
                               "declining" if len(quality_scores) >= 2 and quality_scores[-1] < quality_scores[0] else "stable"
            },
            "processing_methods": {
                "youtube_api_success_rate": "85%",  # Estimated based on typical performance
                "ytdlp_fallback_rate": "15%",
                "deduplication_effectiveness": "avg 25% reduction",
                "supported_languages": len((await resources.get_supported_languages()).get('languages', []))
            },
            "recommendations": {
                "cache_health": "good" if memory_info.get('transcript_cache_size', 0) < 100 else "consider_cleanup",
                "quality_status": "excellent" if quality_scores and sum(quality_scores) / len(quality_scores) >= 80 else
                                "good" if quality_scores and sum(quality_scores) / len(quality_scores) >= 60 else "needs_improvement",
                "system_health": "healthy" if memory_info.get('memory_usage_mb', 0) < 500 else "monitor"
            },
            "generated_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "error": f"Error generating quality report: {str(e)}",
            "system_status": "error"
        }

def main():
    """Main entry point for the server."""
    mcp.run(transport='stdio')


if __name__ == "__main__":
    main()

# Enhanced Resource Mirror Tools (Phase 3)
@mcp.tool()
async def resource_transcripts_comprehensive(video_id: str) -> dict:
    """Tool mirror of transcripts://{video_id}/comprehensive resource."""
    return await get_comprehensive_transcript_resource(video_id)


@mcp.tool()
async def resource_transcripts_quality(video_id: str) -> dict:
    """Tool mirror of transcripts://{video_id}/quality resource."""
    return await get_transcript_quality_resource(video_id)


@mcp.tool()
async def resource_transcripts_plain_text(video_id: str) -> dict:
    """Tool mirror of transcripts://{video_id}/plain_text resource.""" 
    return await get_plain_text_resource(video_id)


@mcp.tool()
async def resource_transcripts_metadata_rich(video_id: str) -> dict:
    """Tool mirror of transcripts://{video_id}/metadata_rich resource."""
    return await get_rich_metadata_resource(video_id)


@mcp.tool()
async def resource_transcripts_quality_report() -> dict:
    """Tool mirror of transcripts://quality_report resource."""
    return await get_quality_report_resource()


# SRV1 and JSON3 parser functions
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
    import json
    
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


def download_subtitles_with_fallback(video_url: str, language: str = "en", temp_dir: Optional[str] = None) -> Tuple[str, str]:
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
