"""
Test the Prompts system for v0.3.0
"""

import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.youtube_transcript_server import prompts


class TestPromptsSystem:
    """Test the prompts module functionality."""
    
    def test_available_prompts_structure(self):
        """Test that all prompts have the required structure."""
        assert hasattr(prompts, 'AVAILABLE_PROMPTS')
        assert isinstance(prompts.AVAILABLE_PROMPTS, dict)
        assert len(prompts.AVAILABLE_PROMPTS) >= 6  # Expected number of prompts
        
        required_prompts = [
            "transcript_analysis_workshop",
            "video_comparison_framework", 
            "content_extraction_guide",
            "study_notes_generator",
            "video_research_planner",
            "list_available_prompts"
        ]
        
        for prompt_name in required_prompts:
            assert prompt_name in prompts.AVAILABLE_PROMPTS
    
    def test_prompt_data_structure(self):
        """Test that each prompt has the correct data structure."""
        for prompt_name, prompt_data in prompts.AVAILABLE_PROMPTS.items():
            # Test required fields
            assert "name" in prompt_data
            assert "description" in prompt_data
            assert "arguments" in prompt_data
            assert "returns" in prompt_data
            
            # Test field types
            assert isinstance(prompt_data["name"], str)
            assert isinstance(prompt_data["description"], str)
            assert isinstance(prompt_data["arguments"], list)
            assert isinstance(prompt_data["returns"], str)
            
            # Name should match the key
            assert prompt_data["name"] == prompt_name
    
    def test_transcript_analysis_workshop_prompt(self):
        """Test the transcript analysis workshop prompt."""
        prompt = prompts.AVAILABLE_PROMPTS["transcript_analysis_workshop"]
        
        assert prompt["name"] == "transcript_analysis_workshop"
        assert "analysis" in prompt["description"].lower()
        
        # Check arguments - simplified structure (just strings)
        assert "video_url" in prompt["arguments"]
        assert "focus_area" in prompt["arguments"]
    
    def test_video_comparison_framework_prompt(self):
        """Test the video comparison framework prompt."""
        prompt = prompts.AVAILABLE_PROMPTS["video_comparison_framework"]
        
        assert prompt["name"] == "video_comparison_framework"
        assert "comparison" in prompt["description"].lower()
        
        # Check arguments
        assert "video_urls" in prompt["arguments"]
        assert "comparison_focus" in prompt["arguments"]
    
    def test_content_extraction_guide_prompt(self):
        """Test the content extraction guide prompt."""
        prompt = prompts.AVAILABLE_PROMPTS["content_extraction_guide"]
        
        assert prompt["name"] == "content_extraction_guide"
        assert "extract" in prompt["description"].lower()
        
        # Check arguments
        assert "video_url" in prompt["arguments"]
        assert "extraction_type" in prompt["arguments"]
    
    def test_study_notes_generator_prompt(self):
        """Test the study notes generator prompt."""
        prompt = prompts.AVAILABLE_PROMPTS["study_notes_generator"]
        
        assert prompt["name"] == "study_notes_generator"
        assert "study" in prompt["description"].lower()
        
        # Check arguments
        assert "video_url" in prompt["arguments"]
        assert "subject_area" in prompt["arguments"]
    
    def test_video_research_planner_prompt(self):
        """Test the video research planner prompt."""
        prompt = prompts.AVAILABLE_PROMPTS["video_research_planner"]
        
        assert prompt["name"] == "video_research_planner"
        assert "research" in prompt["description"].lower()
        
        # Check arguments
        assert "video_url" in prompt["arguments"]
        assert "research_objectives" in prompt["arguments"]
    
    def test_list_available_prompts_prompt(self):
        """Test the list available prompts prompt."""
        prompt = prompts.AVAILABLE_PROMPTS["list_available_prompts"]
        
        assert prompt["name"] == "list_available_prompts"
        assert "list" in prompt["description"].lower()


class TestPromptArguments:
    """Test prompt argument validation and processing."""
    
    def test_argument_types(self):
        """Test that arguments are consistently typed."""
        for prompt_data in prompts.AVAILABLE_PROMPTS.values():
            assert isinstance(prompt_data["arguments"], list)
            for arg in prompt_data["arguments"]:
                assert isinstance(arg, str)  # Arguments are stored as simple strings
    
    def test_common_arguments_consistency(self):
        """Test that common arguments are consistently named."""
        common_arg_names = {}
        
        for prompt_data in prompts.AVAILABLE_PROMPTS.values():
            for arg_name in prompt_data["arguments"]:
                if arg_name in common_arg_names:
                    # Should be consistent (same string)
                    assert arg_name == common_arg_names[arg_name]
                else:
                    common_arg_names[arg_name] = arg_name
        
        # Common arguments should exist
        assert "video_url" in common_arg_names
        assert "video_urls" in common_arg_names


class TestPromptUsability:
    """Test prompt usability and user experience."""
    
    def test_prompt_descriptions_clarity(self):
        """Test that prompt descriptions are clear and helpful."""
        for prompt_name, prompt_data in prompts.AVAILABLE_PROMPTS.items():
            description = prompt_data["description"]
            
            # Should explain what the prompt does
            action_words = ["analyze", "compare", "extract", "generate", "create", "list", "plan"]
            assert any(word in description.lower() for word in action_words)
            
            # Should be written in a user-friendly way
            assert not description.startswith("This prompt")  # Avoid meta descriptions
    
    def test_argument_helpfulness(self):
        """Test that arguments are self-explanatory."""
        for prompt_data in prompts.AVAILABLE_PROMPTS.values():
            for arg_name in prompt_data["arguments"]:
                # Argument names should be descriptive
                assert len(arg_name) > 3  # Not too short
                assert "_" in arg_name or arg_name.islower()  # Follow naming convention
    
    def test_required_vs_optional_structure(self):
        """Test that prompts have logical argument structure."""
        for prompt_name, prompt_data in prompts.AVAILABLE_PROMPTS.items():
            arguments = prompt_data["arguments"]
            
            if prompt_name != "list_available_prompts":
                # Most prompts should have at least one argument
                assert len(arguments) > 0
                
                # video_url or video_urls should typically be present
                video_args = [arg for arg in arguments if "video" in arg]
                assert len(video_args) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
