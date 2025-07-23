"""Resource handlers for YouTube transcript data."""

from typing import Dict, List, Any, Optional
from .config import settings
from datetime import datetime
import sys

# In-memory cache for transcript data
_transcript_cache: Dict[str, Dict[str, Any]] = {}
_video_cache: Dict[str, Dict[str, Any]] = {}
_analysis_history: List[Dict[str, Any]] = []

# Public attributes for external access (expected by tests)
cached_transcripts = _transcript_cache
analysis_history = _analysis_history


def add_to_cache(video_id: str, transcript_data: str, language: str = "en") -> None:
    """Add transcript to cache."""
    global _transcript_cache, _video_cache
    
    _transcript_cache[video_id] = {
        "transcript": transcript_data,
        "language": language,
        "cached_at": datetime.now().isoformat(),
        "length": len(transcript_data.split('\n'))
    }
    
    _video_cache[video_id] = {
        "video_id": video_id,
        "has_transcript": True,
        "language": language,
        "last_accessed": datetime.now().isoformat()
    }


def add_analysis_to_history(analysis_type: str, video_url: str, query: str = None) -> None:
    """Add analysis to history."""
    global _analysis_history
    
    _analysis_history.append({
        "tool": analysis_type,  # Use "tool" key to match test expectations
        "type": analysis_type,  # Keep "type" for backward compatibility
        "video_url": video_url,
        "query": query,
        "timestamp": datetime.now().isoformat()
    })
    
    # Keep only last 100 analyses
    if len(_analysis_history) > 100:
        _analysis_history = _analysis_history[-100:]


async def get_server_config() -> dict:
    """Get server configuration."""
    config = settings.server_info.copy()
    config.update({
        "transcript_features": [
            "transcript_extraction",
            "multi_language_support",
            "content_search",
            "video_analysis",
            "comparison_tools",
            "study_notes_generation",
            "quiz_creation",
            "presentation_analysis"
        ],
        "supported_formats": ["YouTube URLs", "Video IDs"],
        "cache_storage": "in_memory_transcripts",
        "analysis_tools": len(_analysis_history)
    })
    return config


async def get_cached_transcripts() -> dict:
    """Get all cached transcripts information."""
    global _transcript_cache
    
    transcripts = []
    for video_id, data in _transcript_cache.items():
        transcripts.append({
            "video_id": video_id,
            "language": data.get("language", "unknown"),
            "length_lines": data.get("length", 0),
            "cached_at": data.get("cached_at"),
            "size_kb": round(len(data.get("transcript", "")) / 1024, 2)
        })
    
    return {
        "cached_transcripts": transcripts,
        "total_cached": len(transcripts),
        "total_size_kb": round(sum(len(data.get("transcript", "")) for data in _transcript_cache.values()) / 1024, 2)
    }


async def get_video_metadata(video_id: str) -> dict:
    """Get metadata for a specific video."""
    global _video_cache, _transcript_cache
    
    if video_id not in _video_cache:
        return {
            "video_id": video_id,
            "status": "not_cached",
            "has_transcript": False
        }
    
    video_data = _video_cache[video_id]
    transcript_data = _transcript_cache.get(video_id, {})
    
    return {
        "video_id": video_id,
        "status": "cached",
        "has_transcript": video_data.get("has_transcript", False),
        "language": video_data.get("language", "unknown"),
        "last_accessed": video_data.get("last_accessed"),
        "transcript_length": transcript_data.get("length", 0),
        "cached_at": transcript_data.get("cached_at")
    }


async def get_transcript_sample(video_id: str, lines: int = 10) -> dict:
    """Get a sample of transcript lines."""
    global _transcript_cache
    
    if video_id not in _transcript_cache:
        return {
            "video_id": video_id,
            "status": "not_found",
            "sample": []
        }
    
    transcript = _transcript_cache[video_id]["transcript"]
    lines_list = transcript.split('\n')
    
    # Take first N lines, skipping header if present
    start_idx = 0
    for i, line in enumerate(lines_list[:5]):
        if line.startswith('[') and ']' in line:
            start_idx = max(0, i - 1)
            break
    
    sample_lines = lines_list[start_idx:start_idx + lines]
    
    return {
        "video_id": video_id,
        "status": "found",
        "sample": sample_lines,
        "total_lines": len(lines_list),
        "language": _transcript_cache[video_id].get("language", "unknown")
    }


async def get_analysis_history() -> dict:
    """Get recent analysis history."""
    global _analysis_history
    
    # Get last 20 analyses
    recent_analyses = _analysis_history[-20:] if _analysis_history else []
    
    # Count analysis types
    type_counts = {}
    for analysis in _analysis_history:
        analysis_type = analysis.get("type", "unknown")
        type_counts[analysis_type] = type_counts.get(analysis_type, 0) + 1
    
    return {
        "recent_analyses": recent_analyses,
        "total_analyses": len(_analysis_history),
        "analysis_types": type_counts,
        "most_used_type": max(type_counts.items(), key=lambda x: x[1])[0] if type_counts else None
    }


async def get_supported_languages() -> dict:
    """Get information about supported languages."""
    return {
        "primary_languages": ["en", "es", "fr", "de", "it", "pt", "ru", "ja", "ko", "zh"],
        "auto_fallback": True,
        "default_language": settings.default_language,
        "note": "Will attempt requested language, fallback to English, then auto-generated if available"
    }


def get_memory_usage() -> dict:
    """Get memory usage information."""
    global _transcript_cache, _video_cache, _analysis_history
    
    transcript_size = sum(len(str(data)) for data in _transcript_cache.values())
    video_cache_size = sum(len(str(data)) for data in _video_cache.values())
    history_size = sum(len(str(analysis)) for analysis in _analysis_history)
    
    total_size_bytes = transcript_size + video_cache_size + history_size
    
    return {
        "transcript_cache": {
            "entries": len(_transcript_cache),
            "size_kb": round(transcript_size / 1024, 2)
        },
        "video_cache": {
            "entries": len(_video_cache),
            "size_kb": round(video_cache_size / 1024, 2)
        },
        "analysis_history": {
            "entries": len(_analysis_history),
            "size_kb": round(history_size / 1024, 2)
        },
        "total_memory_kb": round(total_size_bytes / 1024, 2),
        "python_memory_mb": round(sys.getsizeof(_transcript_cache) / (1024 * 1024), 2),
        # Additional fields expected by tests
        "cache_size": len(_transcript_cache),
        "history_size": len(_analysis_history),
        "total_transcripts": len(_transcript_cache),
        "total_analyses": len(_analysis_history)
    }


async def get_system_status() -> dict:
    """Get system status information."""
    # Check yt-dlp availability (our primary method)
    try:
        import subprocess
        yt_dlp_result = subprocess.run(['yt-dlp', '--version'], capture_output=True, text=True, timeout=5)
        yt_dlp_available = yt_dlp_result.returncode == 0
        yt_dlp_version = yt_dlp_result.stdout.strip() if yt_dlp_available else None
    except:
        yt_dlp_available = False
        yt_dlp_version = None
    
    return {
        "status": "healthy" if yt_dlp_available else "degraded",
        "timestamp": datetime.now().isoformat(),
        "dependencies": {
            "yt_dlp": "available" if yt_dlp_available else "missing",
            "yt_dlp_version": yt_dlp_version,
            "extraction_method": "yt-dlp (reliable)"
        },
        "cache_status": {
            "transcripts_cached": len(_transcript_cache),
            "videos_tracked": len(_video_cache),
            "analyses_logged": len(_analysis_history)
        },
        "notes": {
            "youtube_transcript_api": "removed due to cloud server blocking issues",
            "primary_method": "yt-dlp for reliable transcript extraction"
        }
    }
