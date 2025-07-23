# Development Guide

> **Updated for v0.2.0:** Simplified development without AI API dependencies

Contributing to and extending the YouTube Video Intelligence Suite.

## Project Overview

The YouTube Video Intelligence Suite is built using:
- **FastMCP**: Modern MCP server framework
- **Python 3.10+**: Core language
- **Claude Desktop**: Direct AI integration (no external APIs)
- **YouTube Libraries**: Multiple transcript extraction methods

## Architecture

```
mcp-youtube-transcript/
├── server.py                    # Main MCP server (FastMCP)
├── pyproject.toml              # Project configuration
├── uv.lock                     # Dependency lock file
├── tests/                      # Test suite
│   └── test_transformation.py  # v0.2.0 transformation tests
├── scripts/                    # Utility scripts
├── examples/                   # Usage examples
└── docs/                       # Documentation
    └── TRANSFORMATION_SUMMARY.md # v0.2.0 changes
```

## Development Setup

### 1. Clone and Setup

```bash
git clone <repository-url>
cd mcp-youtube-transcript

# Install with uv (recommended)
uv sync

# Or with pip
pip install -e .
```

### 2. Development Dependencies

```bash
# Install additional dev dependencies
pip install pytest pytest-asyncio black flake8 mypy
```

### 3. Environment Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit with your API keys
ANTHROPIC_API_KEY=your-key-here
OPENAI_API_KEY=your-key-here
```

## Code Structure

### Core Components

#### server.py Structure
```python
# FastMCP server setup
app = FastMCP("YouTube Video Intelligence Suite")

# Core functions
async def extract_transcript(url: str) -> str
async def analyze_with_ai(content: str, prompt: str) -> dict
async def get_video_metadata(url: str) -> dict

# 12 Analysis tools
@app.tool()
async def analyze_youtube_video(url: str, focus_areas: str = None) -> dict:
    # Implementation

@app.tool() 
async def summarize_youtube_video(url: str, length: str = "medium") -> dict:
    # Implementation

# ... other tools
```

#### Key Design Patterns

**Error Handling**:
```python
try:
    result = await risky_operation()
    return {"success": True, "data": result}
except SpecificError as e:
    return {"error": str(e), "code": "SPECIFIC_ERROR"}
except Exception as e:
    return {"error": str(e), "code": "GENERAL_ERROR"}
```

**AI Provider Abstraction**:
```python
async def analyze_with_ai(content: str, prompt: str, provider: str = None):
    if provider == "anthropic" or (provider is None and ANTHROPIC_API_KEY):
        return await analyze_with_anthropic(content, prompt)
    elif provider == "openai" or (provider is None and OPENAI_API_KEY):
        return await analyze_with_openai(content, prompt)
    else:
        raise ValueError("No AI provider available")
```

**Transcript Extraction with Fallbacks**:
```python
async def extract_transcript(url: str) -> str:
    methods = [
        youtube_transcript_api_method,
        yt_dlp_method,
        pytube_method
    ]
    
    for method in methods:
        try:
            return await method(url)
        except Exception:
            continue
    
    raise TranscriptExtractionError("All methods failed")
```

## Adding New Analysis Tools

### 1. Tool Template

```python
@app.tool()
async def your_new_tool(
    url: str,
    custom_param: str = "default_value"
) -> dict:
    """
    Description of your new analysis tool.
    
    Args:
        url: YouTube video URL
        custom_param: Your custom parameter
        
    Returns:
        Dictionary with analysis results
    """
    try:
        # Extract video data
        transcript = await extract_transcript(url)
        metadata = await get_video_metadata(url)
        
        # Create analysis prompt
        prompt = f"""
        Analyze this YouTube video transcript for [your specific purpose]:
        
        Video: {metadata.get('title', 'Unknown')}
        Custom Parameter: {custom_param}
        
        Transcript:
        {transcript}
        
        Please provide:
        1. [Specific analysis point 1]
        2. [Specific analysis point 2]
        3. [Specific analysis point 3]
        
        Format as structured JSON.
        """
        
        # Get AI analysis
        analysis = await analyze_with_ai(transcript, prompt)
        
        return {
            "video_metadata": metadata,
            "analysis_results": analysis,
            "parameters": {
                "custom_param": custom_param
            },
            "metadata": {
                "analysis_timestamp": datetime.now().isoformat(),
                "tool": "your_new_tool"
            }
        }
        
    except Exception as e:
        return {"error": str(e), "code": "ANALYSIS_ERROR"}
```

### 2. Add Tool Test

Create `tests/test_your_new_tool.py`:

```python
import pytest
from server import your_new_tool

@pytest.mark.asyncio
async def test_your_new_tool():
    """Test the new tool with a sample video."""
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    result = await your_new_tool(url, custom_param="test_value")
    
    assert "error" not in result
    assert "video_metadata" in result
    assert "analysis_results" in result
    assert result["parameters"]["custom_param"] == "test_value"

@pytest.mark.asyncio
async def test_your_new_tool_with_invalid_url():
    """Test error handling with invalid URL."""
    result = await your_new_tool("invalid-url")
    
    assert "error" in result
    assert result["code"] == "ANALYSIS_ERROR"
```

### 3. Update Documentation

Add your tool to:
- `docs/api-reference.md` - Complete API documentation
- `docs/examples.md` - Usage examples
- `README.md` - Tool list

## Testing

### Running Tests

```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest tests/test_server.py

# Run with coverage
python -m pytest --cov=server

# Run integration tests
python -m pytest tests/test_integration.py
```

### Test Categories

**Unit Tests** (`tests/test_units.py`):
```python
@pytest.mark.asyncio
async def test_extract_video_id():
    """Test video ID extraction from various URL formats."""
    assert extract_video_id("https://www.youtube.com/watch?v=ABC123") == "ABC123"
    assert extract_video_id("https://youtu.be/ABC123") == "ABC123"
```

**Integration Tests** (`tests/test_integration.py`):
```python
@pytest.mark.asyncio
async def test_full_analysis_pipeline():
    """Test complete analysis pipeline."""
    url = "https://www.youtube.com/watch?v=test"
    result = await analyze_youtube_video(url)
    
    # Verify complete pipeline works
    assert "video_metadata" in result
    assert "analysis_results" in result
```

**API Tests** (`tests/test_api.py`):
```python
@pytest.mark.asyncio
async def test_anthropic_api():
    """Test Anthropic API integration."""
    result = await analyze_with_anthropic("test content", "summarize this")
    assert isinstance(result, dict)
```

### Mock Testing

For tests without API calls:

```python
from unittest.mock import patch, AsyncMock

@pytest.mark.asyncio
@patch('server.analyze_with_ai')
async def test_analysis_without_api(mock_ai):
    """Test analysis logic without hitting AI APIs."""
    mock_ai.return_value = {"summary": "test summary"}
    
    result = await analyze_youtube_video("test-url")
    assert result["analysis_results"]["summary"] == "test summary"
```

## Code Quality

### Formatting

```bash
# Format code with Black
black server.py tests/

# Check formatting
black --check server.py tests/
```

### Linting

```bash
# Run flake8
flake8 server.py tests/

# Configuration in setup.cfg
[flake8]
max-line-length = 88
extend-ignore = E203, W503
```

### Type Checking

```bash
# Run mypy
mypy server.py

# Type hints example
from typing import Dict, List, Optional, Union

async def analyze_with_ai(
    content: str, 
    prompt: str,
    provider: Optional[str] = None
) -> Dict[str, Union[str, Dict, List]]:
    ...
```

## Performance Optimization

### Async Best Practices

```python
# Good: Concurrent API calls
async def analyze_multiple_aspects(transcript: str):
    tasks = [
        analyze_sentiment(transcript),
        extract_topics(transcript),
        identify_key_points(transcript)
    ]
    results = await asyncio.gather(*tasks)
    return combine_results(results)

# Bad: Sequential API calls
async def analyze_multiple_aspects_slow(transcript: str):
    sentiment = await analyze_sentiment(transcript)
    topics = await extract_topics(transcript)
    points = await identify_key_points(transcript)
    return combine_results([sentiment, topics, points])
```

### Caching Strategy

```python
from functools import lru_cache
import hashlib

# Cache transcripts
transcript_cache = {}

async def extract_transcript(url: str) -> str:
    cache_key = hashlib.md5(url.encode()).hexdigest()
    
    if cache_key in transcript_cache:
        return transcript_cache[cache_key]
    
    transcript = await _extract_transcript_uncached(url)
    transcript_cache[cache_key] = transcript
    return transcript
```

### Memory Management

```python
# Process large transcripts in chunks
def chunk_transcript(transcript: str, chunk_size: int = 1000) -> List[str]:
    words = transcript.split()
    return [
        ' '.join(words[i:i + chunk_size])
        for i in range(0, len(words), chunk_size)
    ]

async def analyze_large_transcript(transcript: str):
    if len(transcript.split()) > 5000:
        chunks = chunk_transcript(transcript)
        results = []
        for chunk in chunks:
            result = await analyze_with_ai(chunk, prompt)
            results.append(result)
        return combine_chunk_results(results)
    else:
        return await analyze_with_ai(transcript, prompt)
```

## Error Handling

### Custom Exceptions

```python
class YouTubeIntelligenceError(Exception):
    """Base exception for YouTube Intelligence Suite."""
    pass

class TranscriptExtractionError(YouTubeIntelligenceError):
    """Raised when transcript extraction fails."""
    pass

class AIAnalysisError(YouTubeIntelligenceError):
    """Raised when AI analysis fails."""
    pass

class InvalidVideoError(YouTubeIntelligenceError):
    """Raised when video URL is invalid or inaccessible."""
    pass
```

### Error Response Format

```python
def create_error_response(error: Exception, code: str) -> dict:
    """Create standardized error response."""
    return {
        "error": str(error),
        "code": code,
        "timestamp": datetime.now().isoformat(),
        "type": type(error).__name__
    }
```

## Documentation

### Code Documentation

```python
async def extract_youtube_key_points(
    url: str, 
    max_points: int = 10
) -> dict:
    """
    Extract key points from a YouTube video.
    
    Uses AI analysis to identify the most important points
    discussed in the video transcript.
    
    Args:
        url: YouTube video URL (any valid format)
        max_points: Maximum number of key points to extract (1-20)
        
    Returns:
        Dict containing:
        - video_metadata: Video information
        - analysis_results: Extracted key points with rankings
        - metadata: Analysis metadata
        
    Raises:
        InvalidVideoError: If URL is invalid or video inaccessible
        TranscriptExtractionError: If transcript cannot be extracted
        AIAnalysisError: If AI analysis fails
        
    Example:
        >>> result = await extract_youtube_key_points(
        ...     "https://www.youtube.com/watch?v=example",
        ...     max_points=5
        ... )
        >>> print(result["analysis_results"]["key_points"])
    """
```

### API Documentation

Update `docs/api-reference.md` for any new tools or changes.

### Examples Documentation

Add examples to `docs/examples.md` showing:
- Basic usage
- Advanced configurations
- Error handling
- Integration patterns

## Deployment

### Production Configuration

```python
# Production settings
PRODUCTION_CONFIG = {
    "max_transcript_length": 50000,
    "api_timeout": 30,
    "retry_attempts": 3,
    "enable_caching": True,
    "log_level": "INFO"
}
```

### Environment Variables

Required environment variables:
```bash
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...

# Optional
YOUTUBE_API_KEY=...  # For enhanced metadata
LOG_LEVEL=INFO
CACHE_TTL=3600
```

### Health Checks

```python
@app.tool()
async def health_check() -> dict:
    """Server health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "apis": {
            "anthropic": bool(ANTHROPIC_API_KEY),
            "openai": bool(OPENAI_API_KEY)
        }
    }
```

## Contributing Guidelines

### Pull Request Process

1. **Fork and Branch**:
```bash
git checkout -b feature/your-feature-name
```

2. **Development**:
   - Write code following existing patterns
   - Add comprehensive tests
   - Update documentation
   - Ensure all tests pass

3. **Commit Messages**:
```bash
git commit -m "feat: add sentiment analysis granularity options

- Add granularity parameter to analyze_youtube_sentiment
- Support overall, section, and detailed analysis levels
- Update tests and documentation
- Closes #123"
```

4. **Testing**:
```bash
# Run full test suite
python -m pytest

# Run linting
black . && flake8 . && mypy server.py

# Test with real videos
python scripts/validate_setup.py
```

5. **Documentation**:
   - Update API reference
   - Add usage examples
   - Update changelog

### Code Review Checklist

- [ ] Code follows existing patterns
- [ ] Comprehensive tests included
- [ ] Documentation updated
- [ ] Error handling implemented
- [ ] Performance considerations addressed
- [ ] Backward compatibility maintained

## Release Process

### Version Management

Update version in:
- `pyproject.toml`
- `server.py` (version constant)
- Documentation references

### Changelog

Maintain `CHANGELOG.md` with:
- **Added**: New features
- **Changed**: Changes in existing functionality
- **Deprecated**: Soon-to-be removed features
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Security improvements

### Release Steps

1. Update version numbers
2. Update changelog
3. Run full test suite
4. Create release tag
5. Update documentation
6. Announce release

## Advanced Features

### Custom AI Providers

```python
class CustomAIProvider:
    """Interface for custom AI providers."""
    
    async def analyze(self, content: str, prompt: str) -> dict:
        """Implement custom analysis logic."""
        pass

# Register custom provider
register_ai_provider("custom", CustomAIProvider())
```

### Plugin System

```python
class AnalysisPlugin:
    """Base class for analysis plugins."""
    
    def __init__(self, name: str):
        self.name = name
    
    async def analyze(self, transcript: str, metadata: dict) -> dict:
        """Implement plugin analysis."""
        pass

# Load plugins
load_plugins_from_directory("plugins/")
```

### Batch Processing

```python
@app.tool()
async def batch_analyze_videos(
    urls: List[str],
    analysis_type: str = "summary"
) -> dict:
    """Analyze multiple videos in batch."""
    tasks = [
        analyze_single_video(url, analysis_type)
        for url in urls
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return format_batch_results(results)
```

Happy coding! 🚀
