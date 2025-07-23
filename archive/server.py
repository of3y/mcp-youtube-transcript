#!/usr/bin/env python3
"""
YouTube Transcript MCP Server

A Model-Context-Protocol server that provides YouTube transcript extraction functionality.
"""

import re
import json
import subprocess
import os
from typing import Any, List, Optional
from mcp.server.fastmcp import FastMCP
from youtube_transcript_api._api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
# Initialize FastMCP server
mcp = FastMCP("youtube-transcript-server")


def extract_video_id(url: str) -> str:
    """
    Extract YouTube video ID from various URL formats.
    """
    # Define regex patterns for different YouTube URL formats
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


@mcp.tool()
async def get_youtube_transcript(video_url: str, language: str = "en") -> str:
    """Get the transcript of a YouTube video.

    Args:
        video_url: YouTube video URL
        language: Language code (e.g., 'en', 'es'). Defaults to 'en'
    """
    try:
        video_id = extract_video_id(video_url)

        # First, try to list available transcripts
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            
            # Get available languages
            available_languages = []
            for transcript in transcript_list:
                available_languages.append(f"{transcript.language_code} ({'auto' if transcript.is_generated else 'manual'})")
            
            # Try to find the requested language first
            try:
                transcript = transcript_list.find_transcript([language])
            except NoTranscriptFound:
                # Try English as fallback
                try:
                    transcript = transcript_list.find_transcript(['en'])
                    language = 'en'
                except NoTranscriptFound:
                    # Try any available language
                    transcript = transcript_list.find_generated_transcript(['en'])
                    language = 'en (auto-generated)'
            
            # Get the transcript data
            transcript_data = transcript.fetch()
            
            # Format the transcript - handle both dict and object formats
            formatted_transcript = []
            for entry in transcript_data:
                # Handle both dictionary and object formats
                if isinstance(entry, dict):
                    # Dictionary format (most common)
                    start_time = entry.get('start', 0)
                    text = entry.get('text', '')
                elif hasattr(entry, 'start') and hasattr(entry, 'text'):
                    # Object format
                    start_time = entry.start
                    text = entry.text
                else:
                    # Fallback - try to convert to string
                    start_time = 0
                    text = str(entry)
                
                timestamp = f"[{int(start_time//60):02d}:{int(start_time%60):02d}]"
                formatted_transcript.append(f"{timestamp} {text}")
            
            full_transcript = "\n".join(formatted_transcript)
            
            result = f"Transcript for {video_url} (Language: {language}):\n"
            result += f"Available languages: {', '.join(available_languages)}\n\n"
            result += full_transcript
            
            return result
            
        except Exception as list_error:
            # Fallback to direct transcript request
            transcript_data = YouTubeTranscriptApi.get_transcript(video_id, languages=[language, 'en'])
            
            formatted_transcript = []
            for entry in transcript_data:
                # Handle both dictionary and object formats
                if isinstance(entry, dict):
                    # Dictionary format (most common)
                    start_time = entry.get('start', 0)
                    text = entry.get('text', '')
                elif hasattr(entry, 'start') and hasattr(entry, 'text'):
                    # Object format
                    start_time = entry.start
                    text = entry.text
                else:
                    # Fallback - try to convert to string
                    start_time = 0
                    text = str(entry)
                
                timestamp = f"[{int(start_time//60):02d}:{int(start_time%60):02d}]"
                formatted_transcript.append(f"{timestamp} {text}")
            
            full_transcript = "\n".join(formatted_transcript)
            return f"Transcript for {video_url}:\n\n{full_transcript}"
    
    except (TranscriptsDisabled, NoTranscriptFound) as e:
        return f"❌ No transcript available for this video.\n\nPossible reasons:\n- Video has no captions/subtitles\n- Transcripts are disabled by the creator\n- Video is private/restricted\n- Geo-blocking restrictions\n\nError details: {str(e)}"
    
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
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)

        # Search for matches
        matches = []
        query_lower = query.lower()
        
        for i, entry in enumerate(transcript_list):
            # Handle both dictionary and object formats
            if isinstance(entry, dict):
                entry_text = entry.get('text', '')
            elif hasattr(entry, 'text'):
                entry_text = entry.text
            else:
                entry_text = str(entry)
                
            if query_lower in entry_text.lower():
                # Get context
                start_idx = max(0, i - context_lines)
                end_idx = min(len(transcript_list), i + context_lines + 1)

                context_entries = transcript_list[start_idx:end_idx]
                context_text = []

                for j, ctx_entry in enumerate(context_entries):
                    # Handle both dictionary and object formats
                    if isinstance(ctx_entry, dict):
                        start_time = ctx_entry.get('start', 0)
                        text = ctx_entry.get('text', '')
                    elif hasattr(ctx_entry, 'start') and hasattr(ctx_entry, 'text'):
                        start_time = ctx_entry.start
                        text = ctx_entry.text
                    else:
                        start_time = 0
                        text = str(ctx_entry)
                    
                    timestamp = f"[{int(start_time//60):02d}:{int(start_time%60):02d}]"

                    # Highlight the match
                    if j == i - start_idx:  # This is the matching line
                        # Case-insensitive replacement while preserving original case
                        import re
                        pattern = re.compile(re.escape(query), re.IGNORECASE)
                        text = pattern.sub(f"**{query}**", text)

                    context_text.append(f"{timestamp} {text}")

                matches.append("\n".join(context_text))
        
        if matches:
            result = f"Found {len(matches)} matches for '{query}' in {video_url}:\n\n"
            result += "\n\n---\n\n".join(matches)
            return result
        else:
            return f"No matches found for '{query}' in the video transcript."
        
    except Exception as e:
        return f"Error searching transcript: {str(e)}"


@mcp.tool()
async def get_youtube_transcript_ytdlp(video_url: str, language: str = "en") -> str:
    """Get the transcript of a YouTube video using yt-dlp (more reliable alternative).

    Args:
        video_url: YouTube video URL
        language: Language code (e.g., 'en', 'es'). Defaults to 'en'
    """
    try:
        video_id = extract_video_id(video_url)
        
        # Use yt-dlp to extract subtitle information
        cmd = [
            'yt-dlp',
            '--write-auto-subs',
            '--write-subs', 
            '--sub-lang', language,
            '--sub-format', 'vtt',
            '--skip-download',
            '--output', f'/tmp/%(title)s.%(ext)s',
            video_url
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode != 0:
            # Try with auto-generated subtitles only
            cmd_auto = [
                'yt-dlp',
                '--write-auto-subs',
                '--sub-lang', 'en',
                '--sub-format', 'vtt',
                '--skip-download',
                '--output', f'/tmp/%(title)s.%(ext)s',
                video_url
            ]
            result = subprocess.run(cmd_auto, capture_output=True, text=True, timeout=30)
            
            if result.returncode != 0:
                return f"❌ yt-dlp failed to extract subtitles: {result.stderr}"
        
        # Try to find the VTT file
        import glob
        vtt_files = glob.glob(f'/tmp/*.{language}.vtt') or glob.glob('/tmp/*.en.vtt')
        
        if not vtt_files:
            return f"❌ No subtitle file found for language '{language}'. Try 'en' or check if video has captions."
        
        # Parse VTT file
        with open(vtt_files[0], 'r', encoding='utf-8') as f:
            vtt_content = f.read()
        
        # Simple VTT parsing
        lines = vtt_content.split('\n')
        formatted_transcript = []
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Look for timestamp lines (format: 00:00:00.000 --> 00:00:02.000)
            if '-->' in line:
                start_time = line.split(' --> ')[0]
                # Get the subtitle text (next non-empty line)
                i += 1
                while i < len(lines) and not lines[i].strip():
                    i += 1
                
                if i < len(lines):
                    subtitle_text = lines[i].strip()
                    # Remove HTML tags
                    import re
                    subtitle_text = re.sub(r'<[^>]+>', '', subtitle_text)
                    
                    if subtitle_text:
                        formatted_transcript.append(f"[{start_time}] {subtitle_text}")
            i += 1
        
        # Clean up
        for vtt_file in vtt_files:
            try:
                import os
                os.remove(vtt_file)
            except:
                pass
        
        if formatted_transcript:
            return f"Transcript for {video_url} (extracted via yt-dlp):\n\n" + "\n".join(formatted_transcript)
        else:
            return f"❌ Could not parse subtitle content for {video_url}"
            
    except subprocess.TimeoutExpired:
        return "❌ yt-dlp extraction timed out (30s limit)"
    except Exception as e:
        return f"❌ Error using yt-dlp: {str(e)}"


# ========== VIDEO INTELLIGENCE SUITE ==========

@mcp.tool()
async def analyze_video_comprehensive(
    video_url: str, 
    analysis_type: str = "summary", 
    custom_prompt: str = ""
) -> str:
    """Get video transcript with analysis prompt for comprehensive video analysis.
    
    Args:
        video_url: YouTube video URL
        analysis_type: Type of analysis - summary, key_points, action_items, questions, sentiment, transcript_cleanup
        custom_prompt: Custom analysis prompt (overrides analysis_type if provided)
    """
    try:
        # Get transcript first
        transcript = await get_youtube_transcript(video_url)
        
        if "❌" in transcript:
            return transcript  # Return error message
        
        # Clean transcript for analysis (remove timestamp formatting)
        clean_transcript = transcript.split("\n\n", 2)[-1] if "\n\n" in transcript else transcript
        
        # Define analysis prompts
        prompts = {
            "summary": "Provide a concise 3-5 bullet point summary of this video transcript:",
            "key_points": "Extract the main key points and important concepts from this video transcript:",
            "action_items": "Extract actionable items, recommendations, and next steps mentioned in this video:",
            "questions": "Generate 5 thoughtful questions that test understanding of the content in this video:",
            "sentiment": "Analyze the sentiment and tone of this video content:",
            "transcript_cleanup": "Clean up this transcript by removing filler words, fixing grammar, and improving readability while preserving all important content:"
        }
        
        if custom_prompt:
            prompt = custom_prompt
        elif analysis_type in prompts:
            prompt = prompts[analysis_type]
        else:
            return f"❌ Invalid analysis_type. Choose from: {', '.join(prompts.keys())}"
        
        # Return structured data for Claude Desktop to process
        result = f"🎯 Analysis Request ({analysis_type}):\nVideo: {video_url}\n\n"
        result += f"**Analysis Prompt:**\n{prompt}\n\n"
        result += f"**Transcript:**\n{clean_transcript}\n\n"
        result += "---\n*Claude Desktop: Please analyze the above transcript using the provided prompt.*"
        
        return result
        
    except Exception as e:
        return f"❌ Error preparing video analysis: {str(e)}"


@mcp.tool()
async def extract_key_quotes(video_url: str, topic: str) -> str:
    """Get video transcript with prompt to find key quotes about a specific topic.
    
    Args:
        video_url: YouTube video URL
        topic: Topic or subject to search for quotes about
    """
    try:
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


def main():
    """Main entry point for the server."""
    mcp.run(transport='stdio')


if __name__ == "__main__":
    main()