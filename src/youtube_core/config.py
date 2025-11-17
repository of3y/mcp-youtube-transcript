"""
Configuration settings for YouTube extraction core.
"""

import os
from pathlib import Path
from typing import Optional


class ExtractionConfig:
    """Configuration for YouTube data extraction."""

    def __init__(
        self,
        default_language: str = "en",
        max_comments: int = 100,
        comment_sort: str = "top",  # top, new, or relevant
        enable_replies: bool = False,
        max_replies_per_comment: int = 3,
        output_dir: Optional[str] = None,
        temp_dir: Optional[str] = None,
        timeout: int = 60,
        aggressive_dedup: bool = True,
    ):
        self.default_language = default_language
        self.max_comments = max_comments
        self.comment_sort = comment_sort
        self.enable_replies = enable_replies
        self.max_replies_per_comment = max_replies_per_comment
        self.output_dir = Path(output_dir) if output_dir else Path("./output")
        self.temp_dir = temp_dir
        self.timeout = timeout
        self.aggressive_dedup = aggressive_dedup

    @classmethod
    def from_env(cls) -> "ExtractionConfig":
        """Create config from environment variables."""
        return cls(
            default_language=os.getenv("YT_DEFAULT_LANG", "en"),
            max_comments=int(os.getenv("YT_MAX_COMMENTS", "100")),
            comment_sort=os.getenv("YT_COMMENT_SORT", "top"),
            enable_replies=os.getenv("YT_ENABLE_REPLIES", "false").lower() == "true",
            max_replies_per_comment=int(os.getenv("YT_MAX_REPLIES", "3")),
            output_dir=os.getenv("YT_OUTPUT_DIR"),
            timeout=int(os.getenv("YT_TIMEOUT", "60")),
            aggressive_dedup=os.getenv("YT_AGGRESSIVE_DEDUP", "true").lower() == "true",
        )


# Default configuration instance
default_config = ExtractionConfig()
