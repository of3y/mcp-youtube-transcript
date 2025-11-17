"""
Output formatters for transcripts and comments.

Provides multiple output formats:
- Plain text (clean, readable)
- Markdown (structured, rich)
- JSON (machine-readable)
"""

import re
import json
from typing import List, Dict, Any
from datetime import datetime


def create_plain_text_script(
    lines: List[str],
    remove_duplicates: bool = True,
    aggressive_dedup: bool = False
) -> str:
    """
    Create a clean plain text script from timestamped transcript lines.

    Args:
        lines: List of transcript lines with timestamps
        remove_duplicates: Whether to remove consecutive duplicate text
        aggressive_dedup: Whether to use aggressive deduplication

    Returns:
        Clean plain text script without timestamps
    """
    if not lines:
        return ""

    from .transcript import deduplicate_transcript_lines

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


def format_transcript_as_markdown(
    result: Dict[str, Any],
    include_metadata: bool = True,
    include_quality: bool = True,
    include_timestamped: bool = False,
    minimal: bool = False
) -> str:
    """
    Format transcript extraction result as markdown.

    Args:
        result: Extraction result dictionary
        include_metadata: Include video metadata section
        include_quality: Include quality analysis section
        include_timestamped: Include full timestamped transcript
        minimal: Use minimal format (optimized for Claude)

    Returns:
        Markdown formatted string
    """
    if not result.get('success'):
        return f"# Transcript Extraction Failed\n\nError: {result.get('error', 'Unknown error')}"

    metadata = result.get('metadata', {})
    transcript = result.get('transcript', {})
    video_id = result.get('video_id', 'unknown')
    video_url = result.get('video_url', '')
    title = metadata.get('title', f'Video {video_id}')

    if minimal:
        # Minimal format optimized for Claude
        duration_str = metadata.get('duration_string', 'Unknown')
        channel = metadata.get('uploader', 'Unknown')
        quality_rating = transcript.get('quality_metrics', {}).get('quality_rating', 'Unknown')

        # Generate clean plain text script
        lines = transcript.get('lines', [])
        plain_script = create_plain_text_script(lines, remove_duplicates=True, aggressive_dedup=True)

        markdown = f"""# {title}

**Channel:** {channel} | **Duration:** {duration_str} | **ID:** {video_id}
**URL:** {video_url}

---

{plain_script}

---
*Extracted: {datetime.now().strftime('%Y-%m-%d')} | Quality: {quality_rating}*
"""
        return markdown

    # Full format
    markdown = f"# {title}\n\n"

    # Metadata section
    if include_metadata and metadata:
        markdown += f"""## Video Information

- **Video ID:** `{video_id}`
- **URL:** {video_url}
- **Title:** {title}
- **Channel:** {metadata.get('uploader', 'Unknown')}
- **Duration:** {metadata.get('duration_string', 'Unknown')} ({metadata.get('duration', 0)} seconds)
- **Upload Date:** {metadata.get('upload_date', 'Unknown')}
- **View Count:** {metadata.get('view_count', 'Unknown'):,} views
- **Like Count:** {metadata.get('like_count', 'Unknown')}

"""

    # Transcript metadata
    if transcript.get('success'):
        markdown += f"""## Transcript Information

- **Extraction Method:** {transcript.get('method', 'unknown')}
- **Format:** {transcript.get('format', 'unknown')}
- **Language:** {transcript.get('language', 'unknown')}
- **Line Count:** {transcript.get('line_count', 0)}
- **Original Lines:** {transcript.get('original_line_count', 0)}
- **Deduplication:** {transcript.get('deduplication_effectiveness', 0):.1f}% removed

"""

    # Plain text script
    lines = transcript.get('lines', [])
    if lines:
        plain_script = create_plain_text_script(lines, remove_duplicates=True, aggressive_dedup=True)
        markdown += f"## Plain Text Script\n\n{plain_script}\n\n"

    # Quality analysis
    if include_quality and transcript.get('quality_metrics'):
        quality = transcript['quality_metrics']

        markdown += f"""## Quality Analysis

### Core Metrics
- **Quality Score:** {quality.get('quality_score', 0):.1f}%
- **Quality Rating:** {quality.get('quality_rating', 'Unknown')}
- **Total Words:** {quality.get('total_words', 0):,}
- **Average Words per Line:** {quality.get('avg_words_per_line', 0)}
- **Has Punctuation:** {'Yes ✅' if quality.get('has_punctuation', False) else 'No ❌'}

### Duplicate Analysis
- **Exact Duplicates:** {quality.get('exact_duplicates', 0)}
- **Partial Duplicates:** {quality.get('partial_duplicates', 0)}

"""

        # Quality warnings
        warnings = quality.get('quality_warnings', [])
        if warnings:
            markdown += "### 🚨 Quality Warnings\n\n"
            for warning in warnings:
                markdown += f"- {warning}\n"
            markdown += "\n"

    # Timestamped transcript (optional, can be very long)
    if include_timestamped and lines:
        markdown += f"## Timestamped Transcript\n\n"
        for line in lines[:100]:  # Limit to first 100 lines to avoid huge output
            markdown += f"{line}\n"

        if len(lines) > 100:
            markdown += f"\n*... and {len(lines) - 100} more lines*\n\n"

    return markdown


def format_comments_as_markdown(
    result: Dict[str, Any],
    include_statistics: bool = True,
    max_display: int = 50
) -> str:
    """
    Format comment extraction result as markdown.

    Args:
        result: Extraction result dictionary
        include_statistics: Include comment statistics
        max_display: Maximum comments to display

    Returns:
        Markdown formatted string
    """
    if not result.get('success'):
        return f"# Comment Extraction Failed\n\nError: {result.get('error', 'Unknown error')}"

    comments_data = result.get('comments', {})
    if not comments_data.get('success'):
        return f"# Comment Extraction Failed\n\nError: {comments_data.get('error', 'Unknown error')}"

    comments = comments_data.get('comments', [])
    metadata = result.get('metadata', {})
    title = metadata.get('title', 'Video')

    markdown = f"## Comments ({len(comments)})\n\n"
    markdown += f"*Top comments from: {title}*\n\n"

    # Statistics
    if include_statistics and comments_data.get('statistics'):
        stats = comments_data['statistics']
        markdown += f"""### Statistics

- **Total Comments Extracted:** {stats.get('total_comments', 0)}
- **Total Likes:** {stats.get('total_likes', 0):,}
- **Average Likes per Comment:** {stats.get('avg_likes_per_comment', 0)}
- **Uploader Comments:** {stats.get('uploader_comments', 0)}
- **Top Comment:** {stats.get('top_comment_author', 'Unknown')} ({stats.get('top_comment_likes', 0):,} likes)

---

"""

    # Display comments
    for i, comment in enumerate(comments[:max_display], 1):
        author = comment.get('author', 'Unknown')
        is_uploader = comment.get('author_is_uploader', False)
        uploader_badge = " 👤 **[UPLOADER]**" if is_uploader else ""
        like_count = comment.get('like_count', 0)
        time_text = comment.get('time_text', 'unknown')
        text = comment.get('text', '').strip()

        markdown += f"### {i}. {author}{uploader_badge}\n"
        markdown += f"*👍 {like_count} · {time_text}*\n\n"
        markdown += f"{text}\n\n"

        # Replies if available
        if 'replies' in comment and comment['replies']:
            replies = comment['replies']
            markdown += f"**Replies ({len(replies)}):**\n\n"
            for reply in replies:
                reply_author = reply.get('author', 'Unknown')
                reply_text = reply.get('text', '').strip()
                reply_likes = reply.get('like_count', 0)
                markdown += f"- **{reply_author}** (👍 {reply_likes}): {reply_text}\n"
            markdown += "\n"

        markdown += "---\n\n"

    if len(comments) > max_display:
        markdown += f"\n*... and {len(comments) - max_display} more comments*\n"

    return markdown


def format_complete_as_markdown(
    result: Dict[str, Any],
    minimal: bool = False,
    include_comments: bool = True
) -> str:
    """
    Format complete extraction result (transcript + comments) as markdown.

    Args:
        result: Complete extraction result dictionary
        minimal: Use minimal format
        include_comments: Include comments section

    Returns:
        Markdown formatted string
    """
    # Start with transcript
    markdown = format_transcript_as_markdown(
        result,
        include_metadata=True,
        include_quality=not minimal,
        minimal=minimal
    )

    # Add comments if available and requested
    if include_comments and result.get('comments', {}).get('success'):
        markdown += "\n\n" + format_comments_as_markdown(result)

    return markdown


def save_as_json(result: Dict[str, Any], filepath: str) -> bool:
    """
    Save extraction result as JSON.

    Args:
        result: Extraction result dictionary
        filepath: Output file path

    Returns:
        True if successful, False otherwise
    """
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving JSON: {e}")
        return False


def save_as_markdown(result: Dict[str, Any], filepath: str, minimal: bool = False) -> bool:
    """
    Save extraction result as Markdown.

    Args:
        result: Extraction result dictionary
        filepath: Output file path
        minimal: Use minimal format

    Returns:
        True if successful, False otherwise
    """
    try:
        markdown = format_complete_as_markdown(result, minimal=minimal)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(markdown)
        return True
    except Exception as e:
        print(f"Error saving Markdown: {e}")
        return False
