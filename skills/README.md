# YouTube Analysis Claude Skills

A comprehensive suite of **stand-alone Claude Skills** for extracting, analyzing, and learning from YouTube video content. These skills translate the core functionality of the YouTube Transcript MCP server into reusable, independent workflows.

## 🎯 Overview

These skills enable Claude to help you:
- Extract high-quality transcripts from YouTube videos
- Perform deep content analysis
- Create structured study materials
- Plan systematic video research
- Compare multiple videos
- Extract specific content types (quotes, data, references, actions)

**Key Advantage:** Unlike the MCP server, these skills work in any Claude environment that supports bash execution and file operations. No special setup required beyond having `yt-dlp` installed.

## 📚 Available Skills

### 1. 🎬 [youtube-transcript](./youtube-transcript.md)
**Core transcript extraction and quality analysis**

**Use when:** You need to get a transcript from a YouTube video

**Key capabilities:**
- Extract transcripts using yt-dlp with smart format fallback (SRV1 → JSON3 → TTML → VTT)
- Intelligent deduplication and quality analysis
- Provide both plain text and timestamped versions
- Extract comprehensive video metadata
- Quality scoring (0-100) with safety validation

**Example:** "Get me the transcript from https://youtube.com/watch?v=..."

---

### 2. 🔍 [youtube-analysis](./youtube-analysis.md)
**Deep content analysis workshop**

**Use when:** You want comprehensive, structured analysis of video content

**Key capabilities:**
- 4-phase analysis framework (Exploration → Deep Analysis → Critical Evaluation → Actionable Insights)
- Customizable focus areas (educational, business, technical, entertainment, general)
- Systematic evaluation of content quality and credibility
- Extraction of key messages with supporting evidence
- Balanced assessment of strengths and weaknesses

**Example:** "Analyze this educational video about machine learning"

---

### 3. 📝 [study-notes](./study-notes.md)
**Educational content → study materials**

**Use when:** Creating study materials from educational videos

**Key capabilities:**
- 4 note-taking formats (Outline, Cornell Notes, Mind Map, Flashcards)
- Subject-specific guidelines (STEM, Humanities, Business, Languages)
- Comprehensive study aids (glossary, review questions, cross-references)
- Learning objectives identification
- Optimal review schedule suggestions

**Example:** "Create Cornell-style study notes from this biology lecture"

---

### 4. 🔬 [video-research](./video-research.md)
**Systematic research planning**

**Use when:** Planning to learn a topic through multiple YouTube videos

**Key capabilities:**
- 3 research depth levels (Overview 2-3h, Comprehensive 8-12h, Expert 15+h)
- Video selection criteria and quality indicators
- Structured research methodology
- Documentation templates
- Synthesis frameworks for multiple sources

**Example:** "Help me plan a comprehensive research strategy for learning Python"

---

### 5. ⚖️ [video-comparison](./video-comparison.md)
**Systematic multi-video comparison**

**Use when:** Comparing 2+ videos on the same topic

**Key capabilities:**
- 4 comparison frameworks (Content, Style, Accuracy, Audience)
- Side-by-side analysis with scoring
- Identification of agreements, contradictions, and gaps
- Use-case specific recommendations
- Synthesis of best elements from each

**Example:** "Compare these 3 videos about climate change"

---

### 6. 🎯 [content-extraction](./content-extraction.md)
**Extract specific content types**

**Use when:** You need specific information from a video

**Key capabilities:**
- 5 extraction types (Summary, Quotes, Data/Statistics, References, Action Items)
- Structured output formats for each type
- Timestamp preservation
- Context and source documentation
- Multi-type extraction for comprehensive coverage

**Example:** "Extract all the actionable advice from this productivity video"

---

## 🚀 Quick Start Guide

### Installation

**Prerequisites:**
```bash
# Install yt-dlp (required for transcript extraction)
pip install yt-dlp
# or
uv pip install yt-dlp
```

### Using the Skills

Skills are markdown files that provide Claude with specialized knowledge and workflows. To use them:

**Option 1: Direct Reference**
```
You: "Use the youtube-transcript skill to get the transcript from [URL]"
```

**Option 2: Implicit Use**
```
You: "Analyze this YouTube video: [URL]"
Claude: [Automatically uses youtube-transcript + youtube-analysis skills]
```

**Option 3: Skill Chaining**
```
You: "Extract the transcript from [URL], analyze it, and create study notes"
Claude: [Uses youtube-transcript → youtube-analysis → study-notes]
```

### Basic Workflows

**📺 Single Video Analysis**
```
1. Extract transcript (youtube-transcript)
2. Analyze content (youtube-analysis)
3. Create notes if needed (study-notes)
```

**🔬 Research Project**
```
1. Plan research (video-research)
2. Extract transcripts for each video (youtube-transcript)
3. Analyze individually (youtube-analysis)
4. Compare multiple perspectives (video-comparison)
5. Synthesize findings (study-notes)
```

**🎯 Quick Information Extraction**
```
1. Extract transcript (youtube-transcript)
2. Pull specific content (content-extraction)
```

## 📖 Skill Descriptions

### Skill Selection Guide

| Your Goal | Primary Skill | Supporting Skills |
|-----------|--------------|-------------------|
| Get transcript from video | youtube-transcript | - |
| Understand video deeply | youtube-analysis | youtube-transcript |
| Create study materials | study-notes | youtube-transcript, youtube-analysis |
| Learn topic via videos | video-research | All others |
| Choose best video | video-comparison | youtube-transcript, youtube-analysis |
| Find specific info | content-extraction | youtube-transcript |
| Research comprehensively | video-research | All others in sequence |

## 🔄 Skill Workflows

### Workflow 1: Single Video Deep Dive
```mermaid
youtube-transcript → youtube-analysis → study-notes
```
**Best for:** Learning from one high-quality educational video

**Steps:**
1. Extract transcript with quality analysis
2. Perform comprehensive 4-phase analysis
3. Create study notes in preferred format

**Time:** 15-30 minutes per video

---

### Workflow 2: Topic Research
```mermaid
video-research → (youtube-transcript → youtube-analysis) × N → video-comparison → synthesis
```
**Best for:** Systematically learning a new topic

**Steps:**
1. Plan research strategy with video-research skill
2. For each video:
   - Extract transcript
   - Analyze content
   - Take notes
3. Compare all videos
4. Synthesize into comprehensive understanding

**Time:** Varies by research depth level (2-20+ hours)

---

### Workflow 3: Quick Information Gathering
```mermaid
youtube-transcript → content-extraction
```
**Best for:** Finding specific information quickly

**Steps:**
1. Extract transcript
2. Pull specific content type (quotes, data, actions, etc.)

**Time:** 5-10 minutes

---

### Workflow 4: Video Evaluation
```mermaid
youtube-transcript × N → video-comparison → selection
```
**Best for:** Choosing best resource from multiple options

**Steps:**
1. Extract transcripts from all candidates
2. Compare systematically using chosen framework
3. Select best video for your needs

**Time:** 20-40 minutes for 2-4 videos

---

## 💡 Use Cases

### For Students
- **Lecture Note-Taking:** Use study-notes skill for class videos
- **Exam Preparation:** Extract key concepts, create flashcards
- **Research Papers:** Use video-research for literature review
- **Study Groups:** Share extracted transcripts and summaries

### For Professionals
- **Skill Development:** Create learning plans with video-research
- **Conference Talks:** Extract key insights and action items
- **Training Materials:** Convert videos to documentation
- **Knowledge Sharing:** Summarize and share video content

### For Researchers
- **Literature Review:** Systematic analysis of academic videos
- **Source Comparison:** Compare different perspectives
- **Data Extraction:** Pull statistics and research findings
- **Bibliography Building:** Extract all references mentioned

### For Content Creators
- **Competitive Analysis:** Analyze competitor videos
- **Script Research:** Extract effective phrases and structures
- **Idea Generation:** Mine videos for content ideas
- **Quality Benchmarking:** Compare your content with others

## 🎓 Best Practices

### ✅ Do:

**General:**
- Start with youtube-transcript to get the content first
- Use the right skill for your specific goal
- Combine skills for comprehensive analysis
- Save extracted transcripts for future reference

**For Learning:**
- Follow the 4-phase analysis framework completely
- Create active recall materials (flashcards, questions)
- Compare multiple sources on important topics
- Apply knowledge through projects or teaching

**For Research:**
- Plan before diving into videos
- Use systematic comparison frameworks
- Document sources properly
- Synthesize across multiple perspectives

### ❌ Don't:

- Skip transcript quality check before deep analysis
- Use videos as sole source for critical information
- Ignore credibility assessment
- Copy analysis verbatim without understanding
- Rush through analysis phases
- Neglect to cross-reference multiple sources
- Forget to timestamp important moments
- Assume all video content is accurate

## 🔧 Technical Details

### How Transcript Extraction Works

The youtube-transcript skill uses `yt-dlp` to extract subtitles with smart format fallback:

```bash
# Priority order: SRV1 (best) → JSON3 → TTML → VTT (fallback)
yt-dlp --write-subs --sub-lang en --sub-format srv1/json3/ttml/vtt --skip-download "VIDEO_URL"
```

**Format advantages:**
- **SRV1 (XML):** Native YouTube format, highest quality, best timing
- **JSON3:** Detailed timing, millisecond precision
- **TTML:** W3C standard, good structure
- **VTT (WebVTT):** Universal fallback, widely supported

### Quality Analysis Metrics

Transcripts are scored 0-100 based on:

| Metric | Points | Criteria |
|--------|--------|----------|
| Line Count | 0-30 | More lines = more content (optimal: 200+) |
| Avg Line Length | 0-25 | Sweet spot: 20-100 characters |
| Punctuation | 0-20 | Professional captions have good punctuation |
| Timestamps | 0-25 | Percentage of lines with timing data |
| **Penalties** | -20 to -35 | Excessive repetition, gibberish, language issues |

### Deduplication

Smart deduplication removes:
- Exact duplicate consecutive lines
- Substring containment (partial repeats)
- >75% word overlap (aggressive mode)
- Special annotations ([Music], [Applause], etc.)

While preserving:
- Intentional repetition in speech
- Timestamp accuracy
- Line structure integrity

## 🆚 MCP Server vs. Claude Skills

| Aspect | MCP Server | Claude Skills |
|--------|-----------|---------------|
| **Setup** | Requires Claude Desktop + config | Works anywhere Claude has bash access |
| **Dependencies** | uv, mcp library, yt-dlp | Only yt-dlp needed |
| **Caching** | Built-in persistent caching | Manual (save transcripts yourself) |
| **Resources** | Zero-token resource access | Standard tool calls |
| **Portability** | Claude Desktop only | Any Claude environment |
| **Prompts** | Pre-loaded prompt library | Integrated into skill instructions |
| **Tools** | 10 specialized MCP tools | Bash + file operations |
| **Best For** | Regular heavy use in Claude Desktop | Flexible use across environments |

**Bottom Line:**
- Use **MCP Server** if you primarily work in Claude Desktop and want seamless integration with caching
- Use **Claude Skills** if you want portability, simplicity, or use Claude in various environments

## 📊 Skill Comparison Matrix

| Skill | Complexity | Time/Video | Output Type | Requires Prior Skill |
|-------|-----------|------------|-------------|---------------------|
| youtube-transcript | Low | 2-5 min | Raw transcript + metadata | - |
| youtube-analysis | Medium | 15-30 min | Structured analysis report | youtube-transcript |
| study-notes | Medium | 20-40 min | Formatted study materials | youtube-transcript |
| video-research | High | Varies | Research plan + documentation | All others |
| video-comparison | High | 30-60 min | Comparative analysis | youtube-transcript |
| content-extraction | Low | 5-15 min | Extracted content lists | youtube-transcript |

## 🔍 Example Sessions

### Example 1: Learning from a Tutorial

**User:** "I want to learn Python from this video: https://youtube.com/watch?v=..."

**Claude's Process:**
1. Uses `youtube-transcript` to extract transcript
2. Assesses quality (e.g., 87/100 - excellent)
3. Uses `youtube-analysis` with technical focus
4. Uses `study-notes` to create outline format notes
5. Provides comprehensive study materials with:
   - Code examples extracted
   - Key concepts organized hierarchically
   - Practice problems identified
   - Review questions
   - Timestamped references

**Deliverable:** Complete study guide ready for learning

---

### Example 2: Researching a Topic

**User:** "I want to learn about machine learning. Help me plan a comprehensive research strategy."

**Claude's Process:**
1. Uses `video-research` to create research plan
2. Helps identify 12-15 high-quality videos across categories
3. For each video:
   - Extracts transcript
   - Analyzes content
   - Creates notes
   - Documents in research log
4. Uses `video-comparison` for videos covering similar topics
5. Synthesizes findings into master document

**Deliverable:** Complete research documentation with:
- Curated video playlist
- Comprehensive notes
- Comparative analysis
- Unified knowledge map
- Further study recommendations

---

### Example 3: Quick Information Extraction

**User:** "What are the main action items from this productivity video?"

**Claude's Process:**
1. Uses `youtube-transcript` to get content
2. Uses `content-extraction` with action_items type
3. Organizes into immediate/learning/habits/decisions
4. Creates checkable action plan

**Deliverable:** Organized action item list with timestamps, ready to implement

---

## 🛠️ Customization

### Adapting Skills to Your Needs

**For Different Learning Styles:**
- Visual learners: Request mind maps and diagram descriptions
- Verbal learners: Request detailed outline notes
- Kinesthetic learners: Request action items and practice problems

**For Different Time Budgets:**
- Quick (5-10 min): content-extraction only
- Medium (20-30 min): transcript + analysis
- Deep (1-2 hours): Full workflow with study notes

**For Different Purposes:**
- Academic: Emphasize citations, critical analysis, comprehensive notes
- Professional: Emphasize action items, key insights, time efficiency
- Personal: Customize format and depth to preference

### Adding Custom Extraction Types

You can request custom extraction types beyond the standard 5:

- "Extract all code examples"
- "List all tools mentioned"
- "Find all definitions"
- "Pull out all stories and anecdotes"
- "Extract timestamps for topic changes"

## 📝 Contributing

Have ideas for new skills or improvements? Consider:

- New analysis frameworks
- Additional note-taking formats
- Specialized extraction types
- Domain-specific guidelines
- Quality assessment criteria
- Integration workflows

## 🎯 Next Steps

1. **Install yt-dlp**: `pip install yt-dlp`
2. **Try a simple extraction**: Use youtube-transcript with any video
3. **Explore analysis**: Use youtube-analysis on educational content
4. **Plan research**: Use video-research for a topic you want to learn
5. **Create study materials**: Use study-notes for an educational video

## 📚 Resources

**Related Documentation:**
- [Main Project README](../README.md) - MCP Server documentation
- [yt-dlp Documentation](https://github.com/yt-dlp/yt-dlp) - Transcript extraction tool

**Skill Files:**
- [youtube-transcript.md](./youtube-transcript.md)
- [youtube-analysis.md](./youtube-analysis.md)
- [study-notes.md](./study-notes.md)
- [video-research.md](./video-research.md)
- [video-comparison.md](./video-comparison.md)
- [content-extraction.md](./content-extraction.md)

---

## ⚙️ Version

**Skills Version:** 1.0.0
**Based on:** YouTube Transcript MCP Server v0.5.0
**Last Updated:** 2025-01-14

---

## 📄 License

These skills are derived from the MCP YouTube Transcript Server project. See the main repository for license details.

---

## 💬 Feedback

Found these skills useful? Have suggestions for improvements? The skills are designed to evolve based on real-world usage patterns.

**Key Design Principles:**
- ✅ Stand-alone functionality (no MCP required)
- ✅ Clear, structured workflows
- ✅ Comprehensive but not overwhelming
- ✅ Adaptable to different use cases
- ✅ Integration-friendly (skills work together)

---

**Happy Learning! 🎓**
