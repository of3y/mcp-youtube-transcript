"""
YouTube comment retrieval using yt-dlp.

Optimized implementation for extracting video comments with support for:
- Top comments extraction
- Reply threads
- Like counts and author information
- Sorting options (top, new, relevant)
"""

import json
import subprocess
import tempfile
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime


def extract_video_id(url: str) -> str:
    """Extract YouTube video ID from URL."""
    import re
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
    """Check if yt-dlp is installed and available."""
    try:
        subprocess.run(['yt-dlp', '--version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def extract_comments(
    video_url: str,
    max_comments: int = 100,
    sort_by: str = "top",
    include_replies: bool = False,
    max_replies: int = 3,
    timeout: int = 120
) -> Dict[str, Any]:
    """
    Extract comments from a YouTube video using yt-dlp.

    Args:
        video_url: YouTube video URL
        max_comments: Maximum number of top-level comments to extract
        sort_by: Comment sorting ('top', 'new', or 'time')
        include_replies: Whether to include comment replies
        max_replies: Maximum replies per comment if enabled
        timeout: Command timeout in seconds

    Returns:
        Dictionary containing:
        - success: bool
        - comments: List of comment dictionaries
        - count: Number of comments extracted
        - error: Error message if failed
    """
    if not check_ytdlp_available():
        return {
            'success': False,
            'error': 'yt-dlp not available - install with: pip install yt-dlp',
            'comments': [],
            'count': 0
        }

    try:
        # Build yt-dlp command for comment extraction
        cmd = [
            'yt-dlp',
            '--skip-download',
            '--write-comments',
            '--extractor-args', f'youtube:comment_sort={sort_by};max_comments={max_comments}',
            '--print-json',
            '--no-warnings',
            video_url
        ]

        # Execute command with timeout
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout
        )

        if result.returncode != 0:
            return {
                'success': False,
                'error': f'yt-dlp failed: {result.stderr}',
                'comments': [],
                'count': 0
            }

        # Parse JSON output
        try:
            video_info = json.loads(result.stdout.split('\n')[0])
            raw_comments = video_info.get('comments', [])
        except (json.JSONDecodeError, IndexError) as e:
            return {
                'success': False,
                'error': f'Failed to parse yt-dlp output: {e}',
                'comments': [],
                'count': 0
            }

        # Process and format comments
        formatted_comments = []

        for comment in raw_comments[:max_comments]:
            formatted_comment = {
                'id': comment.get('id', ''),
                'author': comment.get('author', 'Unknown'),
                'author_id': comment.get('author_id', ''),
                'text': comment.get('text', ''),
                'timestamp': comment.get('timestamp', 0),
                'time_text': comment.get('time_text', ''),
                'like_count': comment.get('like_count', 0),
                'is_favorited': comment.get('is_favorited', False),
                'author_is_uploader': comment.get('author_is_uploader', False),
                'parent': comment.get('parent', 'root')
            }

            # Add replies if requested and available
            if include_replies and '_replies' in comment:
                replies = comment['_replies'][:max_replies] if max_replies else comment['_replies']
                formatted_comment['replies'] = [
                    {
                        'author': r.get('author', 'Unknown'),
                        'text': r.get('text', ''),
                        'like_count': r.get('like_count', 0),
                        'time_text': r.get('time_text', '')
                    }
                    for r in replies
                ]
                formatted_comment['reply_count'] = len(comment.get('_replies', []))

            formatted_comments.append(formatted_comment)

        return {
            'success': True,
            'comments': formatted_comments,
            'count': len(formatted_comments),
            'total_available': len(raw_comments),
            'sort_by': sort_by,
            'extracted_at': datetime.now().isoformat()
        }

    except subprocess.TimeoutExpired:
        return {
            'success': False,
            'error': f'Comment extraction timed out after {timeout} seconds',
            'comments': [],
            'count': 0
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'Unexpected error: {str(e)}',
            'comments': [],
            'count': 0
        }


def format_comments_as_text(
    comments: List[Dict[str, Any]],
    include_metadata: bool = True,
    include_replies: bool = False
) -> str:
    """
    Format comments as readable text.

    Args:
        comments: List of comment dictionaries
        include_metadata: Include like counts and timestamps
        include_replies: Include reply threads

    Returns:
        Formatted text string
    """
    if not comments:
        return "No comments available."

    lines = []

    for i, comment in enumerate(comments, 1):
        # Comment header
        author = comment.get('author', 'Unknown')
        is_uploader = comment.get('author_is_uploader', False)
        uploader_badge = " 👤 [UPLOADER]" if is_uploader else ""

        lines.append(f"\n{'='*80}")
        lines.append(f"Comment #{i} - {author}{uploader_badge}")

        if include_metadata:
            like_count = comment.get('like_count', 0)
            time_text = comment.get('time_text', 'unknown')
            lines.append(f"👍 {like_count} likes · Posted {time_text}")

        lines.append(f"{'-'*80}")

        # Comment text
        text = comment.get('text', '').strip()
        lines.append(text)

        # Replies if available
        if include_replies and 'replies' in comment:
            replies = comment['replies']
            reply_count = comment.get('reply_count', len(replies))

            if replies:
                lines.append(f"\n  ↳ {len(replies)} of {reply_count} replies:")
                for reply in replies:
                    reply_author = reply.get('author', 'Unknown')
                    reply_text = reply.get('text', '').strip()
                    reply_likes = reply.get('like_count', 0)

                    lines.append(f"\n    • {reply_author} (👍 {reply_likes})")
                    lines.append(f"      {reply_text}")

    lines.append(f"\n{'='*80}\n")

    return '\n'.join(lines)


def format_comments_as_markdown(
    comments: List[Dict[str, Any]],
    video_title: str = "Video",
    include_replies: bool = False
) -> str:
    """
    Format comments as markdown.

    Args:
        comments: List of comment dictionaries
        video_title: Video title for heading
        include_replies: Include reply threads

    Returns:
        Markdown formatted string
    """
    if not comments:
        return "## Comments\n\nNo comments available.\n"

    lines = [
        f"## Comments ({len(comments)})\n",
        f"*Top comments from: {video_title}*\n"
    ]

    for i, comment in enumerate(comments, 1):
        author = comment.get('author', 'Unknown')
        is_uploader = comment.get('author_is_uploader', False)
        uploader_badge = " 👤 **[UPLOADER]**" if is_uploader else ""
        like_count = comment.get('like_count', 0)
        time_text = comment.get('time_text', 'unknown')
        text = comment.get('text', '').strip()

        lines.append(f"### {i}. {author}{uploader_badge}")
        lines.append(f"*👍 {like_count} · {time_text}*\n")
        lines.append(f"{text}\n")

        # Add replies if available
        if include_replies and 'replies' in comment:
            replies = comment['replies']
            if replies:
                lines.append(f"**Replies ({len(replies)}):**\n")
                for reply in replies:
                    reply_author = reply.get('author', 'Unknown')
                    reply_text = reply.get('text', '').strip()
                    reply_likes = reply.get('like_count', 0)
                    lines.append(f"- **{reply_author}** (👍 {reply_likes}): {reply_text}")
                lines.append("")

        lines.append("---\n")

    return '\n'.join(lines)


def get_comment_statistics(comments: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculate statistics about comments.

    Args:
        comments: List of comment dictionaries

    Returns:
        Dictionary of statistics
    """
    if not comments:
        return {
            'total_comments': 0,
            'total_likes': 0,
            'avg_likes_per_comment': 0,
            'uploader_comments': 0,
            'top_comment_likes': 0
        }

    total_likes = sum(c.get('like_count', 0) for c in comments)
    uploader_comments = sum(1 for c in comments if c.get('author_is_uploader', False))
    top_comment = max(comments, key=lambda c: c.get('like_count', 0))

    return {
        'total_comments': len(comments),
        'total_likes': total_likes,
        'avg_likes_per_comment': round(total_likes / len(comments), 1),
        'uploader_comments': uploader_comments,
        'top_comment_likes': top_comment.get('like_count', 0),
        'top_comment_author': top_comment.get('author', 'Unknown')
    }
