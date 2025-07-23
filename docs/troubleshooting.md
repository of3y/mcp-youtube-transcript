# Troubleshooting Guide

Common issues and solutions for the YouTube Video Intelligence Suite.

## Quick Diagnostics

### 1. Run Validation Script

First, run the built-in validation script:

```bash
cd /path/to/your/mcp-youtube-transcript
python scripts/validate_setup.py
```

This will check:
- ✅ Python dependencies
- ✅ API key configuration  
- ✅ MCP server functionality
- ✅ Sample video analysis

### 2. Check Server Status

Test MCP server directly:

```bash
python scripts/test_mcp_server.py
```

## Installation Issues

### Python Dependencies

**Problem**: Missing or incompatible dependencies

**Solution**:
```bash
# Reinstall all dependencies
pip uninstall -y -r <(pip freeze)
pip install -r requirements.txt

# Or use pyproject.toml
pip install -e .
```

**Common Specific Issues**:

```bash
# yt-dlp issues
pip install --upgrade yt-dlp

# YouTube transcript API issues  
pip install --upgrade youtube-transcript-api

# FastMCP issues
pip install --upgrade fastmcp

# Anthropic/OpenAI issues
pip install --upgrade anthropic openai
```

### Python Version Compatibility

**Problem**: Using incompatible Python version

**Requirements**: Python 3.8+

**Check Version**:
```bash
python --version
# Should show Python 3.8.x or higher
```

**Solution**:
```bash
# Install compatible Python version
# macOS with Homebrew:
brew install python@3.11

# Update Claude Desktop config to use correct Python
```

## Configuration Issues

### Claude Desktop Configuration

**Problem**: Server not appearing in Claude Desktop

**Check Configuration File Location**:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

**Common Configuration Errors**:

```json
// ❌ Wrong - Missing quotes around path
{
  "mcpServers": {
    "youtube-intelligence": {
      "command": "python",
      "args": [/path/to/server.py]  // Missing quotes
    }
  }
}

// ✅ Correct
{
  "mcpServers": {
    "youtube-intelligence": {
      "command": "python", 
      "args": ["/path/to/server.py"]
    }
  }
}
```

**Validate JSON Format**:
```bash
# Check JSON syntax
python -m json.tool ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

### Path Issues

**Problem**: "File not found" or "Command not found"

**Find Correct Paths**:
```bash
# Find Python executable
which python
# Example: /usr/bin/python

# Find server.py location
pwd
# From your project directory
```

**Update Configuration**:
```json
{
  "mcpServers": {
    "youtube-intelligence": {
      "command": "/usr/bin/python",  // Full Python path
      "args": ["/full/path/to/mcp-youtube-transcript/server.py"]
    }
  }
}
```

### Permission Issues

**Problem**: Permission denied errors

**Solution**:
```bash
# Make server.py executable
chmod +x server.py

# Check file ownership
ls -la server.py

# Fix permissions if needed
sudo chown $USER:$USER server.py
```

## API Key Issues

### Invalid API Keys

**Problem**: Authentication failed

**Check API Key Format**:
- **Anthropic**: Should start with `sk-ant-`
- **OpenAI**: Should start with `sk-`

**Test API Keys**:
```bash
# Test Anthropic key
python scripts/debug_api.py --provider anthropic

# Test OpenAI key  
python scripts/debug_api.py --provider openai
```

**Common Issues**:
- Expired API keys
- Insufficient API quotas
- Incorrect key format
- Keys in wrong environment

### Environment Variables

**Problem**: API keys not being read

**Check Environment**:
```bash
echo $ANTHROPIC_API_KEY
echo $OPENAI_API_KEY
```

**Set Environment Variables**:
```bash
# Temporary (current session)
export ANTHROPIC_API_KEY="your-key-here"
export OPENAI_API_KEY="your-key-here"

# Permanent (add to ~/.bashrc or ~/.zshrc)
echo 'export ANTHROPIC_API_KEY="your-key-here"' >> ~/.zshrc
```

### API Quota Issues

**Problem**: Rate limiting or quota exceeded

**Symptoms**:
- "Rate limit exceeded" errors
- "Quota exceeded" messages
- Slow response times

**Solutions**:
1. Check your API usage dashboard
2. Upgrade API plan if needed
3. Implement request delays
4. Use both providers for load balancing

## Runtime Issues

### Transcript Extraction Failures

**Problem**: Cannot extract video transcript

**Debug Steps**:
```bash
# Test transcript extraction manually
python -c "
from youtube_transcript_api import YouTubeTranscriptApi
print(YouTubeTranscriptApi.get_transcript('VIDEO_ID'))
"
```

**Common Causes**:
- Video has no transcript/captions
- Video is private/unavailable
- Geographic restrictions
- Age-restricted content

**Solutions**:
- Try different video
- Check video availability
- Use VPN if geographic restrictions
- Enable auto-generated captions

### Memory Issues

**Problem**: Out of memory errors with long videos

**Symptoms**:
- Process killed
- Memory errors
- Slow performance

**Solutions**:
```bash
# Check available memory
free -h

# Process smaller chunks
# Use length parameter in analysis
```

**Configuration Options**:
```python
# In server.py, you can adjust:
MAX_TRANSCRIPT_LENGTH = 50000  # Reduce if needed
CHUNK_SIZE = 1000             # Process in smaller chunks
```

### Network Issues

**Problem**: Connection timeouts or failures

**Check Connection**:
```bash
# Test internet connectivity
curl -I https://www.youtube.com/
curl -I https://api.anthropic.com/
curl -I https://api.openai.com/
```

**Solutions**:
- Check firewall settings
- Try different network
- Configure proxy if needed
- Increase timeout values

## Video-Specific Issues

### Unsupported Video Types

**Problem**: Cannot analyze certain videos

**Unsupported Content**:
- Live streams (while live)
- Private videos
- Deleted videos
- Age-restricted (sometimes)
- Videos without captions

**Check Video Status**:
```python
import yt_dlp

ydl = yt_dlp.YoutubeDL({'quiet': True})
try:
    info = ydl.extract_info('VIDEO_URL', download=False)
    print(f"Title: {info['title']}")
    print(f"Available: {info.get('availability', 'unknown')}")
except Exception as e:
    print(f"Error: {e}")
```

### Large Video Analysis

**Problem**: Timeouts with very long videos

**Solutions**:
1. Use summary tools first
2. Analyze in sections
3. Focus on specific aspects
4. Increase timeout settings

## Performance Issues

### Slow Analysis

**Problem**: Analysis takes too long

**Optimization**:
1. Use appropriate analysis depth
2. Limit focus areas
3. Choose efficient AI provider
4. Cache transcripts

**Monitor Performance**:
```bash
# Run with timing
time python scripts/test_mcp_server.py
```

### High API Costs

**Problem**: Unexpected high API usage

**Cost Management**:
1. Use shorter analysis lengths
2. Cache results when possible
3. Choose appropriate AI models
4. Monitor usage dashboards

## Claude Desktop Integration

### Server Not Showing

**Problem**: YouTube Intelligence tools not available in Claude

**Checklist**:
1. ✅ Restart Claude Desktop after config changes
2. ✅ Check config file syntax
3. ✅ Verify file paths
4. ✅ Confirm API keys set
5. ✅ Test server independently

**Debug Steps**:
```bash
# 1. Test server directly
python server.py

# 2. Check Claude Desktop logs (if available)
# 3. Verify config syntax
python -m json.tool claude_desktop_config.json
```

### Partial Functionality

**Problem**: Some tools work, others don't

**Common Causes**:
- API key issues for specific provider
- Quota limits reached
- Network restrictions
- Tool-specific bugs

**Debugging**:
```bash
# Test specific tools
python scripts/test_mcp_protocol.py --tool analyze_youtube_video
python scripts/test_mcp_protocol.py --tool summarize_youtube_video
```

## Debugging Tools

### Enable Debug Logging

Add to server.py:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Test Individual Components

```bash
# Test transcript extraction
python -c "from server import extract_transcript; print(extract_transcript('VIDEO_URL'))"

# Test AI analysis  
python -c "from server import analyze_with_ai; print(analyze_with_ai('test content', 'summarize this'))"

# Test full pipeline
python scripts/debug_api.py --url "VIDEO_URL" --tool "analyze_youtube_video"
```

### Common Debug Commands

```bash
# Check Python path
which python

# Check installed packages
pip list | grep -E "(anthropic|openai|youtube|fastmcp)"

# Check file permissions
ls -la server.py

# Test network connectivity
ping google.com
curl -I https://www.youtube.com/

# Check process status
ps aux | grep python
```

## Getting Help

### Log Collection

When reporting issues, include:

```bash
# System info
python --version
pip list

# Error logs
python server.py 2>&1 | tee error.log

# Configuration (remove API keys!)
cat claude_desktop_config.json | sed 's/"sk-[^"]*"/"REDACTED"/g'
```

### Common Error Patterns

**"Module not found"**:
- Check Python path
- Reinstall dependencies
- Verify virtual environment

**"Permission denied"**:
- Check file permissions
- Run with appropriate user
- Check directory access

**"API Error"**:
- Verify API keys
- Check quota limits
- Test network connectivity

**"Transcript not available"**:
- Check video accessibility
- Try different video
- Verify transcript exists

### Support Resources

1. **Documentation**: Check all docs in `/docs` folder
2. **Validation Script**: `python scripts/validate_setup.py`
3. **Debug Script**: `python scripts/debug_api.py`
4. **Test Suite**: `python -m pytest tests/`

### Emergency Recovery

If nothing works:

```bash
# Complete reinstall
rm -rf venv/
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Reset configuration
cp claude_desktop_config.json claude_desktop_config.json.backup
# Recreate config from scratch using configuration.md guide
```

Remember: Most issues are configuration-related. Double-check paths, API keys, and JSON syntax first!
