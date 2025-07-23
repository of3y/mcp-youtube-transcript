# Enhanced Server Simplification Instructions

## 🎯 Objective
Apply the same youtube-transcript-api removal and yt-dlp simplification that was successfully completed in `scripts/youtube_to_mcp.py` to the `enhanced_server.py` MCP server.

## 📋 Context Summary
We successfully simplified the standalone script by:
1. Removing `youtube-transcript-api` dependency (causes cloud server blocking)
2. Using only `yt-dlp` for transcript extraction
3. Eliminating method selection complexity
4. Maintaining all transcript processing and quality features

## 🔍 Current enhanced_server.py Structure
- **File size**: ~1,835 lines
- **Architecture**: FastMCP server with 25+ tools, 13 resources, 6 prompts
- **Problem**: Still uses `youtube-transcript-api` in multiple functions
- **Target**: Convert to yt-dlp-only approach like the standalone script

## 📖 Reference Implementation
The **perfect pattern** is in `scripts/youtube_to_mcp.py`:
- See the `extract_transcript()` function (formerly `extract_transcript_ytdlp()`)
- See the VTT parsing logic starting around line 230
- See the deduplication function `deduplicate_transcript_lines()`

## 🎯 Step-by-Step Instructions

### Phase 0: Git operations
- Check git status and commit changes if present, design commit message by analyzing changes
- Create new git dev/further_simplification branch where we develop

### Phase 1: Remove youtube-transcript-api Imports
**Location**: Top of `enhanced_server.py` (around lines 20-21)

**Current code:**
```python
from youtube_transcript_api._api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
```

**Action**: Replace with:
```python
# Note: Simplified to use only yt-dlp for reliable transcript extraction
# youtube-transcript-api removed due to cloud server blocking issues
```

### Phase 2: Identify Functions Using youtube-transcript-api
**Search for these patterns** in enhanced_server.py:
- `YouTubeTranscriptApi.list_transcripts`
- `YouTubeTranscriptApi.get_transcript`
- `NoTranscriptFound`
- `TranscriptsDisabled`

**Expected locations** (approximate):
- Line ~199: `transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)`
- Line ~256: `transcript_data = YouTubeTranscriptApi.get_transcript(video_id, languages=[language, 'en'])`
- Line ~287: `except (TranscriptsDisabled, NoTranscriptFound) as e:`
- Line ~309: `transcript_list = YouTubeTranscriptApi.get_transcript(video_id)`

### Phase 3: Replace Core Extraction Logic
**Primary function to modify**: The main transcript extraction function in enhanced_server.py

**Pattern to follow**: Copy the exact VTT parsing logic from `scripts/youtube_to_mcp.py` lines ~230-320:

```python
def extract_transcript_ytdlp(video_url: str, language: str = "en") -> Dict[str, Any]:
    # Use the EXACT implementation from youtube_to_mcp.py
    # This includes:
    # 1. yt-dlp command execution
    # 2. VTT file parsing
    # 3. Timestamp extraction and formatting
    # 4. Deduplication call
```

**Key components to copy**:
1. **yt-dlp command setup** (lines ~245-265 in youtube_to_mcp.py)
2. **VTT parsing logic** (lines ~280-320 in youtube_to_mcp.py)  
3. **Deduplication function** (entire `deduplicate_transcript_lines()` function)

### Phase 4: Update Function Signatures
**Change pattern**:
- Remove `language` parameter complexity from API-based functions
- Standardize on the yt-dlp approach signature
- Ensure return format matches existing MCP tool expectations

### Phase 5: Error Handling Updates
**Replace youtube-transcript-api errors** with yt-dlp specific errors:

**Old pattern**:
```python
except (TranscriptsDisabled, NoTranscriptFound) as e:
```

**New pattern**:
```python
except subprocess.TimeoutExpired:
    return {"error": "yt-dlp timed out"}
except Exception as e:
    return {"error": f"yt-dlp extraction failed: {str(e)}"}
```

### Phase 6: Preserve MCP Architecture
**Critical**: Maintain all existing:
- **Tool definitions** and signatures
- **Resource endpoints**
- **Prompt structures**
- **Return formats** expected by MCP clients

**Only change**: The internal transcript extraction method, not the MCP interface.

## 🔧 Implementation Strategy

### Option A: Function-by-Function (Recommended)
1. Start with the main extraction function
2. Test with a simple MCP tool call
3. Move to next function using youtube-transcript-api
4. Validate each change maintains MCP compatibility

### Option B: Copy-Replace Pattern
1. Copy entire `extract_transcript()` function from youtube_to_mcp.py
2. Adapt the function name/signature to match enhanced_server.py needs
3. Replace all youtube-transcript-api calls with calls to this new function

## 🧪 Testing Instructions
After each modification:

```bash
# Test MCP server still starts
uv run python main.py

# Test basic transcript extraction (in another terminal)
# Use MCP client or Claude Desktop to test get_youtube_transcript tool
```

## ⚠️ Critical Preservation Points

### Must Maintain:
1. **All MCP tool names** and signatures
2. **Resource URI patterns** (transcripts://, analytics://)
3. **Prompt names** and structures
4. **Return data formats** (same JSON structure)
5. **Error message patterns** that MCP clients expect

### Can Change:
1. **Internal extraction method** (youtube-transcript-api → yt-dlp)
2. **Import statements**
3. **Internal error handling** (as long as external format stays same)
4. **Internal function names** (as long as MCP tools still work)

## 📁 Files to Reference
- `scripts/youtube_to_mcp.py` - **Perfect implementation pattern**
- `SIMPLIFICATION_SUMMARY.md` - Context on what was changed and why
- `enhanced_server.py` - Target file to modify

## 🎯 Success Criteria
- [ ] MCP server starts without import errors
- [ ] All existing MCP tools still function
- [ ] Transcript extraction works reliably (no cloud blocking)
- [ ] Same quality output as simplified standalone script
- [ ] All resources and prompts remain functional

## 🚫 What NOT to Do
- Don't change MCP tool names or signatures
- Don't modify resource URI patterns
- Don't alter the FastMCP server setup
- Don't change existing prompt structures
- Don't remove any existing MCP functionality

## 💡 Pro Tips
1. **Use grep** to find all youtube-transcript-api usage: `grep -n "YouTubeTranscriptApi\|NoTranscriptFound\|TranscriptsDisabled" enhanced_server.py`
2. **Test incrementally** - don't change everything at once
3. **Keep the VTT parsing identical** to youtube_to_mcp.py for consistency
4. **Preserve all existing comments** that explain MCP-specific logic
5. **Use git for maintenance** purposes and merge to main after successful implementation
6. **Make sure to always use `uv run ...`** when executing any python script

---
*Instructions created with perfect context from the successful youtube_to_mcp.py simplification - follow this pattern exactly for enhanced_server.py*
