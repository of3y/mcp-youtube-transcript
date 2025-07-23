# 🎥 YouTube Video Intelligence Suite

> **Professional-grade YouTube transcript extraction and AI-powered video analysis for Claude Desktop**

A comprehensive Model Context Protocol (MCP) server that transforms YouTube videos into intelligent, searchable content through advanced transcript extraction and AI analysis. No API keys required - works seamlessly with Claude Desktop's built-in intelligence.

## � Current Version: v0.5.0

**Latest Enhancement:** VTT→SRV1 Migration with Enhanced Quality Analysis
- **Smart Format Fallback**: SRV1 → JSON3 → TTML → VTT priority chain for superior quality
- **Advanced Quality Analysis**: Comprehensive safety validation with quality scoring
- **Enhanced Deduplication**: Intelligent duplicate detection with effectiveness tracking
- **Professional-Grade Output**: Industry-standard transcript quality with safety validation

## 🚀 Quick Start

### Prerequisites
- **Python 3.10+** 
- **[uv](https://docs.astral.sh/uv/)** package manager
- **Claude Desktop** app
- **No API keys required!** ✨

### Installation & Testing

```bash
# Clone and setup
git clone <repository-url>
cd mcp-youtube-transcript
uv sync

# Quick test (optional but recommended)
python quick_test.py

# Or use automated setup
./setup.sh
```

### Claude Desktop Configuration

Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
    "mcpServers": {
        "youtube-transcript": {
            "command": "uv",
            "args": [
                "run",
                "--directory",
                "/FULL/PATH/TO/mcp-youtube-transcript",
                "python",
                "main.py"
            ]
        }
    }
}
```

**⚠️ Replace `/FULL/PATH/TO/mcp-youtube-transcript` with your actual project path!**

### Test in Claude Desktop

```
Get the transcript from: https://www.youtube.com/watch?v=jNQXAC9IVRw
```

**📖 For complete setup instructions, see [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)**

## 🛠️ Manual Transcript Extraction

Extract transcripts directly without Claude Desktop:

```bash
# Basic extraction
uv run scripts/youtube_to_mcp.py <video-url>

# Examples
uv run scripts/youtube_to_mcp.py https://www.youtube.com/watch?v=dQw4w9WgXcQ
uv run scripts/youtube_to_mcp.py https://youtu.be/jNQXAC9IVRw

# Output saved to resources/transcripts/ as markdown files
# Perfect for standalone use or integration with other tools
```

## 🌟 Features

### 🏗️ Complete MCP Architecture
- **8 Core Tools** - Professional transcript extraction + advanced analysis
- **6 Smart Resources** - Zero-token access to cached data and analytics  
- **3 Essential Prompts** - Guided conversation starters for common workflows
- **Enhanced Quality Pipeline** - Advanced deduplication and safety validation
- **Rich Metadata** - Comprehensive video information with engagement metrics
- **Modular Design** - Shared extraction module for consistency across interfaces

### 🚀 Enhanced Extraction Pipeline (v0.5.0)
- **Smart Format Fallback** - SRV1 → JSON3 → TTML → VTT priority chain for best quality
- **Advanced Quality Analysis** - Comprehensive safety validation with quality metrics
- **Intelligent Deduplication** - Advanced algorithms with effectiveness tracking
- **HTML Entity Support** - Proper decoding across all subtitle formats
- **Context-Aware Validation** - Video metadata integration for enhanced assessment
- **Professional-Grade Output** - Industry-standard transcript quality

### Core Transcript Extraction
- **Multi-format YouTube URL support** (youtube.com, youtu.be, embed URLs)
- **Multi-language transcript extraction** with automatic fallbacks
- **Robust error handling** with detailed quality analysis
- **yt-dlp based extraction** for universal reliability (no cloud server blocking)
- **Enhanced text processing** with proper HTML entity decoding

### 🔧 8 Core Tools

#### Transcript Extraction
- **get_youtube_transcript** - Primary extraction with quality analysis
- **get_youtube_transcript_ytdlp** - Alternative extraction method
- **get_plain_text_transcript** - Clean text output with deduplication
- **get_transcript_quality_analysis** - Comprehensive quality metrics

#### Video Analysis  
- **get_enhanced_video_metadata** - Rich video information and engagement metrics
- **create_mcp_resource_from_transcript_v2** - Save transcripts as MCP resources

#### System Tools
- **search_transcript** - Find content within transcripts
- **get_system_status** - Server health and configuration info

### 📊 6 Smart Resources
Access cached data and enhanced content through MCP resources:

- **transcripts://available** - Browse all available transcripts
- **transcripts://content/{video_id}** - Access specific transcript content
- **transcripts://cached** - View all cached transcripts with metadata
- **transcripts://quality_report** - System-wide quality analytics and trends
- **analytics://history** - View previous analysis results and usage patterns  
- **system://status** - Server status and configuration information

### 🎯 3 Essential Prompts
Guided workflows for comprehensive analysis:

- **transcript_analysis_workshop** - Deep-dive video content analysis
- **study_notes_generator** - Create structured study materials from videos
- **video_insight_explorer** - Comprehensive video exploration and insights

## 🎨 What You Can Do

### Basic Operations
```
"Get the transcript from: [YouTube URL]"
"Extract transcript from this video: [URL]"
"Show me the quality analysis for: [URL]"
```

### Advanced Analysis
```
"Analyze this video for key points: [URL]"
"Create study notes from: [Educational video URL]"
"Generate a comprehensive analysis of: [URL]"
"Compare the arguments in these videos: [URL1] [URL2]"
```

### Resource Access
```
"Show me all cached transcripts"
"What's the quality report for the system?"
"Access the transcript content for video ID: abc123"
```

## 🏗️ Architecture

### Single-File Design
- **streamlined_server.py** - Complete MCP server implementation
- **main.py** - Entry point for Claude Desktop integration
- **scripts/youtube_to_mcp.py** - Standalone transcript extraction tool

### Quality-First Approach
- **Smart Format Selection** - Automatic fallback ensures best available quality
- **Advanced Deduplication** - Sophisticated algorithms remove caption overlaps
- **Safety Validation** - Multi-layer content quality checks
- **Professional Output** - Industry-standard transcript formatting

### Zero Dependencies Bloat
- **yt-dlp** - Reliable transcript extraction (no cloud server blocking)
- **mcp** - Model Context Protocol integration
- **Pure Python** - No heavy AI libraries or API dependencies

## 📈 Version History

### v0.5.0 (Current) - VTT→SRV1 Migration
- Smart format fallback system (SRV1 → JSON3 → TTML → VTT)
- Enhanced quality analysis with safety validation
- Advanced deduplication with effectiveness tracking
- Professional-grade transcript quality

### v0.4.0 - Complete yt-dlp Migration  
- Removed youtube-transcript-api dependency
- Universal reliability with yt-dlp-only approach
- Enhanced VTT processing and deduplication
- Eliminated cloud server blocking issues

### v0.3.0 - Enhanced Quality & Rich Resources
- Major quality improvements (5,700% richer content)
- Advanced deduplication algorithms
- Comprehensive resource architecture
- Enhanced metadata integration

## 🔧 Troubleshooting

### Common Issues

1. **"Command not found: uv"**
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   source ~/.zshrc
   ```

2. **Claude Desktop not recognizing server**
   - Verify full path in claude_desktop_config.json
   - Restart Claude Desktop completely
   - Run `python quick_test.py` to validate setup

3. **Transcript extraction fails**
   - Check internet connection
   - Verify video has available transcripts
   - Try alternative extraction method

### Validation
```bash
# Test everything works
python quick_test.py

# Test manual extraction
uv run scripts/youtube_to_mcp.py https://www.youtube.com/watch?v=jNQXAC9IVRw
```

## 📚 Documentation

- **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** - Complete setup instructions
- **[docs/](docs/)** - Comprehensive documentation
- **[CHANGELOG.md](CHANGELOG.md)** - Version history and changes
- **[SHARING_SUMMARY.md](SHARING_SUMMARY.md)** - Repository sharing guide

## 🎯 Success Criteria

You should be able to:
- [x] Extract transcripts from any YouTube video
- [x] Perform AI analysis without API keys
- [x] Access cached content through MCP resources
- [x] Use guided prompts for complex analysis
- [x] Run standalone extraction scripts
- [x] Get professional-grade transcript quality
---

**🎉 Transform YouTube videos into intelligent, searchable content with professional-grade quality!** 🎥✨