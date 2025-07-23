#!/usr/bin/env python3
"""
Main entry point for the YouTube Transcript MCP Server.

This module provides the main entry point for running the enhanced YouTube
transcript MCP server with tools, resources, and prompts.
"""

import sys
import asyncio
from streamlined_server import main as streamlined_main


def main():
    """Main entry point for the YouTube Intelligence Suite MCP Server."""
    try:
        return streamlined_main()
    except KeyboardInterrupt:
        print("\nServer stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
