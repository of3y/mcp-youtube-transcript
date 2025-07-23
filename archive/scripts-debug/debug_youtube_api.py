#!/usr/bin/env python3
"""
Debug YouTube Transcript Issues (DEPRECATED)

This script was used to debug youtube-transcript-api issues, but that method
has been removed from the main tool due to frequent blocking on cloud servers.

The main tool now uses only yt-dlp, which is more reliable.
Use the main youtube_to_mcp.py script instead.
"""

import sys

def main():
    print("⚠️  This debug script is deprecated.")
    print("The youtube-transcript-api method has been removed from the main tool")
    print("due to frequent blocking issues on cloud servers.")
    print()
    print("📝 Use the main tool instead:")
    print("   uv run python scripts/youtube_to_mcp.py <youtube_url>")
    print()
    print("� The main tool now uses only yt-dlp, which is more reliable")
    print("   and works consistently across all environments.")

if __name__ == "__main__":
    main()
