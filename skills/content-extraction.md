# YouTube Content Extraction Guide

You are an expert at extracting specific types of content from YouTube video transcripts. This skill helps you systematically identify and organize particular content types like quotes, data, references, summaries, and action items.

## Purpose

Extract specific types of valuable content from video transcripts in a structured, organized format for easy reference and use.

## When to Use This Skill

- User needs specific information from a video
- Want to extract quotes, data, or references
- Need summary or action items
- Creating resource lists from videos
- Building citation library
- Collecting examples or case studies

## Extraction Types

### 1. Summary Extraction

**Goal:** Create comprehensive yet concise summary

**Use when:**
- Need quick overview of video content
- Sharing video content with others
- Creating video library catalog
- Deciding if deep dive is warranted

**Structure:**
1. **Main Topic** (1 sentence)
   - Clear, specific statement of primary subject

2. **Key Points** (3-5 bullet points)
   - Most important ideas or arguments
   - Core concepts explained
   - Main takeaways

3. **Supporting Details**
   - Examples provided
   - Evidence presented
   - Explanations given
   - Context and background

4. **Conclusion/Takeaway** (1-2 sentences)
   - Final message or recommendation
   - What viewers should remember

**Quality Criteria:**
- Captures essence without losing important details
- Logical flow and organization
- Neutral tone and accurate representation
- Appropriate length (10-15% of original)
- Self-contained (understandable without video)

**Output Format:**
```markdown
# Summary: [VIDEO TITLE]

## Main Topic
[One clear sentence describing the primary subject]

## Key Points
1. [First major point with brief explanation]
2. [Second major point with brief explanation]
3. [Third major point with brief explanation]
4. [Fourth major point with brief explanation]
5. [Fifth major point with brief explanation]

## Supporting Details

### [Topic Area 1]
- Example: [specific example given]
- Evidence: [data or research mentioned]
- Explanation: [how concept was explained]

### [Topic Area 2]
[Same structure]

## Conclusion
[1-2 sentences capturing the final message and main takeaway]

**Video Details:**
- Duration: [length]
- Channel: [name]
- URL: [link]
- Summary Length: [word count] words ([%] of estimated transcript)
```

---

### 2. Quote Extraction

**Goal:** Identify most impactful and memorable quotes

**Use when:**
- Creating highlight reels
- Building quote libraries
- Finding shareable content
- Supporting arguments with citations
- Identifying key insights

**Types to Look For:**

1. **Key Insights**
   - Novel ideas or important realizations
   - "Aha!" moments
   - Breakthrough concepts
   - Paradigm shifts

2. **Memorable Phrases**
   - Catchy or profound statements
   - Quotable soundbites
   - Eloquent expressions
   - Definitions or principles

3. **Practical Advice**
   - Actionable recommendations
   - How-to guidance
   - Best practices
   - Tips and tricks

4. **Supporting Evidence**
   - Statistics and data
   - Research findings
   - Expert opinions
   - Factual claims

5. **Personal Stories**
   - Anecdotes illustrating points
   - Personal experiences
   - Case studies
   - Real-world examples

**Output Format:**
```markdown
# Key Quotes: [VIDEO TITLE]

## 🎯 Key Insights

### Quote 1
> "[Exact quote from transcript]"

- **Timestamp:** [MM:SS]
- **Context:** [What was being discussed]
- **Why Important:** [Significance of this quote]
- **Application:** [How to use this insight]

### Quote 2
[Same structure]

---

## 💬 Memorable Phrases

### Quote 3
> "[Exact quote]"

- **Timestamp:** [MM:SS]
- **Context:** [Background]
- **Impact:** [Why this stands out]

---

## 🛠️ Practical Advice

### Quote 4
> "[Exact quote with actionable advice]"

- **Timestamp:** [MM:SS]
- **Action:** [What to do with this advice]
- **Difficulty:** [Easy/Medium/Hard to implement]

---

## 📊 Data & Evidence

### Quote 5
> "[Quote with statistic or research finding]"

- **Timestamp:** [MM:SS]
- **Source:** [If mentioned in video]
- **Reliability:** [Assessment of claim]

---

## 📖 Stories & Examples

### Quote 6
> "[Quote from story or example]"

- **Timestamp:** [MM:SS]
- **Story Summary:** [Brief context]
- **Lesson:** [What this illustrates]

---

**Total Quotes Extracted:** [count]
**Video URL:** [link]
```

---

### 3. Data & Statistics Extraction

**Goal:** Identify all quantitative information and data points

**Use when:**
- Fact-checking content
- Building evidence base
- Creating data-driven presentations
- Research and analysis
- Tracking trends and metrics

**Categories:**

1. **Statistics**
   - Percentages and ratios
   - Counts and frequencies
   - Averages and medians
   - Growth rates

2. **Research Findings**
   - Study results
   - Survey data
   - Experimental outcomes
   - Meta-analysis results

3. **Financial Data**
   - Costs and prices
   - Revenues and profits
   - Market sizes
   - Investment figures

4. **Dates & Timelines**
   - Historical dates
   - Project timelines
   - Projections and forecasts
   - Milestones

5. **Measurements**
   - Performance metrics
   - Comparisons and rankings
   - Before/after measurements
   - Technical specifications

**Output Format:**
```markdown
# Data & Statistics: [VIDEO TITLE]

## 📊 Statistics

### [Topic/Category]
- **Statistic:** [e.g., "70% of users"]
  - **Timestamp:** [MM:SS]
  - **Full Context:** "[complete quote]"
  - **Source:** [if mentioned]
  - **Reliability:** [assessment]

[Repeat for all statistics]

---

## 🔬 Research Findings

### Study 1: [Study name if mentioned]
- **Finding:** [What was found]
- **Timestamp:** [MM:SS]
- **Source:** [Journal/institution if mentioned]
- **Sample Size:** [if mentioned]
- **Year:** [if mentioned]

---

## 💰 Financial Data

### [Financial Topic]
- **Figure:** [e.g., "$10M revenue"]
  - **Timestamp:** [MM:SS]
  - **Context:** [What this refers to]
  - **Time Period:** [if specified]
  - **Source:** [if mentioned]

---

## 📅 Dates & Timelines

### Historical Events
- **[Year]:** [Event description]
  - **Timestamp:** [MM:SS]
  - **Significance:** [Why mentioned]

### Projections
- **[Future Date]:** [Prediction/projection]
  - **Timestamp:** [MM:SS]
  - **Confidence:** [if indicated]

---

## 📏 Measurements & Metrics

### Performance Metrics
- **Metric:** [e.g., "99.9% uptime"]
  - **Timestamp:** [MM:SS]
  - **Benchmark:** [Comparison if given]
  - **Context:** [What was measured]

---

**Total Data Points Extracted:** [count]
**Note:** Always verify important statistics with original sources when possible.
```

---

### 4. References & Sources

**Goal:** Catalog all mentioned sources and further reading

**Use when:**
- Creating bibliography
- Following up on research
- Verifying claims
- Building resource library
- Academic research

**Types to Capture:**

1. **Books**
   - Titles and authors
   - Publication details if mentioned
   - Specific chapters/sections referenced

2. **Research Papers**
   - Studies and journals
   - Authors and institutions
   - Key findings mentioned

3. **Websites/Tools**
   - Online resources recommended
   - Software and platforms
   - Databases and repositories

4. **People**
   - Experts and influencers cited
   - Interview subjects
   - Thought leaders mentioned

5. **Companies/Organizations**
   - Entities discussed
   - Industry examples
   - Institutions referenced

**Output Format:**
```markdown
# References & Sources: [VIDEO TITLE]

## 📚 Books Mentioned

### Book 1: [Title]
- **Author:** [Name]
- **Timestamp:** [MM:SS]
- **Context:** [How it was referenced]
- **Specific Chapter:** [if mentioned]
- **Recommendation Level:** [Highly recommended/Mentioned/Critical of]
- **Availability:** [Link if easily findable]

---

## 📄 Research Papers & Studies

### Paper 1: [Title or Description]
- **Authors:** [if mentioned]
- **Journal/Source:** [if mentioned]
- **Year:** [if mentioned]
- **Timestamp:** [MM:SS]
- **Key Finding Cited:** [What was referenced]
- **How to Find:** [Search terms or DOI if available]

---

## 🌐 Websites & Online Tools

### Resource 1: [Name]
- **Type:** [Website/Tool/Platform/Database]
- **URL:** [if mentioned or easily found]
- **Timestamp:** [MM:SS]
- **Purpose:** [What it's used for]
- **Recommendation:** [How strongly endorsed]

---

## 👤 People & Experts Cited

### Person 1: [Name]
- **Role/Credentials:** [if mentioned]
- **Timestamp:** [MM:SS]
- **Context:** [Why they were cited]
- **Quote:** [If specific quote attributed]
- **How to Learn More:** [Twitter, website, etc. if mentioned]

---

## 🏢 Companies & Organizations

### Organization 1: [Name]
- **Type:** [Company/Institution/Non-profit/etc.]
- **Timestamp:** [MM:SS]
- **Context:** [Why mentioned]
- **Example/Case Study:** [If used as example]

---

## 📖 Additional Resources

### Implicit References
[Things implied or alluded to but not explicitly cited]

### Further Reading Suggestions
[If presenter recommends related topics to explore]

---

**Total References:** [count]
**Note:** Some references may be implied rather than explicitly cited.
```

---

### 5. Action Items Extraction

**Goal:** Identify concrete steps viewers should take

**Use when:**
- Creating implementation guides
- Building to-do lists from learning
- Planning next steps
- Tracking recommendations
- Creating actionable summaries

**Categories:**

1. **Immediate Actions**
   - What to do right away
   - Quick wins
   - First steps

2. **Learning Tasks**
   - Skills to develop
   - Topics to study
   - Resources to explore

3. **Tools to Try**
   - Software to test
   - Platforms to explore
   - Methods to experiment with

4. **Habits to Build**
   - Long-term behavior changes
   - Routines to establish
   - Practices to adopt

5. **Decisions to Make**
   - Choices to consider
   - Options to evaluate
   - Strategies to select

**Output Format:**
```markdown
# Action Items: [VIDEO TITLE]

## ⚡ Immediate Actions (Do Today)

### Action 1: [Clear, actionable statement]
- **Timestamp:** [MM:SS]
- **How to Do It:** [Step-by-step if provided]
- **Time Required:** [Estimate]
- **Difficulty:** [Easy/Medium/Hard]
- **Why Important:** [Benefit or reason]
- **Status:** [ ] Not Started / [ ] In Progress / [ ] Completed

---

## 📚 Learning Tasks (This Week/Month)

### Learning Goal 1: [What to learn]
- **Timestamp:** [MM:SS]
- **Resources Suggested:** [If any mentioned]
- **Prerequisites:** [If any mentioned]
- **Time Estimate:** [If provided]
- **Priority:** [High/Medium/Low]

---

## 🛠️ Tools & Methods to Try

### Tool 1: [Name of tool/method]
- **Timestamp:** [MM:SS]
- **Purpose:** [What it's for]
- **How to Access:** [Where to get it]
- **Cost:** [Free/Paid - if mentioned]
- **Getting Started:** [First steps]

---

## 🔄 Habits to Build (Long-term)

### Habit 1: [Habit to establish]
- **Timestamp:** [MM:SS]
- **Frequency:** [Daily/Weekly/etc. - if specified]
- **Expected Benefit:** [What you'll gain]
- **How to Start:** [Initial steps]
- **Tracking Method:** [If suggested]

---

## 🤔 Decisions to Make

### Decision 1: [Choice to consider]
- **Timestamp:** [MM:SS]
- **Options:** [If presented]
  - Option A: [Pro/cons]
  - Option B: [Pro/cons]
- **Recommendation:** [If given]
- **Deadline:** [If mentioned]

---

## 🎯 Complete Action Plan

### Week 1
- [ ] [Action item]
- [ ] [Action item]

### Month 1
- [ ] [Learning task]
- [ ] [Tool to try]

### Ongoing
- [ ] [Habit to build]
- [ ] [Habit to build]

---

**Total Action Items:** [count]
**Estimated Time to Complete All:** [estimate]
**Difficulty Level:** [Overall assessment]
```

---

## Extraction Process

### Step 1: Get Complete Transcript
1. Use youtube-transcript skill to extract transcript
2. Verify quality and completeness
3. Save for reference

### Step 2: First Read-Through
1. Read entire transcript without stopping
2. Get overall sense of content
3. Identify sections relevant to extraction type
4. Note timestamps of key moments

### Step 3: Detailed Extraction
1. Go through transcript systematically
2. Extract items matching chosen type
3. Capture exact quotes with timestamps
4. Note context for each item
5. Organize by category

### Step 4: Quality Check
1. Verify accuracy of quotes
2. Ensure timestamps are correct
3. Check completeness
4. Validate context
5. Remove duplicates

### Step 5: Organize & Format
1. Structure according to template
2. Add context and explanations
3. Include metadata
4. Cross-reference related items
5. Create summary statistics

## Best Practices

### ✅ Do:
- **Be comprehensive** - Don't miss important items
- **Preserve exact wording** - Quote accurately
- **Include timestamps** - Enable verification
- **Provide context** - Explain why item matters
- **Categorize logically** - Organize for easy reference
- **Cross-reference** - Link related items
- **Assess quality** - Note reliability of sources
- **Make actionable** - Especially for action items

### ❌ Don't:
- Paraphrase when exact quote needed
- Extract out of context
- Skip timestamp documentation
- Over-extract (include everything)
- Under-extract (miss key items)
- Lose neutrality (add bias)
- Forget source attribution
- Ignore quality signals

## Multi-Type Extraction

**For comprehensive video analysis, extract multiple types:**

1. **Start with Summary** - Get overview
2. **Extract Quotes** - Capture key statements
3. **Pull Data** - Gather facts and figures
4. **Document References** - Build resource list
5. **List Actions** - Create implementation guide

**This creates complete resource from single video.**

## Example Usage

**User:** "Extract all the actionable advice from this productivity video"

**Your Process:**
1. Extract transcript using youtube-transcript skill
2. Read through identifying action items
3. Categorize into immediate/learning/habits
4. Create structured action plan
5. Include timestamps and difficulty levels
6. Provide complete checklist

## Integration with Other Skills

**Workflow:**
1. **youtube-transcript** - Extract content
2. **content-extraction** (this skill) - Pull specific types
3. **youtube-analysis** - Deep analysis if needed
4. **study-notes** - Create study materials from extracted content

**Use extracted content for:**
- Building comprehensive notes
- Creating reference libraries
- Planning implementation
- Research documentation
- Resource sharing

---

**Note:** This skill requires a transcript to work with. Use youtube-transcript skill first to extract the video content, then apply these extraction frameworks.
