#!/usr/bin/env python3
"""
YouTube Transcript & Comment Extractor - Standalone CLI Tool

A professional command-line tool for extracting YouTube video data:
- Transcripts (multi-format with fallback)
- Comments (with sorting and threading)
- Video metadata
- Quality analysis

This tool is completely standalone and decoupled from the MCP server.

Usage:
    # Extract transcript only
    python scripts/youtube_extract.py <url>

    # Extract transcript + top 50 comments
    python scripts/youtube_extract.py <url> --comments --max-comments 50

    # Extract with specific language
    python scripts/youtube_extract.py <url> --lang es

    # Save in minimal format
    python scripts/youtube_extract.py <url> --minimal

    # Save as JSON
    python scripts/youtube_extract.py <url> --format json

Examples:
    python scripts/youtube_extract.py https://youtube.com/watch?v=dQw4w9WgXcQ
    python scripts/youtube_extract.py https://youtu.be/jNQXAC9IVRw --comments --max-comments 100
    python scripts/youtube_extract.py <url> --lang fr --comments --output ./data
"""

import os
import sys
import argparse
import re
from pathlib import Path
from datetime import datetime

# Add parent directory to path to import youtube_core
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from youtube_core import (
    YouTubeExtractor,
    ExtractionConfig,
    format_complete_as_markdown,
    save_as_json,
    save_as_markdown
)


def create_safe_filename(title: str, video_id: str, minimal: bool = False, format_type: str = "md") -> str:
    """Create a safe filename from video title."""
    # Clean title
    safe_title = re.sub(r'[^\w\s-]', '', title).strip()
    safe_title = re.sub(r'[-\s]+', '-', safe_title)[:50]

    # Add format indicator
    format_suffix = "_minimal" if minimal else ""

    # Create filename
    filename = f"{video_id}_{safe_title}{format_suffix}.{format_type}"

    return filename


def print_separator(char='=', length=80):
    """Print a separator line."""
    print(char * length)


def print_section(title: str):
    """Print a section header."""
    print(f"\n{title}")
    print_separator('-', len(title))


def main():
    parser = argparse.ArgumentParser(
        description="Extract YouTube transcripts and comments - Standalone CLI Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Extract transcript only
  %(prog)s "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

  # Extract transcript + comments
  %(prog)s "https://youtu.be/jNQXAC9IVRw" --comments --max-comments 100

  # Extract with specific language and minimal format
  %(prog)s "https://youtu.be/dQw4w9WgXcQ" --lang es --minimal

  # Save as JSON
  %(prog)s "https://youtu.be/dQw4w9WgXcQ" --format json

  # Extract everything
  %(prog)s "https://youtu.be/dQw4w9WgXcQ" --comments --max-comments 100 --comment-replies
        """
    )

    # Required arguments
    parser.add_argument('video_url', help='YouTube video URL')

    # Transcript options
    parser.add_argument('--lang', default='en', help='Language code for transcripts (default: en)')
    parser.add_argument('--no-transcript', action='store_true', help='Skip transcript extraction')

    # Comment options
    parser.add_argument('--comments', action='store_true', help='Extract comments')
    parser.add_argument('--max-comments', type=int, default=100, help='Maximum comments to extract (default: 100)')
    parser.add_argument('--comment-sort', choices=['top', 'new', 'time'], default='top',
                        help='Comment sorting method (default: top)')
    parser.add_argument('--comment-replies', action='store_true', help='Include comment replies')
    parser.add_argument('--max-replies', type=int, default=3, help='Maximum replies per comment (default: 3)')

    # Output options
    parser.add_argument('--output', default='./output',
                        help='Output directory (default: ./output)')
    parser.add_argument('--format', choices=['markdown', 'json', 'both'], default='markdown',
                        help='Output format (default: markdown)')
    parser.add_argument('--minimal', action='store_true',
                        help='Generate minimal format optimized for Claude (markdown only)')

    # Behavior options
    parser.add_argument('--timeout', type=int, default=60, help='Command timeout in seconds (default: 60)')
    parser.add_argument('--no-dedup', action='store_true', help='Disable aggressive deduplication')
    parser.add_argument('--debug', action='store_true', help='Enable debug output')
    parser.add_argument('--quiet', action='store_true', help='Minimal console output')

    args = parser.parse_args()

    # Configure extractor
    config = ExtractionConfig(
        default_language=args.lang,
        max_comments=args.max_comments,
        comment_sort=args.comment_sort,
        enable_replies=args.comment_replies,
        max_replies_per_comment=args.max_replies,
        output_dir=args.output,
        timeout=args.timeout,
        aggressive_dedup=not args.no_dedup
    )

    extractor = YouTubeExtractor(config)

    # Print header
    if not args.quiet:
        print_separator()
        print("🎥 YouTube Transcript & Comment Extractor")
        print_separator()
        print(f"Video: {args.video_url}")
        print(f"Language: {args.lang}")
        print(f"Comments: {'Yes' if args.comments else 'No'}")
        if args.comments:
            print(f"  - Max comments: {args.max_comments}")
            print(f"  - Sort by: {args.comment_sort}")
            print(f"  - Include replies: {'Yes' if args.comment_replies else 'No'}")
        print(f"Format: {args.format}")
        if args.format == 'markdown':
            print(f"  - Minimal: {'Yes' if args.minimal else 'No'}")
        print(f"Output: {args.output}")
        print_separator()

    # Extract data
    if not args.quiet:
        print("\n⚙️  Extracting data...")

    result = extractor.extract(
        args.video_url,
        include_transcript=not args.no_transcript,
        include_comments=args.comments,
        include_metadata=True,
        language=args.lang,
        max_comments=args.max_comments,
        comment_sort=args.comment_sort
    )

    # Check if extraction was successful
    if not result.get('success'):
        print(f"\n❌ Extraction failed: {result.get('error', 'Unknown error')}")
        sys.exit(1)

    # Get metadata for later use
    metadata = result.get('metadata', {})

    # Display results
    if not args.quiet:
        print_section("✅ Extraction Results")

        # Metadata
        if metadata:
            print(f"📺 Title: {metadata.get('title', 'Unknown')}")
            print(f"📅 Duration: {metadata.get('duration_string', 'Unknown')}")
            print(f"👤 Channel: {metadata.get('uploader', 'Unknown')}")
            print(f"👁  Views: {metadata.get('view_count', 'Unknown'):,}")

        # Transcript
        transcript = result.get('transcript', {})
        if transcript and transcript.get('success'):
            print_section("📝 Transcript")
            print(f"  Method: {transcript.get('method', 'unknown')}")
            print(f"  Format: {transcript.get('format', 'unknown')}")
            print(f"  Lines: {transcript.get('line_count', 0)}")
            print(f"  Deduplication: {transcript.get('deduplication_effectiveness', 0):.1f}% removed")

            quality = transcript.get('quality_metrics', {})
            if quality:
                print(f"  Quality Score: {quality.get('quality_score', 0):.1f}% ({quality.get('quality_rating', 'Unknown')})")
                if quality.get('quality_warnings'):
                    print(f"  ⚠️  Warnings: {len(quality['quality_warnings'])}")
                    if args.debug:
                        for warning in quality['quality_warnings']:
                            print(f"    - {warning}")
        elif not args.no_transcript:
            print_section("❌ Transcript")
            print(f"  Error: {transcript.get('error', 'Unknown error')}")

        # Comments
        comments_data = result.get('comments', {})
        if comments_data and comments_data.get('success'):
            print_section("💬 Comments")
            stats = comments_data.get('statistics', {})
            print(f"  Extracted: {stats.get('total_comments', 0)} comments")
            print(f"  Total likes: {stats.get('total_likes', 0):,}")
            print(f"  Avg likes: {stats.get('avg_likes_per_comment', 0)}")
            print(f"  Uploader comments: {stats.get('uploader_comments', 0)}")

            analytics = comments_data.get('analytics', {})
            if analytics:
                print(f"  Engagement score: {analytics.get('engagement_score', 0):.1f}%")
        elif args.comments:
            print_section("❌ Comments")
            print(f"  Error: {comments_data.get('error', 'Unknown error')}")

    # Save output
    video_id = result.get('video_id', 'unknown')
    title = metadata.get('title', f'Video {video_id}') if metadata else f'Video {video_id}'

    # Create output directory
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    saved_files = []

    # Save as markdown
    if args.format in ['markdown', 'both']:
        filename = create_safe_filename(title, video_id, args.minimal, 'md')
        filepath = output_dir / filename

        if save_as_markdown(result, str(filepath), minimal=args.minimal):
            saved_files.append(str(filepath))
            if not args.quiet:
                print(f"\n💾 Saved Markdown: {filepath}")
        else:
            print(f"\n❌ Failed to save Markdown: {filepath}")

    # Save as JSON
    if args.format in ['json', 'both']:
        filename = create_safe_filename(title, video_id, False, 'json')
        filepath = output_dir / filename

        if save_as_json(result, str(filepath)):
            saved_files.append(str(filepath))
            if not args.quiet:
                print(f"💾 Saved JSON: {filepath}")
        else:
            print(f"❌ Failed to save JSON: {filepath}")

    # Final summary
    if not args.quiet:
        print_separator()
        print(f"🎉 Extraction complete! Saved {len(saved_files)} file(s)")
        print_separator()

    # Debug output
    if args.debug:
        print_section("🔍 Debug Information")
        print(f"Video ID: {video_id}")
        print(f"Extraction timestamp: {result.get('extracted_at', 'unknown')}")
        if transcript and transcript.get('success'):
            print(f"Transcript format used: {transcript.get('format', 'unknown')}")
            print(f"Original line count: {transcript.get('original_line_count', 0)}")
            print(f"Final line count: {transcript.get('line_count', 0)}")

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
