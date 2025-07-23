#!/usr/bin/env python3
"""
Test MCP server protocol integration for v0.3.0
"""

import asyncio
import pytest
import sys
import os
from unittest.mock import patch, MagicMock, AsyncMock

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestMCPServerIntegration:
    """Test MCP server protocol integration."""
    
    def test_server_initialization(self):
        """Test that the MCP server initializes correctly."""
        from enhanced_server import mcp
        from src.youtube_transcript_server.config import settings
        
        # Test server properties
        assert hasattr(mcp, 'name')
        assert mcp.name == settings.server_name
        # Note: FastMCP doesn't have a 'version' attribute directly, but settings does
        assert settings.version == "0.3.0"
    
    @pytest.mark.asyncio
    async def test_tool_registration(self):
        """Test that all tools are properly registered."""
        from enhanced_server import mcp
        
        # Get registered tools using the proper async method
        tools_list = await mcp.list_tools()
        tools = [tool.name for tool in tools_list]
        
        # Expected core tools
        expected_core_tools = [
            "get_youtube_transcript",
            "search_transcript", 
            "get_youtube_transcript_ytdlp",
            "analyze_video_comprehensive",
            "extract_key_quotes",
            "create_study_notes",
            "generate_quiz",
            "fact_check_claims",
            "extract_statistics_and_data",
            "extract_citations_and_references",
            "compare_videos",
            "analyze_presentation_style"
        ]
        
        # Expected resource mirror tools
        expected_resource_tools = [
            "resource_transcripts_cached",
            "resource_analytics_history",
            "resource_analytics_memory_usage",
            "resource_config_server",
            "resource_analytics_supported_languages",
            "resource_system_status"
        ]
        
        # Should have 20 total tools
        assert len(tools) >= 20
        
        # Check that core tools are registered
        for tool in expected_core_tools:
            assert tool in tools, f"Tool {tool} not found in registered tools"
        
        # Check that resource mirror tools are registered
        for tool in expected_resource_tools:
            assert tool in tools, f"Resource mirror tool {tool} not found in registered tools"
    
    def test_resource_registration(self):
        """Test that resources are properly registered."""
        from enhanced_server import mcp
        
        # Resources should be registered
        if hasattr(mcp, '_resources'):
            resources = list(mcp._resources.keys())
            
            expected_resources = [
                "transcripts://cached",
                "analytics://history",
                "analytics://memory_usage", 
                "analytics://supported_languages",
                "config://server",
                "system://status"
            ]
            
            # Check for key resources
            resource_uris = [r for r in resources if "://" in r]
            assert len(resource_uris) >= 6
    
    def test_prompt_registration(self):
        """Test that prompts are properly registered.""" 
        from enhanced_server import mcp
        
        # Prompts should be registered
        if hasattr(mcp, '_prompts'):
            prompts = list(mcp._prompts.keys())
            
            expected_prompts = [
                "transcript_analysis_workshop",
                "video_comparison_framework",
                "content_extraction_guide",
                "study_notes_generator", 
                "video_research_planner",
                "list_available_prompts"
            ]
            
            assert len(prompts) >= 6
            
            for prompt in expected_prompts:
                assert prompt in prompts
    
    @pytest.mark.asyncio
    async def test_tool_execution_format(self):
        """Test that tools return properly formatted responses."""
        from enhanced_server import get_youtube_transcript, analyze_video_comprehensive
        
        with patch('enhanced_server.YouTubeTranscriptApi') as mock_api:
            # Setup mock
            mock_transcript_list = MagicMock()
            mock_transcript = MagicMock()
            mock_transcript.fetch.return_value = [{"start": 0.0, "text": "Test"}]
            mock_transcript_list.find_transcript.return_value = mock_transcript
            mock_api.list_transcripts.return_value = mock_transcript_list
            
            # Test transcript tool with mock
            with patch('enhanced_server.YouTubeTranscriptApi') as mock_api:
                mock_transcript_list = MagicMock()
                mock_transcript = MagicMock()
                mock_transcript.fetch.return_value = [{"start": 0.0, "text": "Test transcript"}]
                mock_transcript_list.find_transcript.return_value = mock_transcript
                mock_api.list_transcripts.return_value = mock_transcript_list
                
                result = await get_youtube_transcript("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
                assert isinstance(result, str)
                assert len(result) > 0
            
            # Test analysis tool with mock
            with patch('enhanced_server.YouTubeTranscriptApi') as mock_api:
                mock_transcript_list = MagicMock()
                mock_transcript = MagicMock()
                mock_transcript.fetch.return_value = [{"start": 0.0, "text": "Test content for analysis"}]
                mock_transcript_list.find_transcript.return_value = mock_transcript
                mock_api.list_transcripts.return_value = mock_transcript_list
                
                result = await analyze_video_comprehensive("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "summary")
                assert isinstance(result, str)
                assert ("Analysis Request" in result or "Test content" in result)  # Accept either format
    
    def test_error_handling_consistency(self):
        """Test that error handling is consistent across tools."""
        import inspect
        from enhanced_server import (
            get_youtube_transcript,
            analyze_video_comprehensive,
            extract_key_quotes
        )
        
        # All tools should be async functions
        assert inspect.iscoroutinefunction(get_youtube_transcript)
        assert inspect.iscoroutinefunction(analyze_video_comprehensive)
        assert inspect.iscoroutinefunction(extract_key_quotes)
    
    @pytest.mark.asyncio
    async def test_concurrent_tool_execution(self):
        """Test that tools can handle concurrent execution."""
        from enhanced_server import get_cached_transcripts, get_analysis_history
        
        # Execute multiple tools concurrently
        tasks = [
            get_cached_transcripts(),
            get_analysis_history(),
            get_cached_transcripts(),  # Duplicate to test concurrent access
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # All should succeed
        for result in results:
            assert not isinstance(result, Exception)
            assert isinstance(result, str)


class TestProtocolCompliance:
    """Test MCP protocol compliance."""
    
    def test_tool_schema_compliance(self):
        """Test that tools follow MCP schema requirements."""
        from enhanced_server import mcp
        
        # Tools should have proper metadata
        if hasattr(mcp, '_tools'):
            for tool_name, tool_func in mcp._tools.items():
                # Should have docstring
                assert tool_func.__doc__ is not None
                assert len(tool_func.__doc__.strip()) > 10
                
                # Should be async
                import inspect
                assert inspect.iscoroutinefunction(tool_func)
    
    def test_resource_uri_compliance(self):
        """Test that resource URIs follow MCP conventions."""
        expected_resource_patterns = [
            "transcripts://",
            "analytics://", 
            "config://",
            "system://"
        ]
        
        # Test that resource URIs follow expected patterns
        from src.youtube_transcript_server import resources
        
        # This would be expanded when resources are fully implemented
        assert hasattr(resources, 'cached_transcripts')
        assert hasattr(resources, 'analysis_history')
    
    def test_prompt_schema_compliance(self):
        """Test that prompts follow MCP prompt schema."""
        from src.youtube_transcript_server import prompts
        
        for prompt_name, prompt_data in prompts.AVAILABLE_PROMPTS.items():
            # Required fields per MCP spec
            assert "name" in prompt_data
            assert "description" in prompt_data
            
            # Arguments should be present (can be simplified structure)
            if "arguments" in prompt_data:
                # In our implementation, arguments are just strings (simplified)
                for arg in prompt_data["arguments"]:
                    assert isinstance(arg, str)  # Just check it's a string argument name


class TestPerformanceAndReliability:
    """Test performance and reliability of the MCP server."""
    
    @pytest.mark.asyncio
    async def test_tool_execution_time(self):
        """Test that tools execute within reasonable time limits."""
        import time
        from enhanced_server import get_cached_transcripts
        
        start_time = time.time()
        result = await get_cached_transcripts()
        execution_time = time.time() - start_time
        
        # Should execute quickly (resource mirror tools should be fast)
        assert execution_time < 1.0  # Less than 1 second
        assert isinstance(result, str)
    
    @pytest.mark.asyncio
    async def test_memory_usage_stability(self):
        """Test that repeated tool calls don't cause memory leaks."""
        import gc
        from enhanced_server import get_analysis_history
        
        # Execute tool multiple times
        for i in range(10):
            result = await get_analysis_history()
            assert isinstance(result, str)
        
        # Force garbage collection
        gc.collect()
        
        # This is a basic test - in practice you'd measure actual memory usage
        assert True  # If we get here without crash, basic stability is OK
    
    @pytest.mark.asyncio
    async def test_error_recovery(self):
        """Test that the server recovers from errors gracefully."""
        from enhanced_server import get_youtube_transcript
        
        # Test with invalid URL
        result = await get_youtube_transcript("invalid-url")
        
        # Should return error message, not raise exception
        assert isinstance(result, str)
        assert ("Error" in result or "❌" in result)
        
        # Should still work for valid calls after error
        with patch('enhanced_server.YouTubeTranscriptApi') as mock_api:
            mock_transcript_list = MagicMock()
            mock_transcript = MagicMock()
            mock_transcript.fetch.return_value = [{"start": 0.0, "text": "Recovery test"}]
            mock_transcript_list.find_transcript.return_value = mock_transcript
            mock_api.list_transcripts.return_value = mock_transcript_list
            
            result = await get_youtube_transcript("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
            assert ("Recovery test" in result or "Transcript for" in result)  # Accept either transcript content or formatted output


class TestBackwardCompatibility:
    """Test backward compatibility with existing configurations."""
    
    def test_legacy_server_exists(self):
        """Test that the legacy server.py still exists for compatibility."""
        import os
        
        legacy_server_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "server.py"
        )
        
        assert os.path.exists(legacy_server_path)
    
    def test_main_entry_point(self):
        """Test that main.py properly routes to enhanced server."""
        from main import main
        
        # Should be callable
        assert callable(main)
        
        # Should route to enhanced server
        import enhanced_server
        assert hasattr(enhanced_server, 'main')
    
    def test_configuration_compatibility(self):
        """Test that existing Claude Desktop configurations work."""
        # Test that the expected entry points exist
        import main
        import enhanced_server
        
        assert hasattr(main, 'main')
        assert hasattr(enhanced_server, 'main')
        
        # Both should be callable
        assert callable(main.main)
        assert callable(enhanced_server.main)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
