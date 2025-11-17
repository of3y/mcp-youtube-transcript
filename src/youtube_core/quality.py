"""
Quality analysis for transcripts and comments.
"""

from typing import List, Dict, Any


def analyze_transcript_quality(
    lines: List[str],
    video_info: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Analyze the quality of a transcript with comprehensive metrics.

    Args:
        lines: List of transcript lines
        video_info: Optional video metadata for context-aware validation

    Returns:
        Dictionary containing quality metrics and warnings
    """
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

    # Safety validation
    quality_warnings = []
    safety_penalties = 0

    full_text = ' '.join(text_lines).lower()

    # Check for excessive repetition of short words
    if full_text:
        words = full_text.split()
        if len(words) > 10:
            word_freq = {}
            for word in words:
                if len(word) <= 3:
                    word_freq[word] = word_freq.get(word, 0) + 1

            most_common_short = max(word_freq.values()) if word_freq else 0
            if most_common_short > len(words) * 0.15:
                quality_warnings.append("High repetition of short words detected")
                safety_penalties += 15

    # Check for incoherent character sequences
    if full_text:
        special_char_ratio = sum(
            1 for c in full_text
            if not c.isalnum() and c not in ' .,!?;:-\'"'
        ) / len(full_text)
        if special_char_ratio > 0.05:
            quality_warnings.append("Excessive special characters suggest garbled content")
            safety_penalties += 20

    # Duration validation (if video info available)
    if video_info and 'duration' in video_info:
        expected_lines = video_info['duration'] / 3
        if total_lines > expected_lines * 2:
            quality_warnings.append("Transcript length seems excessive for video duration")
            safety_penalties += 10
        elif total_lines < expected_lines * 0.3:
            quality_warnings.append("Transcript seems too short for video duration")
            safety_penalties += 15

    # Language consistency check
    if full_text:
        english_words = {'the', 'and', 'is', 'to', 'of', 'in', 'for', 'with', 'on', 'as', 'by', 'this', 'that'}
        words_lower = set(full_text.split())
        english_word_ratio = len(english_words.intersection(words_lower)) / len(english_words)

        if english_word_ratio < 0.3 and len(words_lower) > 20:
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
            for seen_text in seen_texts:
                if (clean_text in seen_text or seen_text in clean_text) and clean_text != seen_text:
                    partial_duplicates += 1
                    break
            seen_texts.add(clean_text)

    # Text quality metrics
    total_words = sum(len(text.split()) for text in text_lines)
    avg_words_per_line = total_words / len(text_lines) if text_lines else 0

    # Punctuation analysis
    punctuation_chars = sum(1 for line in text_lines for char in line if char in '.,!?;:')
    has_punctuation = punctuation_chars > len(text_lines) * 0.1

    # Timestamp coverage
    timestamped_lines = sum(1 for line in lines if line.startswith('['))
    timestamp_coverage = timestamped_lines / total_lines if total_lines > 0 else 0

    # Calculate quality score (0-100)
    quality_score = 0

    # Line count factor
    if total_lines > 10:
        quality_score += min(30, total_lines * 0.5)

    # Average line length
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
        quality_warnings.append("⚠️  High structural score but content quality concerns detected")

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
        'quality_score': round(quality_score, 1),
        'safety_penalties': safety_penalties,
        'quality_warnings': quality_warnings,
        'quality_rating': (
            'Excellent' if quality_score >= 80 else
            'Good' if quality_score >= 60 else
            'Fair' if quality_score >= 40 else
            'Poor' if quality_score >= 20 else 'Very Poor'
        )
    }


def analyze_comment_quality(comments: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Analyze quality and characteristics of comments.

    Args:
        comments: List of comment dictionaries

    Returns:
        Dictionary containing comment analytics
    """
    if not comments:
        return {
            'total_comments': 0,
            'total_likes': 0,
            'avg_likes': 0,
            'engagement_score': 0
        }

    total_likes = sum(c.get('like_count', 0) for c in comments)
    uploader_comments = sum(1 for c in comments if c.get('author_is_uploader', False))

    # Text quality
    total_words = 0
    avg_comment_length = 0

    for comment in comments:
        text = comment.get('text', '')
        words = text.split()
        total_words += len(words)

    if comments:
        avg_comment_length = total_words / len(comments)

    # Find top comment
    top_comment = max(comments, key=lambda c: c.get('like_count', 0))

    # Calculate engagement score
    # Based on: likes distribution, uploader interaction, comment depth
    engagement_score = 0

    # Like distribution factor
    if total_likes > 0:
        like_variance = sum((c.get('like_count', 0) - (total_likes / len(comments))) ** 2 for c in comments)
        engagement_score += min(30, like_variance / 100)

    # Uploader interaction
    if uploader_comments > 0:
        engagement_score += min(20, uploader_comments * 5)

    # Comment length
    if avg_comment_length > 20:
        engagement_score += 25

    # Volume
    engagement_score += min(25, len(comments) * 0.5)

    return {
        'total_comments': len(comments),
        'total_likes': total_likes,
        'avg_likes': round(total_likes / len(comments), 1) if comments else 0,
        'avg_comment_length': round(avg_comment_length, 1),
        'uploader_comments': uploader_comments,
        'engagement_score': round(min(100, engagement_score), 1),
        'top_comment': {
            'author': top_comment.get('author', 'Unknown'),
            'likes': top_comment.get('like_count', 0),
            'text_preview': top_comment.get('text', '')[:100]
        }
    }
