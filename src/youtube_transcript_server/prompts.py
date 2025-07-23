"""Prompt templates for YouTube transcript analysis workflows."""

from typing import Optional

# Available prompts list for external access (expected by tests)
AVAILABLE_PROMPTS = {
    "transcript_analysis_workshop": {
        "name": "transcript_analysis_workshop",
        "description": "Interactive workshop to analyze comprehensive transcript analysis",
        "arguments": ["video_url", "focus_area"],
        "returns": "str"
    },
    "video_comparison_framework": {
        "name": "video_comparison_framework", 
        "description": "Compare multiple videos with systematic comparison framework",
        "arguments": ["video_urls", "comparison_focus"],
        "returns": "str"
    },
    "content_extraction_guide": {
        "name": "content_extraction_guide",
        "description": "Extract specific types of content from videos",
        "arguments": ["video_url", "extraction_type"],
        "returns": "str"
    },
    "study_notes_generator": {
        "name": "study_notes_generator",
        "description": "Create structured study materials from educational content",
        "arguments": ["video_url", "subject_area", "note_style"],
        "returns": "str"
    },
    "video_research_planner": {
        "name": "video_research_planner",
        "description": "Plan comprehensive research using YouTube videos",
        "arguments": ["video_url", "research_objectives"],
        "returns": "str"
    },
    "list_available_prompts": {
        "name": "list_available_prompts",
        "description": "List all available prompts and their use cases",
        "arguments": [],
        "returns": "str"
    }
}


async def transcript_analysis_workshop(video_url: str, focus_area: str = "general") -> str:
    """Interactive workshop prompt for comprehensive transcript analysis.
    
    Args:
        video_url: YouTube video URL to analyze
        focus_area: Area of focus (general, educational, business, technical, entertainment)
    """
    
    focus_guidance = {
        "educational": "learning objectives, teaching methods, clarity of explanations, educational value",
        "business": "key insights, actionable advice, market trends, strategic recommendations", 
        "technical": "technical accuracy, implementation details, code examples, best practices",
        "entertainment": "storytelling techniques, audience engagement, entertainment value, content structure",
        "general": "main themes, key insights, content quality, presentation effectiveness"
    }
    
    guidance = focus_guidance.get(focus_area, focus_guidance["general"])
    
    return f"""# 📺 Transcript Analysis Workshop

## Video Analysis Session
**Video:** {video_url}
**Focus Area:** {focus_area.title()}

## Analysis Framework

Let's conduct a comprehensive analysis focusing on: {guidance}

### Phase 1: Initial Exploration
1. **Content Overview**: What is the main topic and purpose of this video?
2. **Structure Analysis**: How is the content organized? (intro, main points, conclusion)
3. **Target Audience**: Who is this video intended for?

### Phase 2: Deep Analysis  
4. **Key Messages**: What are the 3-5 most important points made?
5. **Supporting Evidence**: What examples, data, or stories support the main points?
6. **Quality Assessment**: How well does the content achieve its purpose?

### Phase 3: Critical Evaluation
7. **Strengths**: What does this video do particularly well?
8. **Weaknesses**: What could be improved or is missing?
9. **Credibility**: How trustworthy and authoritative is the information?

### Phase 4: Actionable Insights
10. **Key Takeaways**: What should viewers remember or act on?
11. **Follow-up Questions**: What questions does this raise for further exploration?
12. **Application**: How can this information be practically applied?

---
**Instructions for AI:** Please extract the transcript using the get_youtube_transcript tool, then work through this analysis framework systematically. Provide specific examples and quotes from the transcript to support your analysis."""


async def video_comparison_framework(video_urls: list, comparison_focus: str = "content") -> str:
    """Framework for comparing multiple videos systematically.
    
    Args:
        video_urls: List of YouTube video URLs to compare
        comparison_focus: What aspect to focus on (content, style, accuracy, audience)
    """
    
    if len(video_urls) < 2:
        return "❌ Please provide at least 2 video URLs for comparison"
    
    videos_list = "\n".join([f"- Video {i+1}: {url}" for i, url in enumerate(video_urls)])
    
    focus_frameworks = {
        "content": """
### Content Comparison Framework
1. **Topic Coverage**: What aspects of the topic does each video cover?
2. **Depth vs Breadth**: Which video goes deeper vs covers more ground?
3. **Accuracy**: How accurate and up-to-date is the information in each?
4. **Evidence Quality**: What types of evidence/examples does each use?
5. **Completeness**: Which video provides a more complete picture?""",
        
        "style": """
### Style & Presentation Framework  
1. **Communication Style**: Formal vs casual, academic vs practical
2. **Pacing**: Fast-paced vs detailed, rushed vs thorough
3. **Engagement**: How does each presenter keep viewers engaged?
4. **Visual Aids**: Use of graphics, examples, demonstrations
5. **Accessibility**: How easy is it for different audiences to follow?""",
        
        "accuracy": """
### Accuracy & Credibility Framework
1. **Source Quality**: What sources and references are cited?
2. **Expertise**: What credentials/experience do the presenters have?
3. **Fact-checking**: Can claims be verified? Are sources reliable?
4. **Bias Detection**: What potential biases might influence the content?
5. **Currency**: How recent and relevant is the information?""",
        
        "audience": """
### Audience & Purpose Framework
1. **Target Audience**: Who is each video intended for?
2. **Skill Level**: Beginner, intermediate, or advanced?
3. **Purpose**: Education, entertainment, persuasion, information?
4. **Effectiveness**: How well does each achieve its purpose?
5. **Recommendation**: Which video would you recommend for different audiences?"""
    }
    
    framework = focus_frameworks.get(comparison_focus, focus_frameworks["content"])
    
    return f"""# ⚖️ Video Comparison Workshop

## Comparison Session Setup
**Focus:** {comparison_focus.title()} Analysis
**Videos to Compare:**
{videos_list}

## Comparison Framework
{framework}

### Systematic Analysis Process

**Step 1:** Extract transcripts for all videos using the get_youtube_transcript tool

**Step 2:** For each video, provide:
- Brief summary (2-3 sentences)
- Key strengths
- Notable weaknesses  
- Target audience assessment

**Step 3:** Direct Comparison
- Create a side-by-side analysis using the framework above
- Identify specific examples from transcripts
- Note direct contradictions or agreements

**Step 4:** Final Recommendations
- Which video is best for different use cases?
- What would an ideal video combining the best elements look like?
- Are there gaps that none of the videos address?

---
**Instructions for AI:** Work through this systematically, using specific quotes and examples from the transcripts to support your comparisons."""


async def content_extraction_guide(video_url: str, extraction_type: str = "summary") -> str:
    """Guide for extracting specific types of content from video transcripts.
    
    Args:
        video_url: YouTube video URL
        extraction_type: Type of content to extract (summary, quotes, data, references, action_items)
    """
    
    extraction_guides = {
        "summary": """
### Summary Extraction Guide
**Goal:** Create a comprehensive yet concise summary

**Structure:**
1. **Main Topic** (1 sentence)
2. **Key Points** (3-5 bullet points)
3. **Supporting Details** (examples, evidence, explanations)
4. **Conclusion/Takeaway** (1-2 sentences)

**Quality Criteria:**
- Captures the essence without losing important details
- Logical flow and organization  
- Neutral tone and accurate representation""",
        
        "quotes": """
### Quote Extraction Guide
**Goal:** Identify the most impactful and memorable quotes

**Types to Look For:**
1. **Key Insights** - Novel ideas or important realizations
2. **Memorable Phrases** - Catchy or profound statements
3. **Practical Advice** - Actionable recommendations
4. **Supporting Evidence** - Statistics, research findings
5. **Personal Stories** - Anecdotes that illustrate points

**Format:** Include timestamp and context for each quote""",
        
        "data": """
### Data & Statistics Extraction Guide
**Goal:** Identify all quantitative information and data points

**Categories:**
1. **Statistics** - Percentages, ratios, counts
2. **Research Findings** - Study results, survey data
3. **Financial Data** - Costs, revenues, market sizes
4. **Dates & Timelines** - Historical data, projections
5. **Measurements** - Performance metrics, comparisons

**Include:** Source attribution when mentioned""",
        
        "references": """
### References & Sources Guide
**Goal:** Catalog all mentioned sources and further reading

**Types to Capture:**
1. **Books** - Titles, authors mentioned
2. **Research Papers** - Studies, journals referenced  
3. **Websites/Tools** - Online resources recommended
4. **People** - Experts, influencers cited
5. **Companies/Organizations** - Entities discussed

**Note:** Some may be implied rather than explicitly cited""",
        
        "action_items": """
### Action Items Extraction Guide
**Goal:** Identify concrete steps viewers should take

**Categories:**
1. **Immediate Actions** - What to do right away
2. **Learning Tasks** - Skills to develop, topics to study
3. **Tools to Try** - Software, platforms, methods to test
4. **Habits to Build** - Long-term behavior changes
5. **Decisions to Make** - Choices to consider

**Format:** Clear, actionable language for each item"""
    }
    
    guide = extraction_guides.get(extraction_type, extraction_guides["summary"])
    
    return f"""# 🎯 Content Extraction Workshop

## Extraction Session
**Video:** {video_url}  
**Extraction Type:** {extraction_type.title()}

{guide}

## Extraction Process

**Step 1:** Get the complete transcript using get_youtube_transcript tool

**Step 2:** Read through and identify relevant content based on the guide above

**Step 3:** Organize findings according to the specified structure

**Step 4:** Quality check - ensure accuracy and completeness

**Step 5:** Present findings in a clear, usable format

---
**Instructions for AI:** Use the transcript to extract the requested content type following the guidelines above. Include specific timestamps where relevant and maintain accuracy to the source material."""


async def study_notes_generator(video_url: str, subject_area: str = "general", note_style: str = "outline") -> str:
    """Generate structured study notes from educational video content.
    
    Args:
        video_url: YouTube video URL
        subject_area: Academic subject or field 
        note_style: Format style (outline, cornell, mindmap, flashcards)
    """
    
    style_templates = {
        "outline": """
### Hierarchical Outline Format
```
I. Main Topic
   A. Subtopic
      1. Key point
      2. Supporting detail
         a. Example
         b. Evidence
   B. Subtopic
      1. Key point
II. Main Topic
```""",
        
        "cornell": """
### Cornell Notes Format
```
Cue Column (Keywords/Questions) | Note-Taking Area
-------------------------------|------------------
Key term                      | Detailed explanation
Important question             | Comprehensive answer
Main concept                   | Examples and details

Summary Section:
Brief overview of all key points
```""",
        
        "mindmap": """
### Mind Map Structure
```
Central Topic
├── Branch 1: Main Concept
│   ├── Sub-concept A
│   └── Sub-concept B
├── Branch 2: Main Concept  
│   ├── Sub-concept C
│   └── Sub-concept D
└── Branch 3: Main Concept
    ├── Sub-concept E
    └── Sub-concept F
```""",
        
        "flashcards": """
### Flashcard Format
```
Card 1:
Q: Question or term
A: Answer or definition

Card 2: 
Q: Question or term
A: Answer or definition
```"""
    }
    
    template = style_templates.get(note_style, style_templates["outline"])
    
    return f"""# 📚 Study Notes Generator

## Study Session Setup
**Video:** {video_url}
**Subject Area:** {subject_area.title()}
**Note Style:** {note_style.title()}

## Note-Taking Framework

{template}

### Subject-Specific Guidelines
**For {subject_area}:**
- Focus on key concepts, definitions, and terminology
- Include examples and applications
- Note any formulas, processes, or methodologies
- Identify connections between concepts
- Highlight important facts and figures

### Study Notes Creation Process

**Step 1:** Extract full transcript using get_youtube_transcript tool

**Step 2:** Identify the educational structure:
- Learning objectives (stated or implied)
- Main concepts and subtopics
- Examples and applications
- Key terminology

**Step 3:** Organize content using the {note_style} format

**Step 4:** Add study aids:
- Key terms with definitions
- Important questions for review
- Cross-references and connections
- Practice problems or examples

**Step 5:** Create summary section with main takeaways

---
**Instructions for AI:** Transform the video transcript into comprehensive study notes using the specified format. Focus on educational value and retention."""


async def video_research_planner(topic: str, research_depth: str = "comprehensive") -> str:
    """Plan a research strategy using YouTube videos for learning about a topic.
    
    Args:
        topic: Research topic or question
        research_depth: Level of research (overview, comprehensive, expert)
    """
    
    depth_strategies = {
        "overview": """
### Overview Research Strategy (2-3 hours)
**Goal:** Get a solid foundational understanding

**Video Types to Find:**
1. **Introduction Videos** (2-3 videos)
   - "Introduction to [topic]"
   - "What is [topic]?"
   - Beginner-friendly explanations

2. **Overview/Summary Videos** (1-2 videos)
   - "Everything you need to know about [topic]"
   - Comprehensive overviews
   - "Top 10 things about [topic]"

**Analysis Focus:** Basic concepts, key terminology, main applications""",
        
        "comprehensive": """
### Comprehensive Research Strategy (8-12 hours)
**Goal:** Develop working knowledge and practical understanding

**Video Categories:**
1. **Fundamentals** (3-4 videos)
   - Basic principles and concepts
   - Historical background
   - Core terminology

2. **Deep Dives** (4-5 videos)
   - Detailed explanations of key aspects
   - Case studies and examples
   - Technical implementations

3. **Applications** (2-3 videos)
   - Real-world use cases
   - Industry applications
   - Best practices

4. **Expert Perspectives** (2-3 videos)
   - Advanced insights
   - Current trends and future outlook
   - Expert interviews or lectures

**Analysis Focus:** In-depth understanding, practical applications, critical analysis""",
        
        "expert": """
### Expert-Level Research Strategy (15+ hours)
**Goal:** Achieve specialized knowledge and critical expertise

**Research Phases:**
1. **Foundation Review** (2-3 videos)
   - Ensure solid understanding of basics
   - Identify knowledge gaps

2. **Specialized Topics** (5-7 videos)
   - Advanced technical aspects
   - Specialized applications
   - Cutting-edge developments

3. **Multiple Perspectives** (4-5 videos)
   - Different schools of thought
   - Comparative approaches
   - Controversial or debated aspects

4. **Current Research** (3-4 videos)
   - Latest developments
   - Research findings
   - Future directions

5. **Critical Analysis** (2-3 videos)
   - Limitations and criticisms
   - Alternative approaches
   - Meta-analysis

**Analysis Focus:** Critical evaluation, synthesis of multiple sources, identification of knowledge frontiers"""
    }
    
    strategy = depth_strategies.get(research_depth, depth_strategies["comprehensive"])
    
    return f"""# 🔍 Video Research Planning Workshop

## Research Project Setup
**Topic:** {topic}
**Depth Level:** {research_depth.title()}
**Estimated Time:** {depth_strategies[research_depth].split('(')[1].split(')')[0]}

{strategy}

## Research Methodology

### Video Selection Criteria
- **Authority:** Check presenter credentials and channel reputation
- **Currency:** Prefer recent videos unless studying historical topics
- **Quality:** Look for clear explanations and good production values
- **Completeness:** Ensure comprehensive coverage of subtopics

### Analysis Framework
1. **Content Analysis:** Use transcript_analysis_workshop for each video
2. **Source Comparison:** Use video_comparison_framework for multiple perspectives
3. **Knowledge Extraction:** Use content_extraction_guide to capture key information
4. **Study Materials:** Use study_notes_generator to create learning resources

### Research Documentation
**For Each Video:**
- Full transcript analysis
- Key insights and takeaways
- Source credibility assessment
- Connection to other videos/sources

**Synthesis Phase:**
- Compare and contrast different perspectives
- Identify consensus vs. controversial points
- Create comprehensive overview document
- Note areas requiring additional research

---
**Instructions for AI:** Use this framework to guide systematic video research. Start by identifying appropriate videos, then analyze each using the relevant prompt tools."""


async def list_available_prompts() -> str:
    """List all available prompts and their use cases."""
    
    return """# 🚀 YouTube Transcript Analysis Prompts

## 📝 Available Analysis Prompts

### 1. **transcript_analysis_workshop** (video_url, focus_area)
**Purpose:** Comprehensive analysis of a single video
**Focus Areas:** general, educational, business, technical, entertainment
**Use When:** You want deep, structured analysis of video content

### 2. **video_comparison_framework** (video_urls[], comparison_focus)
**Purpose:** Systematic comparison of multiple videos  
**Focus Areas:** content, style, accuracy, audience
**Use When:** Comparing different perspectives or approaches on a topic

### 3. **content_extraction_guide** (video_url, extraction_type)
**Purpose:** Extract specific types of content from videos
**Extraction Types:** summary, quotes, data, references, action_items
**Use When:** You need specific information or content types

### 4. **study_notes_generator** (video_url, subject_area, note_style)
**Purpose:** Create structured study materials from educational content
**Note Styles:** outline, cornell, mindmap, flashcards
**Use When:** Learning from educational videos or creating study materials

### 5. **video_research_planner** (topic, research_depth)
**Purpose:** Plan comprehensive research using multiple YouTube videos
**Depth Levels:** overview, comprehensive, expert
**Use When:** Starting research on a new topic or planning learning strategy

---

## 🎯 Quick Start Guide

**For Single Video Analysis:**
```
Use: transcript_analysis_workshop
Example: transcript_analysis_workshop("youtube.com/watch?v=...", "educational")
```

**For Comparing Videos:**
```
Use: video_comparison_framework  
Example: video_comparison_framework(["url1", "url2"], "content")
```

**For Specific Content Extraction:**
```
Use: content_extraction_guide
Example: content_extraction_guide("youtube.com/watch?v=...", "quotes")
```

**For Study Materials:**
```
Use: study_notes_generator
Example: study_notes_generator("youtube.com/watch?v=...", "computer_science", "outline")
```

**For Research Planning:**
```
Use: video_research_planner
Example: video_research_planner("machine learning basics", "comprehensive")
```

---

**💡 Pro Tips:**
• All prompts work with the existing transcript extraction tools
• Combine prompts for comprehensive analysis workflows
• Use the research planner first for multi-video projects
• Customize focus areas and extraction types based on your needs"""
