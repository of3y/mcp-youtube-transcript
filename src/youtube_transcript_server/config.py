"""Server configuration settings."""

import os
from typing import Optional


class Settings:
    """Application settings."""
    
    def __init__(self):
        self.server_name = "YouTube Transcript Analysis MCP Server"
        self.version = "0.3.0"
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.cache_size = int(os.getenv("CACHE_SIZE", "50"))
        self.default_language = os.getenv("DEFAULT_LANGUAGE", "en")
        # Claude Desktop has a 100,000 character limit for tool responses
        self.max_output_chars = int(os.getenv("MAX_OUTPUT_CHARS", "95000"))  # Slightly under limit
        self.enable_smart_truncation = os.getenv("ENABLE_SMART_TRUNCATION", "true").lower() == "true"
    
    @property
    def server_info(self) -> dict:
        """Get server information."""
        return {
            "name": self.server_name,
            "version": self.version,
            "log_level": self.log_level,
            "cache_size": self.cache_size,
            "default_language": self.default_language,
            "max_output_chars": self.max_output_chars,
            "enable_smart_truncation": self.enable_smart_truncation
        }


settings = Settings()


def smart_truncate_output(content: str, url: str = "") -> str:
    """
    Smart truncation for Claude Desktop's 100k character limit.
    
    Args:
        content: The full content to potentially truncate
        url: Optional video URL for context
        
    Returns:
        Truncated content with helpful information about the truncation
    """
    if not settings.enable_smart_truncation or len(content) <= settings.max_output_chars:
        return content
    
    # Calculate how much space we need for our truncation message
    truncation_message = f"""

📋 **TRANSCRIPT TRUNCATED** 
This transcript was truncated due to Claude Desktop's 100,000 character display limit.

**Full transcript stats:**
- Total length: {len(content):,} characters
- Showing: {settings.max_output_chars:,} characters ({(settings.max_output_chars/len(content)*100):.1f}%)

**To get the full transcript:**
- Use `search_transcript` to find specific content
- Request specific time ranges or topics
- Use analysis tools which process the full transcript internally

**Available options:**
- Set MAX_OUTPUT_CHARS environment variable to adjust limit
- Set ENABLE_SMART_TRUNCATION=false to disable this feature
---"""
    
    # Reserve space for the truncation message
    available_chars = settings.max_output_chars - len(truncation_message)
    
    if available_chars < 1000:  # If not enough space, use simple truncation
        return content[:settings.max_output_chars - 100] + "\n\n[TRUNCATED - Output too long for display]"
    
    # Try to truncate at a reasonable boundary (timestamp line)
    lines = content.split('\n')
    truncated_lines = []
    current_length = 0
    
    for line in lines:
        if current_length + len(line) + 1 > available_chars:
            break
        truncated_lines.append(line)
        current_length += len(line) + 1  # +1 for newline
    
    # If we couldn't fit any complete lines, just truncate at character limit
    if not truncated_lines:
        return content[:available_chars] + truncation_message
    
    return '\n'.join(truncated_lines) + truncation_message


def format_transcript_summary(content: str, url: str = "") -> str:
    """
    Create a summary when full transcript is too long for display.
    
    Args:
        content: The full transcript content
        url: Video URL for context
        
    Returns:
        Formatted summary with key statistics and sample content
    """
    lines = content.split('\n')
    
    # Extract transcript lines (skip headers)
    transcript_lines = []
    for line in lines:
        if line.strip() and (line.startswith('[') or any(char.isdigit() for char in line[:10])):
            transcript_lines.append(line.strip())
    
    total_lines = len(transcript_lines)
    total_chars = len(content)
    
    # Show first 20 and last 10 lines as preview
    preview_lines = []
    if total_lines > 30:
        preview_lines.extend(transcript_lines[:20])
        preview_lines.append("\n... [MIDDLE CONTENT TRUNCATED] ...\n")
        preview_lines.extend(transcript_lines[-10:])
    else:
        preview_lines = transcript_lines
    
    summary = f"""📊 **TRANSCRIPT SUMMARY** 
{f"Video: {url}" if url else ""}

**Statistics:**
- Total transcript lines: {total_lines:,}
- Total characters: {total_chars:,}
- Estimated duration: ~{total_lines * 3 // 60} minutes

**Preview (showing ~30 lines):**

{chr(10).join(preview_lines)}

---
**💡 TIP:** Use analysis tools like `analyze_video_comprehensive` or `search_transcript` to work with the full content.
The complete transcript is cached and available for analysis - this summary is just for display purposes."""

    return summary
