# Testing Strategy

Comprehensive testing approach for the YouTube Video Intelligence Suite ensuring reliability, performance, and maintainability.

## Testing Philosophy

Our testing strategy follows these principles:

1. **Comprehensive Coverage**: Unit, integration, and end-to-end tests
2. **Reliability First**: Robust error handling and edge case coverage
3. **Performance Validation**: Timing and resource usage testing
4. **Real-World Scenarios**: Testing with actual YouTube content
5. **Continuous Validation**: Automated testing in CI/CD pipeline

## Test Structure

```
tests/
├── unit/                     # Unit tests for individual components
│   ├── test_transcript_extraction.py
│   ├── test_ai_analysis.py
│   ├── test_video_metadata.py
│   └── test_utilities.py
├── integration/              # Integration tests for combined components
│   ├── test_full_pipeline.py
│   ├── test_ai_providers.py
│   └── test_mcp_protocol.py
├── end_to_end/              # Complete workflow tests
│   ├── test_all_tools.py
│   └── test_claude_desktop.py
├── performance/             # Performance and load tests
│   ├── test_performance.py
│   └── test_concurrent_analysis.py
├── fixtures/                # Test data and mocks
│   ├── sample_transcripts.py
│   ├── mock_responses.py
│   └── test_videos.py
└── conftest.py              # Pytest configuration and fixtures
```

## Test Categories

### 1. Unit Tests

Test individual components in isolation.

#### Transcript Extraction Tests

```python
# tests/unit/test_transcript_extraction.py
import pytest
from unittest.mock import patch, MagicMock
from server import extract_transcript, extract_video_id, TranscriptExtractionError

class TestTranscriptExtraction:
    
    def test_extract_video_id_from_standard_url(self):
        """Test video ID extraction from standard YouTube URL."""
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        video_id = extract_video_id(url)
        assert video_id == "dQw4w9WgXcQ"
    
    def test_extract_video_id_from_short_url(self):
        """Test video ID extraction from short YouTube URL."""
        url = "https://youtu.be/dQw4w9WgXcQ"
        video_id = extract_video_id(url)
        assert video_id == "dQw4w9WgXcQ"
    
    def test_extract_video_id_with_additional_params(self):
        """Test video ID extraction with URL parameters."""
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=30s&list=playlist"
        video_id = extract_video_id(url)
        assert video_id == "dQw4w9WgXcQ"
    
    def test_extract_video_id_invalid_url(self):
        """Test error handling for invalid URLs."""
        with pytest.raises(ValueError):
            extract_video_id("https://not-youtube.com/video")
    
    @pytest.mark.asyncio
    @patch('server.YouTubeTranscriptApi.get_transcript')
    async def test_extract_transcript_success_first_method(self, mock_transcript):
        """Test successful transcript extraction with first method."""
        mock_transcript.return_value = [
            {'text': 'Hello', 'start': 0.0},
            {'text': 'World', 'start': 1.0}
        ]
        
        url = "https://www.youtube.com/watch?v=test"
        transcript = await extract_transcript(url)
        
        assert transcript == "Hello World"
        mock_transcript.assert_called_once()
    
    @pytest.mark.asyncio
    @patch('server.YouTubeTranscriptApi.get_transcript')
    @patch('server.extract_with_ytdlp')
    async def test_extract_transcript_fallback_to_second_method(self, mock_ytdlp, mock_transcript):
        """Test fallback to second extraction method."""
        mock_transcript.side_effect = Exception("API failed")
        mock_ytdlp.return_value = "Fallback transcript"
        
        url = "https://www.youtube.com/watch?v=test"
        transcript = await extract_transcript(url)
        
        assert transcript == "Fallback transcript"
        mock_transcript.assert_called_once()
        mock_ytdlp.assert_called_once()
    
    @pytest.mark.asyncio
    @patch('server.YouTubeTranscriptApi.get_transcript')
    @patch('server.extract_with_ytdlp')
    @patch('server.extract_with_pytube')
    async def test_extract_transcript_all_methods_fail(self, mock_pytube, mock_ytdlp, mock_transcript):
        """Test error when all extraction methods fail."""
        mock_transcript.side_effect = Exception("API failed")
        mock_ytdlp.side_effect = Exception("ytdlp failed")
        mock_pytube.side_effect = Exception("pytube failed")
        
        url = "https://www.youtube.com/watch?v=test"
        
        with pytest.raises(TranscriptExtractionError):
            await extract_transcript(url)
```

#### AI Analysis Tests

```python
# tests/unit/test_ai_analysis.py
import pytest
from unittest.mock import patch, AsyncMock
from server import analyze_with_ai, AIProviderError

class TestAIAnalysis:
    
    @pytest.mark.asyncio
    @patch('server.ANTHROPIC_API_KEY', 'test-key')
    @patch('server.anthropic.Anthropic')
    async def test_analyze_with_anthropic(self, mock_anthropic_client):
        """Test AI analysis with Anthropic provider."""
        mock_client = AsyncMock()
        mock_anthropic_client.return_value = mock_client
        mock_client.messages.create.return_value.content = [
            MagicMock(text='{"summary": "Test summary"}')
        ]
        
        result = await analyze_with_ai("test content", "summarize this", "anthropic")
        
        assert result == {"summary": "Test summary"}
        mock_client.messages.create.assert_called_once()
    
    @pytest.mark.asyncio
    @patch('server.OPENAI_API_KEY', 'test-key')
    @patch('server.openai.AsyncOpenAI')
    async def test_analyze_with_openai(self, mock_openai_client):
        """Test AI analysis with OpenAI provider."""
        mock_client = AsyncMock()
        mock_openai_client.return_value = mock_client
        mock_response = AsyncMock()
        mock_response.choices = [
            MagicMock(message=MagicMock(content='{"summary": "Test summary"}'))
        ]
        mock_client.chat.completions.create.return_value = mock_response
        
        result = await analyze_with_ai("test content", "summarize this", "openai")
        
        assert result == {"summary": "Test summary"}
        mock_client.chat.completions.create.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_analyze_with_ai_no_provider_available(self):
        """Test error when no AI provider is available."""
        with patch('server.ANTHROPIC_API_KEY', None), \
             patch('server.OPENAI_API_KEY', None):
            
            with pytest.raises(AIProviderError):
                await analyze_with_ai("content", "prompt")
    
    @pytest.mark.asyncio
    @patch('server.ANTHROPIC_API_KEY', 'test-key')
    @patch('server.anthropic.Anthropic')
    async def test_analyze_with_ai_api_error(self, mock_anthropic_client):
        """Test handling of AI provider API errors."""
        mock_client = AsyncMock()
        mock_anthropic_client.return_value = mock_client
        mock_client.messages.create.side_effect = Exception("API Error")
        
        with pytest.raises(AIProviderError):
            await analyze_with_ai("content", "prompt", "anthropic")
```

### 2. Integration Tests

Test component interactions and data flow.

#### Full Pipeline Tests

```python
# tests/integration/test_full_pipeline.py
import pytest
from server import analyze_youtube_video, summarize_youtube_video

class TestFullPipeline:
    
    @pytest.mark.asyncio
    @pytest.mark.slow
    async def test_analyze_youtube_video_complete_flow(self):
        """Test complete video analysis pipeline."""
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Rick Roll - always available
        
        result = await analyze_youtube_video(url)
        
        # Verify response structure
        assert "video_metadata" in result
        assert "analysis_results" in result
        assert "metadata" in result
        
        # Verify metadata content
        metadata = result["video_metadata"]
        assert metadata["title"]
        assert metadata["channel"]
        assert metadata["duration"]
        
        # Verify analysis content
        analysis = result["analysis_results"]
        assert isinstance(analysis, dict)
        assert len(str(analysis)) > 100  # Substantial analysis
        
        # Verify processing metadata
        proc_metadata = result["metadata"]
        assert "analysis_timestamp" in proc_metadata
        assert "processing_time" in proc_metadata
        assert proc_metadata["processing_time"] > 0
    
    @pytest.mark.asyncio
    async def test_multiple_tools_same_video(self):
        """Test multiple analysis tools on the same video."""
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        
        # Run multiple analyses
        summary_result = await summarize_youtube_video(url, length="brief")
        analysis_result = await analyze_youtube_video(url)
        
        # Both should succeed
        assert "error" not in summary_result
        assert "error" not in analysis_result
        
        # Should have consistent metadata
        assert summary_result["video_metadata"]["title"] == analysis_result["video_metadata"]["title"]
    
    @pytest.mark.asyncio
    async def test_error_handling_invalid_video(self):
        """Test error handling for invalid video URL."""
        url = "https://www.youtube.com/watch?v=INVALID_VIDEO_ID"
        
        result = await analyze_youtube_video(url)
        
        assert "error" in result
        assert result["code"] in ["TRANSCRIPT_ERROR", "VIDEO_NOT_FOUND"]
```

#### AI Provider Integration Tests

```python
# tests/integration/test_ai_providers.py
import pytest
import os
from server import analyze_with_ai

class TestAIProviderIntegration:
    
    @pytest.mark.skipif(not os.getenv('ANTHROPIC_API_KEY'), reason="No Anthropic API key")
    @pytest.mark.asyncio
    async def test_anthropic_real_api(self):
        """Test actual Anthropic API integration."""
        content = "This is a test video about machine learning and artificial intelligence."
        prompt = "Summarize the main topics discussed in this content."
        
        result = await analyze_with_ai(content, prompt, "anthropic")
        
        assert isinstance(result, dict)
        assert len(str(result)) > 50
    
    @pytest.mark.skipif(not os.getenv('OPENAI_API_KEY'), reason="No OpenAI API key")
    @pytest.mark.asyncio
    async def test_openai_real_api(self):
        """Test actual OpenAI API integration."""
        content = "This is a test video about machine learning and artificial intelligence."
        prompt = "Summarize the main topics discussed in this content."
        
        result = await analyze_with_ai(content, prompt, "openai")
        
        assert isinstance(result, dict)
        assert len(str(result)) > 50
    
    @pytest.mark.asyncio
    async def test_provider_fallback_logic(self):
        """Test automatic fallback between providers."""
        content = "Test content for analysis"
        prompt = "Analyze this content"
        
        # Should work with either provider available
        result = await analyze_with_ai(content, prompt)
        
        assert isinstance(result, dict)
```

### 3. End-to-End Tests

Test complete user workflows.

#### All Tools Test

```python
# tests/end_to_end/test_all_tools.py
import pytest
from server import (
    analyze_youtube_video, summarize_youtube_video, extract_youtube_key_points,
    analyze_youtube_sentiment, identify_youtube_topics, analyze_youtube_structure,
    extract_youtube_quotes, analyze_youtube_audience, extract_youtube_actionable_items,
    analyze_youtube_credibility, compare_youtube_videos, generate_youtube_discussion_questions
)

class TestAllTools:
    
    @pytest.fixture
    def test_video_url(self):
        """Reliable test video URL."""
        return "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    @pytest.mark.asyncio
    @pytest.mark.slow
    async def test_all_single_video_tools(self, test_video_url):
        """Test all tools that work with a single video."""
        tools = [
            analyze_youtube_video,
            summarize_youtube_video,
            extract_youtube_key_points,
            analyze_youtube_sentiment,
            identify_youtube_topics,
            analyze_youtube_structure,
            extract_youtube_quotes,
            analyze_youtube_audience,
            extract_youtube_actionable_items,
            analyze_youtube_credibility,
            generate_youtube_discussion_questions
        ]
        
        results = {}
        for tool in tools:
            try:
                result = await tool(test_video_url)
                results[tool.__name__] = result
                
                # Basic validation
                assert "error" not in result, f"{tool.__name__} returned error: {result.get('error')}"
                assert "video_metadata" in result
                assert "analysis_results" in result
                
            except Exception as e:
                pytest.fail(f"{tool.__name__} failed: {str(e)}")
        
        # Verify all tools completed successfully
        assert len(results) == len(tools)
        
        # Verify consistent metadata across tools
        titles = [r["video_metadata"]["title"] for r in results.values()]
        assert len(set(titles)) == 1, "Inconsistent video metadata across tools"
    
    @pytest.mark.asyncio
    async def test_compare_videos_tool(self):
        """Test video comparison tool with multiple videos."""
        urls = [
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "https://www.youtube.com/watch?v=9bZkp7q19f0"  # Another popular video
        ]
        
        result = await compare_youtube_videos(urls)
        
        assert "error" not in result
        assert "analysis_results" in result
        assert "videos" in result["analysis_results"]
        assert len(result["analysis_results"]["videos"]) == 2
```

### 4. Performance Tests

Validate system performance and resource usage.

#### Performance Benchmarks

```python
# tests/performance/test_performance.py
import pytest
import time
import asyncio
from server import analyze_youtube_video, extract_transcript

class TestPerformance:
    
    @pytest.mark.asyncio
    async def test_analysis_performance_benchmark(self):
        """Benchmark analysis performance."""
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        
        start_time = time.time()
        result = await analyze_youtube_video(url)
        end_time = time.time()
        
        processing_time = end_time - start_time
        
        # Should complete within reasonable time (adjust based on requirements)
        assert processing_time < 60, f"Analysis took {processing_time:.2f}s, expected < 60s"
        assert "error" not in result
    
    @pytest.mark.asyncio
    async def test_concurrent_analysis_performance(self):
        """Test performance with concurrent requests."""
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        
        # Run 3 concurrent analyses
        start_time = time.time()
        tasks = [analyze_youtube_video(url) for _ in range(3)]
        results = await asyncio.gather(*tasks)
        end_time = time.time()
        
        total_time = end_time - start_time
        
        # Concurrent should be faster than sequential
        assert total_time < 120, f"Concurrent analysis took {total_time:.2f}s"
        
        # All should succeed
        for result in results:
            assert "error" not in result
    
    @pytest.mark.asyncio
    async def test_transcript_caching_performance(self):
        """Test transcript caching improves performance."""
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        
        # First extraction (cache miss)
        start_time = time.time()
        transcript1 = await extract_transcript(url)
        first_time = time.time() - start_time
        
        # Second extraction (cache hit)
        start_time = time.time()
        transcript2 = await extract_transcript(url)
        second_time = time.time() - start_time
        
        # Cached version should be faster and identical
        assert transcript1 == transcript2
        assert second_time < first_time * 0.5, "Caching didn't improve performance significantly"
```

#### Memory Usage Tests

```python
# tests/performance/test_memory.py
import pytest
import psutil
import os
from server import analyze_youtube_video

class TestMemoryUsage:
    
    def get_memory_usage(self):
        """Get current memory usage in MB."""
        process = psutil.Process(os.getpid())
        return process.memory_info().rss / 1024 / 1024
    
    @pytest.mark.asyncio
    async def test_memory_usage_single_analysis(self):
        """Test memory usage for single video analysis."""
        initial_memory = self.get_memory_usage()
        
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        result = await analyze_youtube_video(url)
        
        final_memory = self.get_memory_usage()
        memory_increase = final_memory - initial_memory
        
        # Should not use excessive memory (adjust threshold as needed)
        assert memory_increase < 100, f"Memory usage increased by {memory_increase:.2f}MB"
        assert "error" not in result
    
    @pytest.mark.asyncio
    async def test_memory_leak_multiple_analyses(self):
        """Test for memory leaks with multiple analyses."""
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        
        initial_memory = self.get_memory_usage()
        
        # Run multiple analyses
        for i in range(5):
            result = await analyze_youtube_video(url)
            assert "error" not in result
        
        final_memory = self.get_memory_usage()
        memory_increase = final_memory - initial_memory
        
        # Memory should not grow linearly with number of analyses
        assert memory_increase < 200, f"Potential memory leak: {memory_increase:.2f}MB increase"
```

## Test Configuration

### Pytest Configuration

```python
# conftest.py
import pytest
import os
import asyncio
from unittest.mock import patch

def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "slow: marks tests as slow")
    config.addinivalue_line("markers", "integration: marks tests as integration tests")
    config.addinivalue_line("markers", "e2e: marks tests as end-to-end tests")

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def mock_api_keys():
    """Mock API keys for testing."""
    with patch.dict(os.environ, {
        'ANTHROPIC_API_KEY': 'test-anthropic-key',
        'OPENAI_API_KEY': 'test-openai-key'
    }):
        yield

@pytest.fixture
def sample_transcript():
    """Sample transcript for testing."""
    return """
    Hello everyone, welcome to this video about artificial intelligence and machine learning.
    Today we'll be discussing the fundamentals of neural networks and how they work.
    First, let's start with the basics of what a neural network actually is.
    A neural network is a computational model inspired by biological neural networks.
    These networks consist of interconnected nodes or neurons that process information.
    The key advantage of neural networks is their ability to learn patterns from data.
    This makes them particularly useful for tasks like image recognition and natural language processing.
    Thank you for watching, and I hope you found this introduction helpful.
    """

@pytest.fixture
def sample_video_metadata():
    """Sample video metadata for testing."""
    return {
        "title": "Introduction to Neural Networks",
        "channel": "AI Education Channel",
        "duration": "10:30",
        "view_count": 150000,
        "upload_date": "2024-01-15"
    }
```

### Test Data Management

```python
# tests/fixtures/test_videos.py
"""Test video fixtures and data."""

TEST_VIDEOS = {
    "short_educational": {
        "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "expected_duration_range": (180, 240),  # 3-4 minutes
        "expected_topics": ["music", "entertainment"],
        "has_transcript": True
    },
    "long_lecture": {
        "url": "https://www.youtube.com/watch?v=EXAMPLE_LONG",
        "expected_duration_range": (3600, 7200),  # 1-2 hours
        "expected_topics": ["education", "lecture"],
        "has_transcript": True
    },
    "no_transcript": {
        "url": "https://www.youtube.com/watch?v=EXAMPLE_NO_TRANSCRIPT",
        "expected_duration_range": (60, 300),
        "has_transcript": False
    }
}

SAMPLE_TRANSCRIPTS = {
    "technical": """
    In this video, we'll explore the concept of machine learning algorithms.
    We'll start with supervised learning, where we have labeled training data.
    Then we'll move on to unsupervised learning and clustering techniques.
    Finally, we'll discuss reinforcement learning and its applications.
    """,
    
    "conversational": """
    Hey everyone! Welcome back to my channel. Today I'm super excited to share
    with you my morning routine. I wake up at 6 AM every day and start with
    meditation. Then I have a healthy breakfast and review my goals for the day.
    """,
    
    "educational": """
    The human brain contains approximately 86 billion neurons. Each neuron
    connects to thousands of other neurons, forming a complex network.
    This biological neural network inspired the development of artificial
    neural networks in computer science.
    """
}
```

## Test Automation

### GitHub Actions Configuration

```yaml
# .github/workflows/test.yml
name: Test Suite

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, "3.10", 3.11]

    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v3
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-asyncio pytest-cov
    
    - name: Run unit tests
      run: |
        pytest tests/unit/ -v --cov=server --cov-report=xml
    
    - name: Run integration tests
      env:
        ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
      run: |
        pytest tests/integration/ -v -m "not slow"
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml

  e2e-tests:
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v3
      with:
        python-version: 3.9
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-asyncio
    
    - name: Run end-to-end tests
      env:
        ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
      run: |
        pytest tests/end_to_end/ -v --tb=short
```

### Local Test Commands

```bash
# Run all tests
pytest

# Run specific test categories
pytest tests/unit/                    # Unit tests only
pytest tests/integration/             # Integration tests only
pytest tests/end_to_end/             # E2E tests only

# Run tests with coverage
pytest --cov=server --cov-report=html

# Run performance tests
pytest tests/performance/ -v

# Run tests excluding slow ones
pytest -m "not slow"

# Run specific test file
pytest tests/unit/test_transcript_extraction.py -v

# Run with verbose output and stop on first failure
pytest -v -x

# Run tests in parallel (install pytest-xdist)
pytest -n auto
```

## Quality Assurance

### Coverage Requirements

- **Minimum Coverage**: 85% overall
- **Critical Paths**: 95% coverage for core analysis functions
- **Error Handling**: 90% coverage for exception paths

### Performance Benchmarks

- **Single Analysis**: < 60 seconds
- **Concurrent Analysis**: < 2 minutes for 3 concurrent requests
- **Memory Usage**: < 100MB increase per analysis
- **API Response**: < 30 seconds for AI provider calls

### Test Maintenance

1. **Regular Updates**: Update test videos monthly
2. **API Changes**: Update mocks when APIs change
3. **Performance Review**: Review benchmarks quarterly
4. **Documentation**: Keep test documentation current

This comprehensive testing strategy ensures the YouTube Video Intelligence Suite maintains high quality, reliability, and performance across all components and use cases.
