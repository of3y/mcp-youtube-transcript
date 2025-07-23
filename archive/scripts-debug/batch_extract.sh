#!/bin/bash
# Batch process multiple YouTube videos for MCP resources

cd /Users/dkck/Coding/mcp-youtube-transcript

echo "🚀 Batch YouTube Transcript Extraction for MCP Resources"
echo "======================================================="

videos=(
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    "https://www.youtube.com/watch?v=jNQXAC9IVRw"
    "https://www.youtube.com/watch?v=kJQP7kiw5Fk"
)

total=${#videos[@]}
success=0

for i in "${!videos[@]}"; do
    echo ""
    echo "📹 Processing video $((i+1))/$total: ${videos[i]}"
    echo "================================================"
    
    if uv run python scripts/youtube_to_mcp.py "${videos[i]}" --output ./resources/transcripts --method ytdlp; then
        echo "✅ Success"
        ((success++))
    else
        echo "❌ Failed"
    fi
done

echo ""
echo "📊 Batch Summary: $success/$total videos processed successfully"
echo "📁 Resources saved to: ./resources/transcripts/"
echo "🔗 Ready for MCP integration"
