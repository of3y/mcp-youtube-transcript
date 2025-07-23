# Installation Guide

> **🎉 Updated for v0.3.0:** Enhanced MCP architecture with tools, resources, and prompts! No API keys required - works seamlessly with Claude Desktop's built-in intelligence.

## Prerequisites

- **Python 3.10+** 
- **[uv](https://docs.astral.sh/uv/)** package manager
- **Claude Desktop** app
- **No API keys needed!** ✨

## Step 1: Install uv Package Manager

If you don't have uv installed:

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or with Homebrew
brew install uv
```

## Step 2: Clone and Setup Project

```bash
# Clone the repository
git clone <repository-url>
cd mcp-youtube-transcript

# Install dependencies (much simpler now!)
uv sync
```

## Step 3: Configure Claude Desktop

> **No API keys needed!** Skip the old API key setup steps.

### Option 1: Quick Configuration
```bash
source ~/.zshrc
```

## Step 5: Configure Claude Desktop

Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
    "mcpServers": {
        "youtube-transcript": {
            "command": "uv",
            "args": [
                "run",
                "--directory",
                "/path/to/your/mcp-youtube-transcript",
                "python",
                "main.py"
            ],
        }
    }
}
```

**Important:** Replace `/path/to/your/mcp-youtube-transcript` with the actual path to your project.

## Step 4: Test Installation

```bash
# Validate setup
cd /path/to/your/mcp-youtube-transcript
python3 scripts/validate_setup.py
```

## Step 5: Start Using

1. **Restart Claude Desktop** completely
2. Test with: `"Get the transcript from: https://www.youtube.com/watch?v=jNQXAC9IVRw"`
3. Try AI analysis: `"Analyze this video for key points: [video URL]"`

## Verification Checklist

- [ ] uv installed and working
- [ ] Project dependencies installed (`uv sync`)
- [ ] ✅ No API keys needed!
- [ ] Claude Desktop config updated with correct paths
- [ ] Validation script passes all checks
- [ ] Claude Desktop restarted
- [ ] Basic transcript test works

## Next Steps

- See [Usage Examples](examples.md) for what you can do
- Check [Troubleshooting](troubleshooting.md) if you have issues
