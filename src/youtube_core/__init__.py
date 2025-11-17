"""
YouTube Core - Standalone extraction library for YouTube transcripts and comments.

This module provides a clean, standalone API for extracting:
- Video transcripts (multiple formats with fallback)
- Video comments (with threading and sorting)
- Video metadata
- Quality analysis

Example usage:
    from youtube_core import YouTubeExtractor

    # Create extractor
    extractor = YouTubeExtractor()

    # Extract transcript only
    result = extractor.extract_transcript_only("https://youtube.com/watch?v=...")

    # Extract transcript + comments
    result = extractor.extract(
        "https://youtube.com/watch?v=...",
        include_transcript=True,
        include_comments=True
    )

    # Format as markdown
    from youtube_core.formatters import format_complete_as_markdown
    markdown = format_complete_as_markdown(result)
"""

__version__ = "1.0.0"

from .extractor import YouTubeExtractor
from .config import ExtractionConfig
from .transcript import (
    extract_transcript,
    extract_video_id,
    get_video_metadata,
    deduplicate_transcript_lines
)
from .comments import (
    extract_comments,
    format_comments_as_text,
    format_comments_as_markdown,
    get_comment_statistics
)
from .quality import (
    analyze_transcript_quality,
    analyze_comment_quality
)
from .formatters import (
    create_plain_text_script,
    format_transcript_as_markdown,
    format_comments_as_markdown as format_comments_md,
    format_complete_as_markdown,
    save_as_json,
    save_as_markdown
)

__all__ = [
    # Main classes
    'YouTubeExtractor',
    'ExtractionConfig',

    # Transcript functions
    'extract_transcript',
    'extract_video_id',
    'get_video_metadata',
    'deduplicate_transcript_lines',

    # Comment functions
    'extract_comments',
    'format_comments_as_text',
    'format_comments_as_markdown',
    'get_comment_statistics',

    # Quality functions
    'analyze_transcript_quality',
    'analyze_comment_quality',

    # Formatters
    'create_plain_text_script',
    'format_transcript_as_markdown',
    'format_comments_md',
    'format_complete_as_markdown',
    'save_as_json',
    'save_as_markdown',
]
