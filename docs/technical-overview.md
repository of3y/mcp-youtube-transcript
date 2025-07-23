# Technical Overview

> **Updated for v0.3.0:** Enhanced MCP architecture with Tools, Resources, and Prompts

Deep dive into the architecture and implementation of the YouTube Video Intelligence Suite.

## System Architecture

### High-Level Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Claude Desktop │    │   Enhanced MCP   │    │   YouTube APIs  │
│                 │◄──►│   Server v0.3.0  │◄──►│   Transcript    │
│   Built-in AI   │    │                  │    │   Extraction    │
│   Analysis      │    │  Tools+Resources │    │                 │
└─────────────────┘    │  +Prompts        │    └─────────────────┘
                       └──────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │  Enhanced        │
                       │  Caching &       │
                       │  Analytics       │
                       └──────────────────┘
```

### Component Breakdown

#### 1. Enhanced MCP Server Layer (FastMCP)
- **Purpose**: Complete MCP implementation with tools, resources, and prompts
- **Technology**: FastMCP framework with v0.3.0 enhancements
- **Responsibilities**: 
  - 20 tool registration and discovery
  - 8 resource endpoints for dynamic data access
  - 6 guided workflow prompts
  - Enhanced caching and analytics
  - Advanced error management
  - Full MCP protocol compliance

#### 2. Analysis Engine (Enhanced v0.3.0)
- **Purpose**: Comprehensive video intelligence with caching and tracking
- **Components**:
  - Multi-method transcript extraction pipeline
  - Enhanced caching system with history tracking
  - Resource management for dynamic data access
  - Prompt templates for guided workflows
  - Performance monitoring and analytics

#### 3. Resource Management System (New in v0.3.0)
- **Cached Transcripts**: Dynamic access to processed video data
- **Analytics Engine**: Analysis history and performance metrics
- **Configuration Management**: Server settings and system status
- **Memory Monitoring**: Real-time resource usage tracking

#### 4. YouTube Integration
- **Multiple APIs**: youtube-transcript-api, yt-dlp, pytube
- **Fallback Chain**: Try multiple methods for reliability
- **Metadata Extraction**: Video information and statistics

## Data Flow

### 1. Request Processing

```
User Request → Claude Desktop → MCP Protocol → FastMCP Server → Tool Handler
```

**Request Structure**:
```json
{
  "jsonrpc": "2.0",
  "id": "request-id",
  "method": "tools/call",
  "params": {
    "name": "analyze_youtube_video",
    "arguments": {
      "url": "https://www.youtube.com/watch?v=example",
      "focus_areas": "key insights"
    }
  }
}
```

### 2. Video Processing Pipeline

```
URL Validation → Video Metadata → Transcript Extraction → AI Analysis → Response Formatting
```

**Pipeline Details**:

1. **URL Validation**:
   ```python
   def validate_youtube_url(url: str) -> str:
       patterns = [
           r'youtube\.com/watch\?v=([^&]+)',
           r'youtu\.be/([^?]+)',
           r'youtube\.com/embed/([^?]+)'
       ]
       # Extract video ID using regex patterns
   ```

2. **Metadata Extraction**:
   ```python
   async def get_video_metadata(url: str) -> dict:
       try:
           with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
               info = ydl.extract_info(url, download=False)
               return {
                   'title': info.get('title'),
                   'duration': info.get('duration'),
                   'channel': info.get('uploader'),
                   'view_count': info.get('view_count'),
                   'upload_date': info.get('upload_date')
               }
   ```

3. **Transcript Extraction**:
   ```python
   async def extract_transcript(url: str) -> str:
       video_id = extract_video_id(url)
       
       # Method 1: YouTube Transcript API
       try:
           transcript = YouTubeTranscriptApi.get_transcript(video_id)
           return ' '.join([t['text'] for t in transcript])
       except Exception:
           pass
       
       # Method 2: yt-dlp with auto-captions
       try:
           with yt_dlp.YoutubeDL(subtitle_opts) as ydl:
               info = ydl.extract_info(url, download=False)
               # Extract subtitle text
       except Exception:
           pass
       
       # Method 3: pytube fallback
       # ... implementation
   ```

### 3. AI Analysis Process

```
Transcript → Prompt Engineering → AI API Call → Response Processing → Structured Output
```

**AI Provider Abstraction**:
```python
async def analyze_with_ai(content: str, prompt: str, provider: str = None) -> dict:
    """Unified AI analysis interface."""
    
    if provider == "anthropic" or (not provider and ANTHROPIC_API_KEY):
        return await _analyze_with_anthropic(content, prompt)
    elif provider == "openai" or (not provider and OPENAI_API_KEY):
        return await _analyze_with_openai(content, prompt)
    else:
        raise ValueError("No AI provider available")

async def _analyze_with_anthropic(content: str, prompt: str) -> dict:
    """Anthropic-specific implementation."""
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    
    message = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=4000,
        messages=[{
            "role": "user",
            "content": f"{prompt}\n\nContent to analyze:\n{content}"
        }]
    )
    
    return parse_ai_response(message.content[0].text)

async def _analyze_with_openai(content: str, prompt: str) -> dict:
    """OpenAI-specific implementation."""
    client = openai.AsyncOpenAI(api_key=OPENAI_API_KEY)
    
    response = await client.chat.completions.create(
        model="gpt-4",
        messages=[{
            "role": "user", 
            "content": f"{prompt}\n\nContent to analyze:\n{content}"
        }],
        max_tokens=4000
    )
    
    return parse_ai_response(response.choices[0].message.content)
```

## Tool Implementation

### Tool Registration Pattern

```python
from fastmcp import FastMCP

app = FastMCP("YouTube Video Intelligence Suite")

@app.tool()
async def tool_name(
    url: str,
    optional_param: str = "default"
) -> dict:
    """Tool description for MCP discovery."""
    # Implementation
```

### Analysis Tool Template

Each analysis tool follows this pattern:

```python
@app.tool()
async def analyze_youtube_[aspect](
    url: str,
    analysis_params: str = "default"
) -> dict:
    """
    Analyze specific aspect of YouTube video.
    
    Args:
        url: YouTube video URL
        analysis_params: Tool-specific parameters
        
    Returns:
        Structured analysis results
    """
    try:
        # 1. Extract video data
        transcript = await extract_transcript(url)
        metadata = await get_video_metadata(url)
        
        # 2. Create analysis prompt
        prompt = create_analysis_prompt(aspect, transcript, analysis_params)
        
        # 3. Get AI analysis
        analysis_start = time.time()
        analysis = await analyze_with_ai(transcript, prompt)
        analysis_time = time.time() - analysis_start
        
        # 4. Format response
        return {
            "video_metadata": metadata,
            "analysis_results": analysis,
            "parameters": {"analysis_params": analysis_params},
            "metadata": {
                "analysis_timestamp": datetime.now().isoformat(),
                "processing_time": analysis_time,
                "tool": f"analyze_youtube_{aspect}",
                "ai_provider": get_current_provider()
            }
        }
        
    except Exception as e:
        return create_error_response(e, f"{aspect.upper()}_ANALYSIS_ERROR")
```

## Prompt Engineering

### Prompt Structure

Each tool uses carefully crafted prompts:

```python
def create_analysis_prompt(tool_type: str, transcript: str, params: dict) -> str:
    """Create optimized prompts for each analysis type."""
    
    base_context = f"""
    You are analyzing a YouTube video transcript for {tool_type} analysis.
    
    Video Information:
    - Title: {params.get('title', 'Unknown')}
    - Duration: {params.get('duration', 'Unknown')}
    - Channel: {params.get('channel', 'Unknown')}
    
    Analysis Requirements:
    """
    
    tool_specific_prompts = {
        "summary": """
        Create a comprehensive summary that captures:
        1. Main topic and purpose
        2. Key points and arguments
        3. Supporting evidence and examples
        4. Conclusions and takeaways
        
        Format as structured JSON with clear sections.
        """,
        
        "sentiment": """
        Analyze the emotional tone and sentiment:
        1. Overall sentiment (positive/negative/neutral)
        2. Emotional intensity (scale 1-10)
        3. Sentiment changes throughout video
        4. Key emotional triggers and language patterns
        
        Provide confidence scores for all assessments.
        """,
        
        "topics": """
        Identify main topics and themes:
        1. Primary topics (3-5 main themes)
        2. Secondary topics (supporting themes)
        3. Topic relationships and hierarchy
        4. Keywords and concept clusters
        
        Rank by importance and relevance.
        """
    }
    
    return base_context + tool_specific_prompts.get(tool_type, "")
```

### Prompt Optimization Strategies

1. **Context Setting**: Clear role and task definition
2. **Structured Output**: Request specific JSON formats
3. **Example Guidance**: Include format examples when needed
4. **Constraint Definition**: Set clear boundaries and limitations
5. **Quality Metrics**: Request confidence scores and metadata

## Error Handling Strategy

### Error Hierarchy

```python
class YouTubeIntelligenceError(Exception):
    """Base exception for all suite errors."""
    
    def __init__(self, message: str, code: str = None, context: dict = None):
        self.message = message
        self.code = code or "GENERAL_ERROR"
        self.context = context or {}
        super().__init__(self.message)

class VideoAccessError(YouTubeIntelligenceError):
    """Video cannot be accessed or found."""
    pass

class TranscriptExtractionError(YouTubeIntelligenceError):
    """Transcript extraction failed with all methods."""
    pass

class AIProviderError(YouTubeIntelligenceError):
    """AI provider API error."""
    pass

class AnalysisTimeoutError(YouTubeIntelligenceError):
    """Analysis exceeded timeout limit."""
    pass
```

### Graceful Degradation

```python
async def extract_transcript_with_fallback(url: str) -> str:
    """Extract transcript using multiple methods."""
    methods = [
        ("youtube_transcript_api", extract_with_ytapi),
        ("yt_dlp", extract_with_ytdlp), 
        ("pytube", extract_with_pytube)
    ]
    
    last_error = None
    for method_name, method_func in methods:
        try:
            result = await method_func(url)
            if result:
                logger.info(f"Transcript extracted using {method_name}")
                return result
        except Exception as e:
            logger.warning(f"{method_name} failed: {e}")
            last_error = e
            continue
    
    raise TranscriptExtractionError(
        "All transcript extraction methods failed",
        code="TRANSCRIPT_UNAVAILABLE",
        context={"last_error": str(last_error)}
    )
```

## Performance Optimization

### Async Concurrency

```python
async def analyze_multiple_aspects(transcript: str, metadata: dict) -> dict:
    """Analyze multiple aspects concurrently."""
    
    # Define analysis tasks
    tasks = {
        "summary": create_summary_task(transcript),
        "sentiment": create_sentiment_task(transcript),
        "topics": create_topics_task(transcript),
        "key_points": create_key_points_task(transcript)
    }
    
    # Execute concurrently with timeout
    try:
        results = await asyncio.wait_for(
            asyncio.gather(*tasks.values(), return_exceptions=True),
            timeout=120  # 2 minute timeout
        )
        
        return combine_analysis_results(tasks.keys(), results)
        
    except asyncio.TimeoutError:
        raise AnalysisTimeoutError("Analysis exceeded timeout limit")
```

### Caching Strategy

```python
from functools import lru_cache
import hashlib
import pickle

class TranscriptCache:
    """Simple in-memory transcript cache."""
    
    def __init__(self, max_size: int = 100):
        self.cache = {}
        self.max_size = max_size
        self.access_order = []
    
    def _make_key(self, url: str) -> str:
        return hashlib.md5(url.encode()).hexdigest()
    
    def get(self, url: str) -> str | None:
        key = self._make_key(url)
        if key in self.cache:
            # Update access order
            self.access_order.remove(key)
            self.access_order.append(key)
            return self.cache[key]
        return None
    
    def set(self, url: str, transcript: str) -> None:
        key = self._make_key(url)
        
        # Evict oldest if at capacity
        if len(self.cache) >= self.max_size and key not in self.cache:
            oldest_key = self.access_order.pop(0)
            del self.cache[oldest_key]
        
        self.cache[key] = transcript
        if key in self.access_order:
            self.access_order.remove(key)
        self.access_order.append(key)

# Global cache instance
transcript_cache = TranscriptCache()
```

### Memory Management

```python
def chunk_large_transcript(transcript: str, max_chunk_size: int = 8000) -> List[str]:
    """Split large transcripts into manageable chunks."""
    if len(transcript) <= max_chunk_size:
        return [transcript]
    
    # Split on sentence boundaries when possible
    sentences = transcript.split('. ')
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        if len(current_chunk + sentence) > max_chunk_size:
            if current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = sentence
            else:
                # Single sentence too long, force split
                chunks.append(sentence[:max_chunk_size])
                current_chunk = sentence[max_chunk_size:]
        else:
            current_chunk += sentence + ". "
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks

async def analyze_large_content(transcript: str, prompt: str) -> dict:
    """Handle analysis of large transcripts."""
    if len(transcript) > 10000:  # ~2500 tokens
        chunks = chunk_large_transcript(transcript)
        
        # Analyze chunks separately
        chunk_results = []
        for i, chunk in enumerate(chunks):
            chunk_prompt = f"{prompt}\n\nAnalyzing part {i+1} of {len(chunks)}:\n"
            result = await analyze_with_ai(chunk, chunk_prompt)
            chunk_results.append(result)
        
        # Combine results
        combined_prompt = f"""
        Combine these partial analysis results into a single comprehensive analysis:
        
        {json.dumps(chunk_results, indent=2)}
        
        Original request: {prompt}
        """
        
        return await analyze_with_ai("", combined_prompt)
    else:
        return await analyze_with_ai(transcript, prompt)
```

## Security Considerations

### API Key Management

```python
import os
from typing import Optional

def get_api_key(provider: str) -> Optional[str]:
    """Securely retrieve API keys from environment."""
    key_map = {
        "anthropic": "ANTHROPIC_API_KEY",
        "openai": "OPENAI_API_KEY"
    }
    
    env_var = key_map.get(provider)
    if not env_var:
        return None
    
    key = os.getenv(env_var)
    
    # Validate key format
    if provider == "anthropic" and key and not key.startswith("sk-ant-"):
        logger.warning(f"Invalid {provider} API key format")
        return None
    elif provider == "openai" and key and not key.startswith("sk-"):
        logger.warning(f"Invalid {provider} API key format") 
        return None
    
    return key
```

### Input Validation

```python
import re
from urllib.parse import urlparse

def validate_youtube_url(url: str) -> bool:
    """Validate YouTube URL format and accessibility."""
    try:
        parsed = urlparse(url)
        
        # Check domain
        if parsed.netloc not in ['www.youtube.com', 'youtube.com', 'youtu.be']:
            return False
        
        # Check for video ID
        video_id = extract_video_id(url)
        if not video_id or not re.match(r'^[a-zA-Z0-9_-]{11}$', video_id):
            return False
        
        return True
        
    except Exception:
        return False

def sanitize_input(text: str) -> str:
    """Sanitize user input to prevent injection attacks."""
    # Remove potentially dangerous characters
    sanitized = re.sub(r'[<>"\']', '', text)
    
    # Limit length
    if len(sanitized) > 1000:
        sanitized = sanitized[:1000]
    
    return sanitized.strip()
```

### Rate Limiting

```python
import asyncio
from collections import defaultdict
import time

class RateLimiter:
    """Simple rate limiter for API calls."""
    
    def __init__(self, max_requests: int = 60, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = defaultdict(list)
    
    async def acquire(self, identifier: str = "default") -> bool:
        """Acquire rate limit token."""
        now = time.time()
        
        # Clean old requests
        self.requests[identifier] = [
            req_time for req_time in self.requests[identifier]
            if now - req_time < self.window_seconds
        ]
        
        # Check if under limit
        if len(self.requests[identifier]) < self.max_requests:
            self.requests[identifier].append(now)
            return True
        
        # Calculate wait time
        oldest_request = min(self.requests[identifier])
        wait_time = self.window_seconds - (now - oldest_request)
        
        if wait_time > 0:
            await asyncio.sleep(wait_time)
            return await self.acquire(identifier)
        
        return True

# Global rate limiter
api_rate_limiter = RateLimiter(max_requests=30, window_seconds=60)
```

## Monitoring and Observability

### Logging Strategy

```python
import logging
import json
from datetime import datetime

class StructuredLogger:
    """Structured logging for better observability."""
    
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # JSON formatter
        handler = logging.StreamHandler()
        handler.setFormatter(self._json_formatter)
        self.logger.addHandler(handler)
    
    def _json_formatter(self, record):
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        # Add extra context if present
        if hasattr(record, 'context'):
            log_entry.update(record.context)
        
        return json.dumps(log_entry)
    
    def info(self, message: str, **context):
        self.logger.info(message, extra={'context': context})
    
    def error(self, message: str, **context):
        self.logger.error(message, extra={'context': context})

# Usage
logger = StructuredLogger("youtube_intelligence")

async def analyze_youtube_video(url: str) -> dict:
    logger.info("Starting video analysis", url=url, tool="analyze_youtube_video")
    
    try:
        result = await _perform_analysis(url)
        logger.info("Analysis completed", 
                   url=url, 
                   success=True,
                   processing_time=result.get('metadata', {}).get('processing_time'))
        return result
        
    except Exception as e:
        logger.error("Analysis failed", 
                    url=url, 
                    error=str(e), 
                    error_type=type(e).__name__)
        raise
```

### Metrics Collection

```python
from collections import defaultdict, Counter
import time

class MetricsCollector:
    """Simple metrics collection for monitoring."""
    
    def __init__(self):
        self.counters = Counter()
        self.timers = defaultdict(list)
        self.gauges = {}
    
    def increment(self, metric: str, tags: dict = None):
        """Increment counter metric."""
        key = self._make_key(metric, tags)
        self.counters[key] += 1
    
    def time_operation(self, metric: str, tags: dict = None):
        """Context manager for timing operations."""
        return TimerContext(self, metric, tags)
    
    def set_gauge(self, metric: str, value: float, tags: dict = None):
        """Set gauge value."""
        key = self._make_key(metric, tags)
        self.gauges[key] = value
    
    def _make_key(self, metric: str, tags: dict = None) -> str:
        if not tags:
            return metric
        tag_str = ",".join(f"{k}={v}" for k, v in sorted(tags.items()))
        return f"{metric}[{tag_str}]"
    
    def get_stats(self) -> dict:
        """Get all collected statistics."""
        return {
            "counters": dict(self.counters),
            "timers": {k: {"count": len(v), "avg": sum(v)/len(v), "total": sum(v)} 
                      for k, v in self.timers.items()},
            "gauges": dict(self.gauges)
        }

class TimerContext:
    def __init__(self, collector: MetricsCollector, metric: str, tags: dict):
        self.collector = collector
        self.metric = metric
        self.tags = tags
        self.start_time = None
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = time.time() - self.start_time
        key = self.collector._make_key(self.metric, self.tags)
        self.collector.timers[key].append(duration)

# Global metrics collector
metrics = MetricsCollector()

# Usage in tools
async def analyze_youtube_video(url: str) -> dict:
    metrics.increment("analysis.started", {"tool": "analyze_youtube_video"})
    
    with metrics.time_operation("analysis.duration", {"tool": "analyze_youtube_video"}):
        try:
            result = await _perform_analysis(url)
            metrics.increment("analysis.success", {"tool": "analyze_youtube_video"})
            return result
        except Exception as e:
            metrics.increment("analysis.error", {
                "tool": "analyze_youtube_video",
                "error_type": type(e).__name__
            })
            raise
```

This technical overview provides the foundation for understanding, extending, and maintaining the YouTube Video Intelligence Suite. The modular architecture, robust error handling, and comprehensive observability make it suitable for production use while remaining maintainable and extensible.
