# YouTube Standalone CLI - Complete Extraction Tool

A professional-grade, standalone command-line tool for extracting YouTube video data. Completely decoupled from the MCP server and Claude Skills.

## Features

### 🎯 Core Capabilities
- **Transcript Extraction** - Multi-format with automatic fallback (srv1 → json3 → ttml → vtt)
- **Comment Extraction** - Top comments with like counts, author info, and reply threads
- **Video Metadata** - Comprehensive video information (title, duration, views, etc.)
- **Quality Analysis** - Advanced quality scoring and validation
- **Multiple Output Formats** - Markdown (minimal or full) and JSON

### 🚀 Standalone Design
- **No MCP dependency** - Works independently of the MCP server
- **Modular architecture** - Uses `youtube_core` library
- **Flexible configuration** - Environment variables or command-line options
- **Production-ready** - Error handling, timeouts, logging

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd mcp-youtube-transcript

# Install dependencies
uv sync

# Verify installation
uv run python scripts/youtube_extract.py --help
```

## Quick Start

### Extract Transcript Only

```bash
# Basic usage
uv run python scripts/youtube_extract.py "https://youtube.com/watch?v=VIDEO_ID"

# With specific language
uv run python scripts/youtube_extract.py "https://youtube.com/watch?v=VIDEO_ID" --lang es

# Minimal format (optimized for Claude)
uv run python scripts/youtube_extract.py "https://youtube.com/watch?v=VIDEO_ID" --minimal
```

### Extract Transcript + Comments

```bash
# Top 50 comments
uv run python scripts/youtube_extract.py "https://youtube.com/watch?v=VIDEO_ID" \
  --comments --max-comments 50

# With comment replies
uv run python scripts/youtube_extract.py "https://youtube.com/watch?v=VIDEO_ID" \
  --comments --max-comments 100 --comment-replies --max-replies 5

# Sort by newest
uv run python scripts/youtube_extract.py "https://youtube.com/watch?v=VIDEO_ID" \
  --comments --comment-sort new
```

### Save in Different Formats

```bash
# Markdown (default)
uv run python scripts/youtube_extract.py "https://youtube.com/watch?v=VIDEO_ID" \
  --format markdown --output ./transcripts

# JSON
uv run python scripts/youtube_extract.py "https://youtube.com/watch?v=VIDEO_ID" \
  --format json --output ./data

# Both formats
uv run python scripts/youtube_extract.py "https://youtube.com/watch?v=VIDEO_ID" \
  --format both
```

## Command-Line Options

### Required Arguments
- `video_url` - YouTube video URL (any format: youtube.com, youtu.be, embed)

### Transcript Options
- `--lang LANG` - Language code for transcripts (default: en)
- `--no-transcript` - Skip transcript extraction

### Comment Options
- `--comments` - Extract comments
- `--max-comments N` - Maximum comments to extract (default: 100)
- `--comment-sort {top,new,time}` - Comment sorting method (default: top)
- `--comment-replies` - Include comment replies
- `--max-replies N` - Maximum replies per comment (default: 3)

### Output Options
- `--output DIR` - Output directory (default: ./output)
- `--format {markdown,json,both}` - Output format (default: markdown)
- `--minimal` - Generate minimal format optimized for Claude (markdown only)

### Behavior Options
- `--timeout SECONDS` - Command timeout in seconds (default: 60)
- `--no-dedup` - Disable aggressive deduplication
- `--debug` - Enable debug output
- `--quiet` - Minimal console output

## Usage Examples

### Example 1: Educational Video Analysis

```bash
# Extract transcript with top comments for a lecture
uv run python scripts/youtube_extract.py \
  "https://youtube.com/watch?v=LECTURE_ID" \
  --comments \
  --max-comments 50 \
  --output ./lectures \
  --format both
```

Output:
- `lectures/VIDEO_ID_Title.md` - Markdown with transcript and comments
- `lectures/VIDEO_ID_Title.json` - JSON with all data for processing

### Example 2: Quick Research

```bash
# Get minimal transcript for Claude analysis
uv run python scripts/youtube_extract.py \
  "https://youtu.be/VIDEO_ID" \
  --minimal \
  --quiet
```

Output:
- Clean, optimized markdown in `output/` directory
- Minimal console output

### Example 3: Community Analysis

```bash
# Focus on comments and engagement
uv run python scripts/youtube_extract.py \
  "https://youtube.com/watch?v=VIDEO_ID" \
  --comments \
  --max-comments 200 \
  --comment-replies \
  --comment-sort top \
  --output ./community
```

Output:
- Transcript with top 200 comments and their replies
- Comment statistics and engagement metrics

### Example 4: Multi-language Support

```bash
# Extract Spanish transcript
uv run python scripts/youtube_extract.py \
  "https://youtube.com/watch?v=VIDEO_ID" \
  --lang es \
  --output ./spanish
```

### Example 5: Batch Processing

```bash
#!/bin/bash
# Process multiple videos
VIDEOS=(
  "https://youtube.com/watch?v=VIDEO_ID1"
  "https://youtube.com/watch?v=VIDEO_ID2"
  "https://youtube.com/watch?v=VIDEO_ID3"
)

for video in "${VIDEOS[@]}"; do
  uv run python scripts/youtube_extract.py "$video" \
    --comments \
    --max-comments 50 \
    --format both \
    --output ./batch_output
done
```

## Output Formats

### Markdown Format (Default)

**Full Format** (--format markdown):
```markdown
# Video Title

## Video Information
- Video ID: ...
- Duration: ...
- Channel: ...
- Views: ...

## Transcript Information
- Method: yt-dlp
- Format: srv1
- Language: en
- Line Count: 450

## Plain Text Script
[Clean, paragraph-formatted transcript text]

## Quality Analysis
- Quality Score: 85.5%
- Quality Rating: Excellent
- Total Words: 3,200
...

## Comments (50)
### 1. Author Name 👤 [UPLOADER]
*👍 1,234 · 2 weeks ago*

Comment text here...

---
```

**Minimal Format** (--minimal):
```markdown
# Video Title

**Channel:** Channel Name | **Duration:** 12:34 | **ID:** VIDEO_ID
**URL:** https://youtube.com/watch?v=VIDEO_ID

---

[Clean plain text transcript]

---
*Extracted: 2025-11-17 | Quality: Excellent*
```

### JSON Format (--format json)

```json
{
  "success": true,
  "video_id": "VIDEO_ID",
  "video_url": "https://youtube.com/watch?v=VIDEO_ID",
  "extracted_at": "2025-11-17T14:30:00",
  "metadata": {
    "title": "Video Title",
    "uploader": "Channel Name",
    "duration": 754,
    "duration_string": "12:34",
    "view_count": 1000000,
    "like_count": 50000
  },
  "transcript": {
    "success": true,
    "method": "yt-dlp",
    "format": "srv1",
    "language": "en",
    "lines": ["[00:00] First line", "[00:03] Second line", ...],
    "line_count": 450,
    "quality_metrics": {
      "quality_score": 85.5,
      "quality_rating": "Excellent",
      "total_words": 3200
    }
  },
  "comments": {
    "success": true,
    "count": 50,
    "comments": [
      {
        "id": "...",
        "author": "User Name",
        "text": "Comment text",
        "like_count": 1234,
        "author_is_uploader": true,
        "time_text": "2 weeks ago"
      }
    ],
    "statistics": {
      "total_comments": 50,
      "total_likes": 25000,
      "avg_likes_per_comment": 500
    }
  }
}
```

## Environment Variables

Configure defaults using environment variables:

```bash
# Language
export YT_DEFAULT_LANG="en"

# Comments
export YT_MAX_COMMENTS="100"
export YT_COMMENT_SORT="top"
export YT_ENABLE_REPLIES="false"
export YT_MAX_REPLIES="3"

# Output
export YT_OUTPUT_DIR="./output"

# Behavior
export YT_TIMEOUT="60"
export YT_AGGRESSIVE_DEDUP="true"

# Then run without flags
uv run python scripts/youtube_extract.py "https://youtube.com/watch?v=VIDEO_ID"
```

## Python API Usage

You can also use the standalone `youtube_core` library programmatically:

```python
from youtube_core import YouTubeExtractor, ExtractionConfig

# Create extractor
config = ExtractionConfig(
    max_comments=100,
    comment_sort='top',
    aggressive_dedup=True
)
extractor = YouTubeExtractor(config)

# Extract transcript only
result = extractor.extract_transcript_only("https://youtube.com/watch?v=VIDEO_ID")

# Extract everything
result = extractor.extract(
    "https://youtube.com/watch?v=VIDEO_ID",
    include_transcript=True,
    include_comments=True
)

# Access data
if result['success']:
    transcript_lines = result['transcript']['lines']
    comments = result['comments']['comments']
    metadata = result['metadata']
```

## Quality Analysis

The tool provides comprehensive quality analysis:

### Transcript Quality Metrics
- **Quality Score** (0-100): Overall transcript quality
- **Quality Rating**: Excellent, Good, Fair, Poor, Very Poor
- **Deduplication Effectiveness**: Percentage of duplicates removed
- **Safety Penalties**: Points deducted for detected issues
- **Quality Warnings**: Specific issues detected

### Comment Quality Metrics
- **Engagement Score** (0-100): Comment section engagement level
- **Average Likes**: Mean likes per comment
- **Uploader Interaction**: Number of comments from video creator
- **Comment Length**: Average comment word count

## Troubleshooting

### Issue: "yt-dlp not available"
**Solution:**
```bash
uv sync
# or
pip install yt-dlp
```

### Issue: "No subtitle formats available"
**Solution:** Video may not have transcripts. Try:
- Check if video has captions on YouTube
- Try different language with `--lang`
- Check if video is available in your region

### Issue: SSL Certificate Errors
**Solution:**
- Update certificates: `pip install --upgrade certifi`
- Set `REQUESTS_CA_BUNDLE` environment variable

### Issue: Timeout Errors
**Solution:** Increase timeout:
```bash
uv run python scripts/youtube_extract.py "URL" --timeout 120
```

## Architecture

The standalone CLI is built on the `youtube_core` library:

```
src/youtube_core/
├── __init__.py         # Main exports
├── extractor.py        # Core extraction class
├── transcript.py       # Transcript extraction
├── comments.py         # Comment retrieval
├── quality.py          # Quality analysis
├── formatters.py       # Output formatting
└── config.py           # Configuration

scripts/
└── youtube_extract.py  # CLI interface
```

**Key Design Principles:**
1. **Separation of Concerns** - Each module has a single responsibility
2. **Standalone** - No MCP or Claude dependencies
3. **Reusable** - Core library can be imported and used programmatically
4. **Testable** - Modular design enables easy testing
5. **Extensible** - Easy to add new extractors or formatters

## Integration with Other Tools

### Use with Claude Desktop
```bash
# Extract and pipe to Claude
uv run python scripts/youtube_extract.py "URL" --minimal --quiet > video.md
# Then use video.md with Claude
```

### Use in Scripts
```bash
#!/bin/bash
VIDEO="https://youtube.com/watch?v=VIDEO_ID"
OUTPUT="analysis"

# Extract data
uv run python scripts/youtube_extract.py "$VIDEO" \
  --comments \
  --format both \
  --output "$OUTPUT"

# Process JSON with jq
cat "$OUTPUT"/*.json | jq '.metadata.title'
```

### Use with AI Analysis
```bash
# Extract minimal format for AI
uv run python scripts/youtube_extract.py "URL" --minimal --output ./ai_input

# Feed to your AI analysis tool
your_ai_tool ./ai_input/*.md
```

## Performance

### Typical Extraction Times
- **Transcript only**: 5-15 seconds
- **Transcript + 100 comments**: 10-25 seconds
- **Large videos (>1 hour)**: 15-30 seconds

### Resource Usage
- **Memory**: ~50-200 MB
- **Network**: ~1-5 MB per video
- **Disk**: ~10-500 KB per output file

## Comparison with Other Tools

| Feature | This Tool | youtube-transcript-api | yt-dlp directly |
|---------|-----------|----------------------|----------------|
| Transcript Extraction | ✅ Multi-format | ✅ Single format | ⚠️ Manual parsing |
| Comment Extraction | ✅ Optimized | ❌ No | ⚠️ Manual parsing |
| Quality Analysis | ✅ Advanced | ❌ No | ❌ No |
| Output Formats | ✅ MD + JSON | ❌ JSON only | ⚠️ Raw only |
| Deduplication | ✅ Intelligent | ⚠️ Basic | ❌ No |
| Standalone Use | ✅ Yes | ✅ Yes | ✅ Yes |
| MCP Integration | ✅ Optional | ❌ No | ❌ No |

## Contributing

This tool is part of the YouTube Intelligence Suite. To contribute:

1. Fork the repository
2. Create a feature branch
3. Make your changes to `src/youtube_core/`
4. Test with `scripts/youtube_extract.py`
5. Submit a pull request

## License

See main repository LICENSE file.

## Support

- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions
- **Documentation**: docs/ directory

---

**Built with ❤️ for researchers, educators, and content analysts**
