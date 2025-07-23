# Scripts Directory

This directory contains essential utility scripts for the YouTube Video Intelligence Suite.

## Available Scripts

### 🔧 Core Tools

#### `youtube_to_mcp.py`
Core transcript extraction tool that works independently of Claude Desktop.

```bash
cd /Users/dkck/Coding/mcp-youtube-transcript
uv run python scripts/youtube_to_mcp.py "https://youtube.com/watch?v=VIDEO_ID"
```

### ✅ Validation

#### `validate_setup.py`
Comprehensive validation script that checks:
- Environment variables (API keys)
- Claude Desktop configuration
- Project structure
- Available tools
- Setup completeness

```bash
cd /Users/dkck/Coding/mcp-youtube-transcript
uv run python scripts/validate_setup.py
```

## Usage Tips

- Run `validate_setup.py` first to ensure everything is configured correctly
- Use `youtube_to_mcp.py` for standalone transcript extraction outside Claude Desktop
- All scripts can be run independently for troubleshooting

## Script Requirements

- **Environment**: All scripts should be run with `uv run python` for proper dependency management
- **Dependencies**: Managed automatically by UV from pyproject.toml
- **API Keys**: Not required - analysis is performed by Claude Desktop
