# API Reference

Complete reference for all 20 tools in the YouTube Video Intelligence Suite v0.3.0.

## Overview

The enhanced MCP server provides 20 tools organized into three categories:
- **11 Core Analysis Tools**: Primary video intelligence and content analysis capabilities
- **8 Resource Mirror Tools**: Tool access to cached data and system information
- **1 Resource Listing Tool**: Browse available resources

### Architecture Notes
- **Claude Desktop Integration**: Analysis performed directly by Claude Desktop (no API keys required)
- **Enhanced Caching**: In-memory caching with history tracking for improved performance
- **Dynamic Resources**: Real-time access to cached transcripts and analytics
- **Guided Prompts**: Pre-built conversation starters for common workflows

---

## Core Analysis Tools (11 tools)

### 1. get_youtube_transcript

**Purpose**: Extract transcript from any YouTube video with automatic language detection

**Parameters**:
- `video_url` (required): YouTube video URL
- `language` (optional): Language code (default: "en")

**Features**:
- Automatic language fallback (requested → English → auto-generated)
- Available language detection
- Enhanced caching integration
- Timestamp formatting

**Example Usage**:
```
Get the transcript from: https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

---

### 2. get_youtube_transcript_ytdlp

**Purpose**: Alternative transcript extraction using yt-dlp for increased reliability

**Parameters**:
- `video_url` (required): YouTube video URL
- `language` (optional): Language code (default: "en")

**Features**:
- yt-dlp backend for videos where standard API fails
- VTT subtitle parsing
- Automatic fallback to auto-generated subtitles
- Enhanced error handling

---

### 3. search_transcript

**Purpose**: Search for specific content within a video transcript with context

**Parameters**:
- `video_url` (required): YouTube video URL  
- `query` (required): Search term
- `context_lines` (optional): Lines of context around matches (default: 2)

**Features**:
- Case-insensitive search
- Configurable context window
- Match highlighting
- Timestamp preservation

**Example Usage**:
```
Search for "machine learning" in this video: https://www.youtube.com/watch?v=example
```

---

### 4. analyze_video_comprehensive

**Purpose**: Comprehensive AI-powered video analysis with multiple analysis types

**Parameters**:
- `video_url` (required): YouTube video URL
- `analysis_type` (optional): Type of analysis (default: "summary")
  - `summary`: Comprehensive video summary
  - `key_points`: Extract main points and insights
  - `action_items`: Identify actionable recommendations
  - `questions`: Generate discussion questions
  - `sentiment`: Analyze tone and sentiment
  - `transcript_cleanup`: Clean and organize transcript
- `custom_prompt` (optional): Custom analysis prompt (overrides analysis_type)

**Features**:
- Six pre-built analysis types
- Custom prompt support
- Claude Desktop integration for analysis
- Structured output formatting

---

### 5. extract_key_quotes

**Purpose**: Extract and analyze key quotes about a specific topic

**Parameters**:
- `video_url` (required): YouTube video URL
- `topic` (required): Topic or subject to search quotes about

**Features**:
- Topic-focused quote extraction
- Context and significance analysis
- Relevance scoring
- Quote attribution with timestamps

---

### 6. create_study_notes

**Purpose**: Generate structured study materials from video content

**Parameters**:
- `video_url` (required): YouTube video URL
- `format` (optional): Output format (default: "markdown")
  - `markdown`: Structured markdown notes
  - `outline`: Detailed outline format
  - `flashcards`: Question-answer flashcard format

**Features**:
- Three distinct note formats
- Educational content optimization
- Hierarchical organization
- Key concept highlighting

---

### 7. extract_citations_and_references

**Purpose**: Extract all references, citations, and resources mentioned in the video

**Parameters**:
- `video_url` (required): YouTube video URL

**Features**:
- Comprehensive reference extraction
- Bibliography formatting
- Multiple reference types (books, papers, websites, tools)
- Academic citation support

---

### 8. generate_quiz

**Purpose**: Create educational quizzes based on video content

**Parameters**:
- `video_url` (required): YouTube video URL
- `difficulty` (optional): Quiz difficulty (default: "medium")
  - `easy`: Basic comprehension questions
  - `medium`: Standard analysis questions
  - `hard`: Advanced critical thinking questions
- `num_questions` (optional): Number of questions 1-10 (default: 5)

**Features**:
- Multiple choice question generation
- Difficulty scaling
- Answer key inclusion
- Educational assessment focus

---

### 9. fact_check_claims

**Purpose**: Identify and analyze factual claims for verification

**Parameters**:
- `video_url` (required): YouTube video URL

**Features**:
- Factual claim identification
- Verification priority ranking
- Source requirement analysis
- Critical thinking promotion

---

### 10. extract_statistics_and_data

**Purpose**: Extract numerical data, statistics, and quantitative information

**Parameters**:
- `video_url` (required): YouTube video URL

**Features**:
- Comprehensive data extraction
- Multiple data types (percentages, dates, quantities, financial figures)
- Organized data presentation
- Data context preservation

---

### 11. compare_videos

**Purpose**: Comparative analysis of multiple videos on specific aspects

**Parameters**:
- `video_urls` (required): List of 2-4 YouTube video URLs
- `comparison_aspect` (required): Focus area for comparison

**Features**:
- Multi-video analysis (2-4 videos)
- Aspect-focused comparison
- Similarity and difference analysis
- Strength and weakness evaluation

---

### 12. analyze_presentation_style

**Purpose**: Analyze presentation style, delivery, and communication effectiveness

**Parameters**:
- `video_url` (required): YouTube video URL

**Features**:
- Presentation technique analysis
- Audience targeting assessment
- Communication effectiveness evaluation
- Style and tone analysis

---

## Resource Mirror Tools (8 tools)

These tools provide programmatic access to the same data available through MCP resources:

### 13. resource_transcripts_cached
**Purpose**: Access cached transcript information
**Returns**: Dictionary of all cached transcripts with metadata

### 14. resource_transcripts_metadata
**Purpose**: Get metadata for a specific video
**Parameters**: `video_id` (required)
**Returns**: Video metadata including title, duration, language

### 15. resource_transcripts_sample
**Purpose**: Get transcript preview/sample
**Parameters**: `video_id` (required)
**Returns**: Sample transcript lines for preview

### 16. resource_analytics_history
**Purpose**: Access analysis operation history
**Returns**: Recent analysis operations and statistics

### 17. resource_analytics_supported_languages
**Purpose**: Get supported language information
**Returns**: List of supported language codes and names

### 18. resource_analytics_memory_usage
**Purpose**: Monitor system memory usage
**Returns**: Current memory usage statistics

### 19. resource_config_server
**Purpose**: Access server configuration
**Returns**: Server settings and configuration data

### 20. resource_system_status
**Purpose**: Check system health status
**Returns**: System status and health metrics

---

## Usage Examples

### Basic Transcript Extraction
```
Tool: get_youtube_transcript
URL: https://www.youtube.com/watch?v=dQw4w9WgXcQ
Language: en
```

### Advanced Analysis
```
Tool: analyze_video_comprehensive
URL: https://www.youtube.com/watch?v=example
Analysis Type: key_points
```

### Educational Content Creation
```
Tool: create_study_notes
URL: https://www.youtube.com/watch?v=example
Format: flashcards
```

### Research and Verification
```
Tool: extract_citations_and_references
URL: https://www.youtube.com/watch?v=example
```

---

## Error Handling

All tools include comprehensive error handling for:
- Invalid video URLs
- Missing transcripts/captions
- Network connectivity issues
- Rate limiting
- API timeouts

Error messages are prefixed with ❌ and include helpful guidance for resolution.

---

## Enhanced Features in v0.3.0

- **Caching Integration**: All tools now cache results for improved performance
- **Analysis History**: Operations are tracked in analytics for insights
- **Resource Integration**: Tools work seamlessly with MCP resources
- **Enhanced Error Handling**: More detailed error messages and recovery suggestions
- **Performance Monitoring**: Built-in performance and memory usage tracking

**Output**:
- Matching transcript segments with context
- Timestamp information for each match
- Total match count

---

### 3. get_youtube_transcript_ytdlp

**Purpose**: Alternative transcript extraction using yt-dlp (fallback method)

**Parameters**:
- `video_url` (required): YouTube video URL

**Example**:
```
Extract transcript using ytdlp from: https://www.youtube.com/watch?v=example
```

## Analysis Tools

### 4. analyze_video_comprehensive

**Purpose**: Create concise summaries in various formats

**Parameters**:
- `url` (required): YouTube video URL
- `length` (optional): "brief", "medium", "detailed"
- `format` (optional): "bullet", "paragraph", "outline"

**Example**:
```
summarize_youtube_video url="https://www.youtube.com/watch?v=example" length="brief" format="bullet"
```

**Output**:
- Structured summary in requested format
- Key points and main themes
- Essential information distilled

---

### 3. extract_youtube_key_points

**Purpose**: Identify and extract the most important points

**Parameters**:
- `url` (required): YouTube video URL
- `max_points` (optional): Maximum number of key points (default: 10)

**Example**:
```
extract_youtube_key_points url="https://www.youtube.com/watch?v=example" max_points="5"
```

**Output**:
- Ranked list of key points
- Supporting context for each point
- Importance scoring

---

### 4. analyze_youtube_sentiment

**Purpose**: Comprehensive sentiment and emotional tone analysis

**Parameters**:
- `url` (required): YouTube video URL
- `granularity` (optional): "overall", "section", "detailed"

**Example**:
```
analyze_youtube_sentiment url="https://www.youtube.com/watch?v=example" granularity="detailed"
```

**Output**:
- Overall sentiment scores
- Emotional tone analysis
- Sentiment changes over time
- Confidence metrics

---

### 5. identify_youtube_topics

**Purpose**: Extract main topics and themes

**Parameters**:
- `url` (required): YouTube video URL
- `max_topics` (optional): Maximum topics to identify
- `include_subtopics` (optional): Include detailed subtopics

**Example**:
```
identify_youtube_topics url="https://www.youtube.com/watch?v=example" max_topics="8" include_subtopics="true"
```

**Output**:
- Hierarchical topic structure
- Topic relevance scores
- Related concepts and themes

---

### 6. analyze_youtube_structure

**Purpose**: Analyze video organization and flow

**Parameters**:
- `url` (required): YouTube video URL
- `detail_level` (optional): "basic", "detailed", "comprehensive"

**Example**:
```
analyze_youtube_structure url="https://www.youtube.com/watch?v=example" detail_level="comprehensive"
```

**Output**:
- Content structure breakdown
- Section timing and transitions
- Narrative flow analysis
- Organization assessment

---

### 7. extract_youtube_quotes

**Purpose**: Find memorable quotes and key statements

**Parameters**:
- `url` (required): YouTube video URL
- `max_quotes` (optional): Maximum quotes to extract
- `min_length` (optional): Minimum quote length in words

**Example**:
```
extract_youtube_quotes url="https://www.youtube.com/watch?v=example" max_quotes="10" min_length="15"
```

**Output**:
- Curated list of impactful quotes
- Speaker attribution when available
- Context and timestamp information

---

### 8. analyze_youtube_audience

**Purpose**: Determine target audience and accessibility

**Parameters**:
- `url` (required): YouTube video URL
- `analysis_depth` (optional): "basic", "detailed", "comprehensive"

**Example**:
```
analyze_youtube_audience url="https://www.youtube.com/watch?v=example" analysis_depth="detailed"
```

**Output**:
- Target audience demographics
- Content complexity assessment
- Accessibility evaluation
- Engagement factors

---

### 9. extract_youtube_actionable_items

**Purpose**: Identify concrete actions, steps, and recommendations

**Parameters**:
- `url` (required): YouTube video URL
- `item_type` (optional): "all", "steps", "recommendations", "tasks"

**Example**:
```
extract_youtube_actionable_items url="https://www.youtube.com/watch?v=example" item_type="steps"
```

**Output**:
- Categorized actionable items
- Step-by-step instructions
- Implementation recommendations
- Priority assessments

---

### 10. analyze_youtube_credibility

**Purpose**: Assess content reliability and source credibility

**Parameters**:
- `url` (required): YouTube video URL
- `check_level` (optional): "basic", "thorough", "comprehensive"

**Example**:
```
analyze_youtube_credibility url="https://www.youtube.com/watch?v=example" check_level="thorough"
```

**Output**:
- Credibility assessment scores
- Source verification
- Fact-checking insights
- Reliability indicators

---

### 11. compare_youtube_videos

**Purpose**: Detailed comparison between multiple videos

**Parameters**:
- `urls` (required): Array of 2-5 YouTube URLs
- `comparison_aspects` (optional): Specific aspects to compare

**Example**:
```
compare_youtube_videos urls=["https://www.youtube.com/watch?v=video1", "https://www.youtube.com/watch?v=video2"] comparison_aspects="content quality, presentation style"
```

**Output**:
- Side-by-side comparison matrix
- Similarity and difference analysis
- Strengths and weaknesses
- Recommendation rankings

---

### 12. generate_youtube_discussion_questions

**Purpose**: Create engaging discussion questions based on content

**Parameters**:
- `url` (required): YouTube video URL
- `question_count` (optional): Number of questions to generate
- `difficulty_level` (optional): "basic", "intermediate", "advanced", "mixed"
- `question_types` (optional): Types of questions to include

**Example**:
```
generate_youtube_discussion_questions url="https://www.youtube.com/watch?v=example" question_count="8" difficulty_level="mixed" question_types="analytical, reflective, practical"
```

**Output**:
- Categorized discussion questions
- Difficulty level indicators
- Suggested answer frameworks
- Educational applications

## Common Response Format

All tools return responses with this structure:

```json
{
  "video_metadata": {
    "title": "Video Title",
    "channel": "Channel Name", 
    "duration": "MM:SS",
    "url": "original_url",
    "transcript_length": 1234
  },
  "analysis_results": {
    // Tool-specific analysis data
  },
  "metadata": {
    "analysis_timestamp": "ISO datetime",
    "ai_provider": "anthropic|openai",
    "processing_time": "seconds",
    "confidence_score": 0.95
  }
}
```

## Error Handling

### Common Error Responses

**Invalid URL**:
```json
{
  "error": "Invalid YouTube URL format",
  "code": "INVALID_URL"
}
```

**Transcript Unavailable**:
```json
{
  "error": "Could not extract transcript",
  "code": "TRANSCRIPT_ERROR",
  "attempted_methods": ["youtube_transcript_api", "yt_dlp", "pytube"]
}
```

**API Error**:
```json
{
  "error": "AI API error", 
  "code": "API_ERROR",
  "provider": "anthropic|openai",
  "details": "error details"
}
```

## Usage Patterns

### Sequential Analysis
```
# Start with general analysis
analyze_youtube_video url="..."

# Then get specific insights  
extract_youtube_key_points url="..."
analyze_youtube_sentiment url="..."
```

### Focused Analysis
```
# Target specific aspects
summarize_youtube_video url="..." length="brief"
extract_youtube_actionable_items url="..." item_type="steps"
```

### Comparative Analysis
```
# Compare multiple videos
compare_youtube_videos urls=["...", "..."] comparison_aspects="..."
```

### Educational Use
```
# Generate learning materials
generate_youtube_discussion_questions url="..." difficulty_level="mixed"
extract_youtube_quotes url="..." max_quotes="5"
```

## Rate Limits & Performance

- **API Rate Limits**: Respects provider rate limits
- **Concurrent Requests**: Supports parallel processing
- **Caching**: Transcript caching for repeated analysis
- **Timeout**: 30-second timeout per analysis
- **Retry Logic**: Automatic retry with exponential backoff

## Best Practices

### URL Formats
- Use full YouTube URLs: `https://www.youtube.com/watch?v=VIDEO_ID`
- Short URLs work: `https://youtu.be/VIDEO_ID`
- Playlist URLs: Will analyze first video only

### Parameter Optimization
- Start with default parameters
- Adjust based on content length and complexity
- Use specific parameters for targeted analysis

### Error Recovery
- Check video availability before analysis
- Verify API key configuration
- Monitor quota usage

## Integration Examples

### Python Script
```python
import mcp_client

# Analyze video
result = mcp_client.call_tool(
    "analyze_youtube_video",
    {"url": "https://www.youtube.com/watch?v=example"}
)
```

### Claude Desktop
```
Please analyze this YouTube video for key insights:
https://www.youtube.com/watch?v=example
```

For more integration examples, see [Usage Examples](examples.md).
