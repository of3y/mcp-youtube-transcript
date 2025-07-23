# Configuration Guide

> **🎉 Updated for v0.3.0:** Enhanced architecture with tools, resources, and prompts! Simplified configuration - no API keys required!

This guide walks you through configuring the YouTube Video Intelligence Suite with Claude Desktop.

## Prerequisites

Before configuring, ensure you have:
- ✅ Completed the [Installation Guide](installation.md)
- ✅ Claude Desktop installed
- ✅ **No API keys needed!** 🎉

## Claude Desktop Configuration

### 1. Locate Configuration File

The Claude Desktop configuration file is located at:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

### 2. Enhanced v0.3.0 Configuration Format

Add the YouTube Video Intelligence Suite to your Claude Desktop configuration:

```json
{
  "mcpServers": {
    "youtube-intelligence": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/your/mcp-youtube-transcript", "python", "main.py"]
    }
  }
}
```

> **Note**: The enhanced server (`main.py`) provides tools, resources, and prompts. For legacy compatibility, you can still use `server.py` if needed.
```

### 3. Update Paths

Replace `/path/to/your/mcp-youtube-transcript/server.py` with the actual path to your installation:

```bash
# Find your installation path
pwd
# Example output: /Users/username/Coding/mcp-youtube-transcript
```

Update the configuration:
```json
{
  "mcpServers": {
    "youtube-intelligence": {
      "command": "uv",
      "args": ["run", "--directory", "/Users/username/Coding/mcp-youtube-transcript", "python", "main.py"]
    }
  }
}
```

## Enhanced Features in v0.3.0

The enhanced server provides:

### 🛠️ Tools (20 total)
- **11 Analysis Tools**: Complete video intelligence suite
- **8 Resource Mirror Tools**: Access to cached data and analytics
- **1 Resource Listing Tool**: Browse available resources

### 📊 Resources (8 dynamic resources)
- `transcripts://cached` - Browse all cached transcripts
- `transcripts://{video_id}/metadata` - Video information
- `analytics://history` - Analysis usage patterns
- `analytics://memory_usage` - Performance monitoring
- `config://server` - Server configuration
- And more...

### 💡 Prompts (6 guided workflows)
- `transcript_analysis_workshop` - Comprehensive analysis guidance
- `video_comparison_framework` - Multi-video comparison
- `content_extraction_guide` - Content extraction workflows
- `study_notes_generator` - Educational content creation
- And more...
## Verification

### 1. Restart Claude Desktop

After updating the configuration, restart Claude Desktop completely.

### 2. Test Basic Functionality

In a new Claude Desktop conversation, try:
```
Get the transcript from: https://www.youtube.com/watch?v=jNQXAC9IVRw
```

### 3. Test Enhanced Features

Try accessing resources:
```
Show me the cached transcripts resource
```

Try using prompts:
```
Use the transcript analysis workshop prompt
```

### 4. Validate Setup

Run the validation script:
```bash
cd /path/to/your/mcp-youtube-transcript
python scripts/validate_setup.py
```

## Advanced Configuration

### Custom Python Environment

If using a virtual environment or specific Python version:

```json
{
  "mcpServers": {
    "youtube-intelligence": {
      "command": "/path/to/your/python",
      "args": ["/path/to/your/mcp-youtube-transcript/main.py"]
    }
  }
}
```

### Legacy Server Mode

For backward compatibility, you can still use the legacy server:

```json
{
  "mcpServers": {
    "youtube-intelligence": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/your/mcp-youtube-transcript", "python", "server.py"]
    }
  }
}
```

## Troubleshooting

### Common Issues

**Server not starting:**
- Check file paths are correct
- Verify Python installation and uv
- Ensure dependencies installed with `uv sync`

**Tools not appearing:**
- Restart Claude Desktop completely
- Check configuration syntax
- Verify file paths are absolute

**Permission errors:**
- Check file permissions
- Verify Python executable access
- Ensure uv is in PATH

For detailed troubleshooting, see [Troubleshooting Guide](troubleshooting.md).

## Next Steps

Once configured:
1. Review [Usage Examples](examples.md) for v0.3.0 features
2. Explore [API Reference](api-reference.md) for all 20 tools
3. Try the enhanced resources and prompts!
