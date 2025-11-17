"""
Main YouTube extractor class that combines transcript and comment extraction.
"""

from typing import Dict, Any, Optional
from datetime import datetime

from .transcript import (
    extract_transcript,
    extract_video_id,
    get_video_metadata,
    deduplicate_transcript_lines
)
from .comments import (
    extract_comments,
    get_comment_statistics
)
from .quality import (
    analyze_transcript_quality,
    analyze_comment_quality
)
from .config import ExtractionConfig, default_config


class YouTubeExtractor:
    """
    Complete YouTube data extractor for transcripts and comments.

    Usage:
        extractor = YouTubeExtractor()
        result = extractor.extract(video_url, include_comments=True)
    """

    def __init__(self, config: Optional[ExtractionConfig] = None):
        """
        Initialize extractor with optional configuration.

        Args:
            config: ExtractionConfig instance (uses default if not provided)
        """
        self.config = config or default_config

    def extract(
        self,
        video_url: str,
        include_transcript: bool = True,
        include_comments: bool = False,
        include_metadata: bool = True,
        language: str = None,
        max_comments: int = None,
        comment_sort: str = None
    ) -> Dict[str, Any]:
        """
        Extract all data from a YouTube video.

        Args:
            video_url: YouTube video URL
            include_transcript: Extract video transcript
            include_comments: Extract video comments
            include_metadata: Extract video metadata
            language: Transcript language (uses config default if not specified)
            max_comments: Max comments to extract (uses config default if not specified)
            comment_sort: Comment sorting method (uses config default if not specified)

        Returns:
            Dictionary containing all extracted data
        """
        try:
            video_id = extract_video_id(video_url)
        except ValueError as e:
            return {
                'success': False,
                'error': str(e),
                'video_url': video_url
            }

        result = {
            'success': True,
            'video_id': video_id,
            'video_url': video_url,
            'extracted_at': datetime.now().isoformat()
        }

        # Extract metadata
        metadata = {}
        if include_metadata:
            metadata = get_video_metadata(video_url, timeout=self.config.timeout)
            result['metadata'] = metadata

        # Extract transcript
        if include_transcript:
            lang = language or self.config.default_language
            transcript_result = extract_transcript(
                video_url,
                language=lang,
                metadata=metadata,
                timeout=self.config.timeout
            )

            if transcript_result['success']:
                # Apply additional processing
                lines = transcript_result['lines']

                # Deduplicate if configured
                if self.config.aggressive_dedup:
                    lines = deduplicate_transcript_lines(lines)

                # Analyze quality
                quality_metrics = analyze_transcript_quality(
                    lines,
                    video_info={'duration': metadata.get('duration', 0)} if metadata else {}
                )

                result['transcript'] = {
                    'success': True,
                    'method': transcript_result['method'],
                    'format': transcript_result.get('format', 'unknown'),
                    'language': lang,
                    'lines': lines,
                    'line_count': len(lines),
                    'original_line_count': transcript_result.get('original_line_count', len(lines)),
                    'deduplication_effectiveness': transcript_result.get('deduplication_effectiveness', 0),
                    'quality_metrics': quality_metrics
                }
            else:
                result['transcript'] = {
                    'success': False,
                    'error': transcript_result.get('error', 'Unknown error'),
                    'lines': []
                }

        # Extract comments
        if include_comments:
            max_comm = max_comments or self.config.max_comments
            sort = comment_sort or self.config.comment_sort

            comments_result = extract_comments(
                video_url,
                max_comments=max_comm,
                sort_by=sort,
                include_replies=self.config.enable_replies,
                max_replies=self.config.max_replies_per_comment,
                timeout=self.config.timeout
            )

            if comments_result['success']:
                comments = comments_result['comments']

                # Analyze comment quality
                comment_analytics = analyze_comment_quality(comments)
                comment_stats = get_comment_statistics(comments)

                result['comments'] = {
                    'success': True,
                    'comments': comments,
                    'count': len(comments),
                    'sort_by': sort,
                    'statistics': comment_stats,
                    'analytics': comment_analytics
                }
            else:
                result['comments'] = {
                    'success': False,
                    'error': comments_result.get('error', 'Unknown error'),
                    'comments': []
                }

        return result

    def extract_transcript_only(
        self,
        video_url: str,
        language: str = None
    ) -> Dict[str, Any]:
        """
        Quick method to extract only transcript.

        Args:
            video_url: YouTube video URL
            language: Transcript language

        Returns:
            Transcript extraction result
        """
        return self.extract(
            video_url,
            include_transcript=True,
            include_comments=False,
            include_metadata=True,
            language=language
        )

    def extract_comments_only(
        self,
        video_url: str,
        max_comments: int = None,
        sort_by: str = None
    ) -> Dict[str, Any]:
        """
        Quick method to extract only comments.

        Args:
            video_url: YouTube video URL
            max_comments: Maximum comments to extract
            sort_by: Comment sorting method

        Returns:
            Comment extraction result
        """
        return self.extract(
            video_url,
            include_transcript=False,
            include_comments=True,
            include_metadata=True,
            max_comments=max_comments,
            comment_sort=sort_by
        )
